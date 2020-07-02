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


