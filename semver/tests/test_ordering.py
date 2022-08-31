import unittest

from semver.version import Version


class TestOrdering(unittest.TestCase):
    """ Test cases for precedence, as outlined in the official
    documentation at https://semver.org.  The test case names
    refer to the examples given in the document.  I cover all
    the examples and have added test cases of my own.
    """

    def test_11_2(self):
        a = Version('1.0.0')
        b = Version('2.0.0')
        c = Version('2.1.0')
        d = Version('2.1.1')
        self.assertTrue(a < b)
        self.assertTrue(b < c)
        self.assertTrue(c < d)
        self.assertFalse(d < c)

    def test_11_3(self):
        a = Version('1.0.0-alpha')
        b = Version('1.0.0')
        self.assertTrue(a < b)

    def test_11_4(self):
        a = Version('1.0.0-alpha')
        b = Version('1.0.0-alpha.1')
        c = Version('1.0.0-alpha.beta')
        d = Version('1.0.0-beta')
        e = Version('1.0.0-beta.2')
        f = Version('1.0.0-beta.11')
        g = Version('1.0.0-rc.1')
        h = Version('1.0.0')
        self.assertLess(a, b)
        self.assertLess(b, c)
        self.assertLess(c, d)
        self.assertLess(d, e)
        self.assertLess(e, f)
        self.assertLess(f, g)
        self.assertLess(g, h)

    def test_equal_full(self):
        a = Version('1.2.3-RC1+build3562')
        b = Version('1.2.3-RC2+build3562')
        self.assertTrue(a == a)
        self.assertFalse(a == b)

    def test_equal_no_build_metadata(self):
        a = Version('1.2.3-RC1')
        b = Version('1.2.3-RC2')
        self.assertTrue(a == a)
        self.assertFalse(a == b)

    def test_equal_no_prerelease(self):
        a = Version('1.2.3+build3562')
        b = Version('1.2.3+build3563')
        self.assertTrue(a == a)
        self.assertTrue(a == b)

    def test_compare_longer_prerelease(self):
        a = Version('1.0.0-alpha')
        b = Version('1.0.0-alpha.rc1')
        self.assertLess(a, b)

    def test_compare_with_prerelease(self):
        a = Version('1.2.3----R-S.12.9.1--.12+meta')
        b = Version('1.1.7')
        self.assertTrue(a > b)

    def test_single_digit_vs_double_digit(self):
        a = Version("2.3.4-10")
        b = Version("2.3.4-2")
        self.assertTrue(a > b)

    def test_sort(self):
        version_strings = [
            '0.0.4',
            '1.0.0-0A.is.legal',
            '1.0.0-alpha',
            '1.0.0-alpha+beta',
            '1.0.0-alpha.1',
            '1.0.0-alpha.0valid',
            '1.0.0-alpha.beta',
            '1.0.0-alpha.beta.1',
            '1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay',
            '1.0.0-alpha0.valid',
            '1.0.0-beta',
            '1.0.0-rc.1+build.1',
            '1.0.0',
            '1.0.0+0.build.1-rc.10000aaa-kk-0.1',
            '1.1.2-prerelease+meta',
            '1.1.2+meta',
            '1.1.2+meta-valid',
            '1.1.7',
            '1.2.3----R-S.12.9.1--.12+meta',
            '1.2.3----RC-SNAPSHOT.12.9.1--.12+788',
            '1.2.3----RC-SNAPSHOT.12.9.1--.12',
            '1.2.3-SNAPSHOT-123',
            '1.2.3-beta',
            '1.2.3',
            '2.0.0-rc.1+build.123',
            '2.0.0',
            '2.0.0+build.1848',
            '2.0.1-alpha.1227',
            '10.2.3-DEV-SNAPSHOT',
            '10.20.30',
            '99999999999999999999999.999999999999999999.99999999999999999',
        ]

        expected_list: list[str] = version_strings
        actual_version_list: list[Version] = [Version(x) for x in version_strings]
        actual_version_list.sort(key=lambda x: x)
        actual_list: list[str] = [x.version_string for x in actual_version_list]
        self.assertListEqual(expected_list, actual_list)
