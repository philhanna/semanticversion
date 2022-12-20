from semver import Version


def test_str():
    expected = "1.2.3-abc+def"
    v = Version(expected)
    actual = str(v)
    assert actual == expected


def test_hash():
    expected = "1.2.3-abc+def"
    v = Version(expected)
    assert hash(v) != 0