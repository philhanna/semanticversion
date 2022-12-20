"""Test data taken from https://regex101.com/r/Ly7O1x/3/"""
import pytest

from semver import Version


# GOOD STRINGS

@pytest.mark.parametrize("version_string,major,minor,patch,prerel,meta", [
    ('0.0.4', 0, 0, 4, None, None),
    ('1.2.3', 1, 2, 3, None, None),
    ('10.20.30', 10, 20, 30, None, None),
    ('1.1.2-prerelease+meta', 1, 1, 2, 'prerelease', 'meta'),
    ('1.1.2+meta', 1, 1, 2, None, 'meta'),
    ('1.1.2+meta-valid', 1, 1, 2, None, 'meta-valid'),
    ('1.0.0-alpha', 1, 0, 0, 'alpha', None),
    ('1.0.0-beta', 1, 0, 0, 'beta', None),
    ('1.0.0-alpha.beta', 1, 0, 0, 'alpha.beta', None),
    ('1.0.0-alpha.beta.1', 1, 0, 0, 'alpha.beta.1', None),
    ('1.0.0-alpha.1', 1, 0, 0, 'alpha.1', None),
    ('1.0.0-alpha0.valid', 1, 0, 0, 'alpha0.valid', None),
    ('1.0.0-alpha.0valid', 1, 0, 0, 'alpha.0valid', None),
    ('1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay', 1, 0, 0, 'alpha-a.b-c-somethinglong',
     'build.1-aef.1-its-okay'),
    ('1.0.0-rc.1+build.1', 1, 0, 0, 'rc.1', 'build.1'),
    ('2.0.0-rc.1+build.123', 2, 0, 0, 'rc.1', 'build.123'),
    ('1.2.3-beta', 1, 2, 3, 'beta', None),
    ('10.2.3-DEV-SNAPSHOT', 10, 2, 3, 'DEV-SNAPSHOT', None),
    ('1.2.3-SNAPSHOT-123', 1, 2, 3, 'SNAPSHOT-123', None),
    ('1.0.0', 1, 0, 0, None, None),
    ('2.0.0', 2, 0, 0, None, None),
    ('1.1.7', 1, 1, 7, None, None),
    ('2.0.0+build.1848', 2, 0, 0, None, 'build.1848'),
    ('2.0.1-alpha.1227', 2, 0, 1, 'alpha.1227', None),
    ('1.0.0-alpha+beta', 1, 0, 0, 'alpha', 'beta'),
    ('1.2.3----RC-SNAPSHOT.12.9.1--.12+788', 1, 2, 3, '---RC-SNAPSHOT.12.9.1--.12', '788'),
    ('1.2.3----R-S.12.9.1--.12+meta', 1, 2, 3, '---R-S.12.9.1--.12', 'meta'),
    ('1.2.3----RC-SNAPSHOT.12.9.1--.12', 1, 2, 3, '---RC-SNAPSHOT.12.9.1--.12', None),
    ('1.0.0+0.build.1-rc.10000aaa-kk-0.1', 1, 0, 0, None, '0.build.1-rc.10000aaa-kk-0.1'),
    ('99999999999999999999999.999999999999999999.99999999999999999', 99999999999999999999999, 999999999999999999,
     99999999999999999, None, None),
    ('1.0.0-0A.is.legal', 1, 0, 0, '0A.is.legal', None),
])
def test_good_version(version_string, major, minor, patch, prerel, meta):
    version = Version(version_string)
    assert version.major == major
    assert version.minor == minor
    assert version.patch == patch
    assert version.prerelease == prerel
    assert version.buildmetadata == meta


# BAD_STRINGS
@pytest.mark.parametrize("version_string", [
    '2.1',
    '1',
    '1.2',
    '1.2.3-0123',
    '1.2.3-0123.0123',
    '1.1.2+.123',
    '+invalid',
    '-invalid',
    '-invalid+invalid',
    '-invalid.01',
    'alpha',
    'alpha.beta',
    'alpha.beta.1',
    'alpha.1',
    'alpha+beta',
    'alpha_beta',
    'alpha.',
    'alpha..',
    'beta',
    '1.0.0-alpha_beta',
    '-alpha.',
    '1.0.0-alpha..',
    '1.0.0-alpha..1',
    '1.0.0-alpha...1',
    '1.0.0-alpha....1',
    '1.0.0-alpha.....1',
    '1.0.0-alpha......1',
    '1.0.0-alpha.......1',
    '01.1.1',
    '1.01.1',
    '1.1.01',
    '1.2',
    '1.2.3.DEV',
    '1.2-SNAPSHOT',
    '1.2.31.2.3----RC-SNAPSHOT.12.09.1--..12+788',
    '1.2-RC-SNAPSHOT',
    '-1.0.3-gamma+b7718',
    '+justmeta',
    '9.8.7+meta+meta',
    '9.8.7-whatever+meta+meta',
    '99999999999999999999999.999999999999999999.99999999999999999----RC-SNAPSHOT.12.09.1'
    '--------------------------------..12',
])
def test_bad_version(version_string):
    with pytest.raises(ValueError) as ve:
        Version(version_string)
