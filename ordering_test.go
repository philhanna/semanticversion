package semver

import (
	"sort"
	"testing"
)

// Test cases for precedence, as outlined in the official documentation
// at https://semver.org.  The test case names refer to the examples
// given in the document.  I cover all the examples and have added test
// cases of my own.

func TestOrder_11_2(t *testing.T) {
	a, _ := NewVersion("1.0.0")
	b, _ := NewVersion("2.0.0")
	c, _ := NewVersion("2.1.0")
	d, _ := NewVersion("2.1.1")
	assertLess(t, a, b)
	assertLess(t, b, c)
	assertLess(t, c, d)
	assertGreaterOrEqual(t, d, c)
}

func TestOrder_11_3(t *testing.T) {
	a, _ := NewVersion("1.0.0-alpha")
	b, _ := NewVersion("1.0.0")
	assertLess(t, a, b)
}

func TestOrder_11_4(t *testing.T) {
	a, _ := NewVersion("1.0.0-alpha")
	b, _ := NewVersion("1.0.0-alpha.1")
	c, _ := NewVersion("1.0.0-alpha.beta")
	d, _ := NewVersion("1.0.0-beta")
	e, _ := NewVersion("1.0.0-beta.2")
	f, _ := NewVersion("1.0.0-beta.11")
	g, _ := NewVersion("1.0.0-rc.1")
	h, _ := NewVersion("1.0.0")
	assertLess(t, a, b)
	assertLess(t, b, c)
	assertLess(t, c, d)
	assertLess(t, d, e)
	assertLess(t, e, f)
	assertLess(t, f, g)
	assertLess(t, g, h)
}

func TestOrder_equalFull(t *testing.T) {
	a, _ := NewVersion("1.2.3-RC1+build3562")
	b, _ := NewVersion("1.2.3-RC2+build3562")
	assertEqual(t, a, a)
	assertNotEqual(t, a, b)
}

func TestOrder_equalNoBuildMetadata(t *testing.T) {
	a, _ := NewVersion("1.2.3-RC1")
	b, _ := NewVersion("1.2.3-RC2")
	assertEqual(t, a, a)
	assertNotEqual(t, a, b)
}

func TestOrder_equalNoPrerelease(t *testing.T) {
	a, _ := NewVersion("1.2.3+build3562")
	b, _ := NewVersion("1.2.3+build3563")
	assertEqual(t, a, a)
	assertEqual(t, a, b)
}

func TestOrder_compareLongerPrerelease(t *testing.T) {
	a, _ := NewVersion("1.0.0-alpha")
	b, _ := NewVersion("1.0.0-alpha.rc1")
	assertLess(t, a, b)
}

func TestOrder_compareWithPrerelease(t *testing.T) {
	a, _ := NewVersion("1.2.3----R-S.12.9.1--.12+meta")
	b, _ := NewVersion("1.1.7")
	assertGreater(t, a, b)
}

func TestOrder_singleDigitVsDoubleDigit(t *testing.T) {
	a, _ := NewVersion("2.3.4-10")
	b, _ := NewVersion("2.3.4-2")
	assertGreater(t, a, b)
}

func TestOrder_sort(t *testing.T) {
	expectedList := []string{
		"0.0.4",
		"1.0.0-0A.is.legal",
		"1.0.0-alpha",
		"1.0.0-alpha+beta",
		"1.0.0-alpha.1",
		"1.0.0-alpha.0valid",
		"1.0.0-alpha.beta",
		"1.0.0-alpha.beta.1",
		"1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay",
		"1.0.0-alpha0.valid",
		"1.0.0-beta",
		"1.0.0-rc.1+build.1",
		"1.0.0",
		"1.0.0+0.build.1-rc.10000aaa-kk-0.1",
		"1.1.2-prerelease+meta",
		"1.1.2+meta",
		"1.1.2+meta-valid",
		"1.1.7",
		"1.2.3----R-S.12.9.1--.12+meta",
		"1.2.3----RC-SNAPSHOT.12.9.1--.12+788",
		"1.2.3----RC-SNAPSHOT.12.9.1--.12",
		"1.2.3-SNAPSHOT-123",
		"1.2.3-beta",
		"1.2.3",
		"2.0.0-rc.1+build.123",
		"2.0.0",
		"2.0.0+build.1848",
		"2.0.1-alpha.1227",
		"10.2.3-DEV-SNAPSHOT",
		"10.20.30",
		"99999999999999999999999.999999999999999999.99999999999999999",
	}

	// Convert all version strings to Version types
	actualVersionList := make([]Version, 0, len(expectedList))
	for _, s := range expectedList {
		version, _ := NewVersion(s)
		actualVersionList = append(actualVersionList, version)
	}

	// Sort by the Version Compare function
	sort.Slice(actualVersionList, func(i, j int) bool {
		return actualVersionList[i].Compare(actualVersionList[j]) < 0
	})

	// Copy the versions back to a list of strings
	actualList := make([]string, 0, len(actualVersionList))
	for _, v := range actualVersionList {
		actualList = append(actualList, v.VersionString)
	}

	for i := range actualList {
		have := actualList[i]
		want := expectedList[i]
		if have != want {
			t.Errorf("At %d, have=%q, want=%q", i, have, want)
		}
	}
}

func assertLess(t *testing.T, a Version, b Version) {
	if !(a.Compare(b) < 0) {
		t.Errorf("%s is not less than %s", a, b)
	}
}

func assertGreater(t *testing.T, a Version, b Version) {
	if !(a.Compare(b) > 0) {
		t.Errorf("%s is not greater than %s", a, b)
	}
}

func assertEqual(t *testing.T, a Version, b Version) {
	if !(a.Compare(b) == 0) {
		t.Errorf("%s is not equal to %s", a, b)
	}
}

func assertGreaterOrEqual(t *testing.T, a Version, b Version) {
	if !(a.Compare(b) >= 0) {
		t.Errorf("%s is not greater than or equal to %s", a, b)
	}
}

func assertLessOrEqual(t *testing.T, a Version, b Version) {
	if !(a.Compare(b) <= 0) {
		t.Errorf("%s is not less than or equal to %s", a, b)
	}
}

func assertNotEqual(t *testing.T, a Version, b Version) {
	if !(a.Compare(b) != 0) {
		t.Errorf("%s is equal to %s", a, b)
	}
}
