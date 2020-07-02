from itertools import zip_longest
import re


class Version:
    """ A semantic versioned version class

    See https://semver.org for a normative description of
    semantic versioning.

    The basic structure of a semantic version is major.minor.patch,
    where each component is an integer with no leading zeros.
    These three components are all required.

    A semantic version may also contain:
    - A prerelase component, which follows the first '-' and ends
    at the first '+', if any
    - A buildmetadata component, which follows the first '+'
    Both of these are optional.

    A change in the major version means that backwards incompatible
    changes have been introduced into the public API.  When the
    major version changes, the minor and patch versions must be
    reset to zero.

    A change in the minor version means that backwards compatible
    functionality has been added to the public API.  When the minor
    version changes, the patch version must be reset to zero.

    A change in the patch version means that backwards compatible
    bug fixes have been introduced.

    See the official documentation for a description of the
    prerelease and buildmetadata components.

    Semantic versions have a strict ordering; that is, any two
    are comparable according to a set of rules:

    1. Precedence MUST be calculated by separating the version into
    major, minor, patch and pre-release identifiers in that order (Build
    metadata does not figure into precedence).

    2. Precedence is determined by the first difference when comparing
    each of these identifiers from left to right as follows: Major,
    minor, and patch versions are always compared numerically.

    Example: 1.0.0 < 2.0.0 < 2.1.0 < 2.1.1.

    3. When major, minor, and patch are equal, a pre-release version has
    lower precedence than a normal version:

    Example: 1.0.0-alpha < 1.0.0.

    4. Precedence for two pre-release versions with the same major,
    minor, and patch version MUST be determined by comparing each dot
    separated identifier from left to right until a difference is found
    as follows:

        - Identifiers consisting of only digits are compared numerically.

        - Identifiers with letters or hyphens are compared lexically in
          ASCII sort order.

        - Numeric identifiers always have lower precedence than
          non-numeric identifiers.

        - A larger set of pre-release fields has a higher precedence
          than a smaller set, if all of the preceding identifiers are
          equal.

          Example: 1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta
                  < 1.0.0-beta < 1.0.0-beta.2 < 1.0.0-beta.11
                  < 1.0.0-rc.1 < 1.0.0.


    See https://regex101.com/r/Ly7O1x/3/ for the regular expression used
    to parse the version string.

    """

    def __init__(self, version_string):
        regexp = re.compile((
            r'''^'''
            r'''(?P<major>0|[1-9]\d*)'''
            r'''\.'''
            r'''(?P<minor>0|[1-9]\d*)'''
            r'''\.'''
            r'''(?P<patch>0|[1-9]\d*)'''
            r'''(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'''
            r'''(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))'''
            r'''?$'''
        ))
        m = regexp.match(version_string)
        if not m:
            errmsg = f"{version_string} is not a valid semantic version number. See https://semver.org"
            raise ValueError(errmsg)
        self.major = m.group('major')
        self.minor = m.group('minor')
        self.patch = m.group('patch')
        self.prerelease = m.group('prerelease')
        self.buildmetadata = m.group('buildmetadata')

    @property
    def major(self):
        """ Returns the major version """
        return self._major

    @major.setter
    def major(self, value):
        """ Sets the major version """
        self._major = int(value)

    @property
    def minor(self):
        """ Returns the minor version """
        return self._minor

    @minor.setter
    def minor(self, value):
        """ Sets the minor version """
        self._minor = int(value)

    @property
    def patch(self):
        """ Returns the patch version """
        return self._patch

    @patch.setter
    def patch(self, value):
        """ Sets the patch version """
        self._patch = int(value)

    @property
    def prerelease(self):
        """ Returns the prerelease version """
        return self._prerelease

    @prerelease.setter
    def prerelease(self, value):
        """ Sets the prerelease version """
        self._prerelease = value

    @property
    def buildmetadata(self):
        """ Returns the buildmetadata version """
        return self._buildmetadata

    @buildmetadata.setter
    def buildmetadata(self, value):
        """ Sets the buildmetadata version """
        self._buildmetadata = value

    def __str__(self):
        basic_string = ".".join([str(self.major), str(self.minor), str(self.patch)])
        if self.prerelease is not None:
            basic_string += "-" + self.prerelease
        if self.buildmetadata is not None:
            basic_string += "+" + self.buildmetadata
        return basic_string

    def __gt__(self, other):
        return self.compare(other) > 0

    def __lt__(self, other):
        return self.compare(other) < 0

    def __eq__(self, other):
        return self.compare(other) == 0

    def __ge__(self, other):
        return self.compare(other) >= 0

    def __le__(self, other):
        return self.compare(other) <= 0

    def __ne__(self, other):
        return self.compare(other) != 0

    def __hash__(self):
        return hash(self.__str__())

    def compare(self, other):
        """ Compares two versions and returns -1, 0, or 1

        The __gt__, __lt__, __eq__, __ge__, __le__, and __ne__
        relations are based on this.

        Note that build metadata is NOT considered in precedence comparisons,
        according to the specification.
        """
        if self.major < other.major:
            return -1
        elif self.major > other.major:
            return 1
        elif self.minor < other.minor:
            return -1
        elif self.minor > other.minor:
            return 1
        elif self.patch < other.patch:
            return -1
        elif self.patch > other.patch:
            return 1

        # At this point, we know the three primary components are equal

        # 11.3 A pre-release version has lower precedence than a normal version
        if all([self.prerelease is not None,
                other.prerelease is None]):
            return -1
        if all([self.prerelease is None,
                other.prerelease is not None]):
            return 1
        if all([self.prerelease is None,
                other.prerelease is None]):
            return 0

        # 11.4 - Precedence for two pre-release versions with the same
        # major, minor, and patch must be determined by comparing each
        # dot-separated identifier from left to right until a difference
        # is found

        def is_integer(x):
            return all([ch in "0123456789" for ch in str(x)])

        these_fields = self.prerelease.split('.')
        those_fields = other.prerelease.split('.')
        for this, that in zip_longest(these_fields, those_fields):

            # 11.4.4 Longer sets are greater than shorter sets
            if this is None and that is not None:
                return -1
            if this is not None and that is None:
                return 1

            # 11.4.1 Integers are compared numerically
            if is_integer(this) and is_integer(that):
                this = int(this)
                that = int(that)
                if this < that:
                    return -1
                if this > that:
                    return 1

            # 11.4.3 Numerics are always less than non-numerics
            if is_integer(this) and not is_integer(that):
                return -1
            if not is_integer(this) and is_integer(that):
                return 1

            # 11.4.2 Nonnumeric fields are compared lexicographically
            if this < that:
                return -1
            if this > that:
                return 1

        # Welp, they must be equal

        return 0
