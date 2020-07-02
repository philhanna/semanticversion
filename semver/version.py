import re


class Version:
    """ A semantic versioned version class

    See https://semver.org for background.
    See https://regex101.com/r/Ly7O1x/3/ for the regular expression used
    to parse the version string
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
        self._major = value

    @property
    def minor(self):
        """ Returns the minor version """
        return self._minor

    @minor.setter
    def minor(self, value):
        """ Sets the minor version """
        self._minor = value

    @property
    def patch(self):
        """ Returns the patch version """
        return self._patch

    @patch.setter
    def patch(self, value):
        """ Sets the patch version """
        self._patch = value

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
