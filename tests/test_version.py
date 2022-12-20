from unittest import TestCase

from semver import Version


class TestVersion(TestCase):

    def test_str(self):
        expected = "1.2.3-abc+def"
        v = Version(expected)
        actual = str(v)
        self.assertEqual(expected, actual)

    def test_hash(self):
        expected = "1.2.3-abc+def"
        v = Version(expected)
        self.assertNotEqual(0, hash(v))
