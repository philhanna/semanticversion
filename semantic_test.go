package semver

// Test data taken from https://regex101.com/r/Ly7O1x/3/

import "testing"

// TestVersion_good tests for valid version strings
func TestVersion_good(t *testing.T) {
	tests := []struct {
		versionString string
		major         int
		minor         int
		patch         int
		prerelease    string
		buildmetadata string
	}{
		{"0.0.4", 0, 0, 4, "", ""},
		{"1.2.3", 1, 2, 3, "", ""},
		{"10.20.30", 10, 20, 30, "", ""},
		{"1.1.2-prerelease+meta", 1, 1, 2, "prerelease", "meta"},
		{"1.1.2+meta", 1, 1, 2, "", "meta"},
		{"1.1.2+meta-valid", 1, 1, 2, "", "meta-valid"},
		{"1.0.0-alpha", 1, 0, 0, "alpha", ""},
		{"1.0.0-beta", 1, 0, 0, "beta", ""},
		{"1.0.0-alpha.beta", 1, 0, 0, "alpha.beta", ""},
		{"1.0.0-alpha.beta.1", 1, 0, 0, "alpha.beta.1", ""},
		{"1.0.0-alpha.1", 1, 0, 0, "alpha.1", ""},
		{"1.0.0-alpha0.valid", 1, 0, 0, "alpha0.valid", ""},
		{"1.0.0-alpha.0valid", 1, 0, 0, "alpha.0valid", ""},
		{"1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay", 1, 0, 0, "alpha-a.b-c-somethinglong",
			"build.1-aef.1-its-okay"},
		{"1.0.0-rc.1+build.1", 1, 0, 0, "rc.1", "build.1"},
		{"2.0.0-rc.1+build.123", 2, 0, 0, "rc.1", "build.123"},
		{"1.2.3-beta", 1, 2, 3, "beta", ""},
		{"10.2.3-DEV-SNAPSHOT", 10, 2, 3, "DEV-SNAPSHOT", ""},
		{"1.2.3-SNAPSHOT-123", 1, 2, 3, "SNAPSHOT-123", ""},
		{"1.0.0", 1, 0, 0, "", ""},
		{"2.0.0", 2, 0, 0, "", ""},
		{"1.1.7", 1, 1, 7, "", ""},
		{"2.0.0+build.1848", 2, 0, 0, "", "build.1848"},
		{"2.0.1-alpha.1227", 2, 0, 1, "alpha.1227", ""},
		{"1.0.0-alpha+beta", 1, 0, 0, "alpha", "beta"},
		{"1.2.3----RC-SNAPSHOT.12.9.1--.12+788", 1, 2, 3, "---RC-SNAPSHOT.12.9.1--.12", "788"},
		{"1.2.3----R-S.12.9.1--.12+meta", 1, 2, 3, "---R-S.12.9.1--.12", "meta"},
		{"1.2.3----RC-SNAPSHOT.12.9.1--.12", 1, 2, 3, "---RC-SNAPSHOT.12.9.1--.12", ""},
		{"1.0.0+0.build.1-rc.10000aaa-kk-0.1", 1, 0, 0, "", "0.build.1-rc.10000aaa-kk-0.1"},
		{"1.0.0-0A.is.legal", 1, 0, 0, "0A.is.legal", ""},
	}
	for _, tt := range tests {
		t.Run(tt.versionString, func(t *testing.T) {
			have, _ := NewVersion(tt.versionString)
			if have.Major != tt.major {
				t.Errorf("Major: have=%d,want=%d", have.Major, tt.major)
			}
			if have.Minor != tt.minor {
				t.Errorf("Minor: have=%d,want=%d", have.Minor, tt.minor)
			}
			if have.Patch != tt.patch {
				t.Errorf("Patch: have=%d,want=%d", have.Patch, tt.patch)
			}
			if have.Prerelease != tt.prerelease {
				t.Errorf("Prerelease: have=%q,want=%q", have.Prerelease, tt.prerelease)
			}
			if have.Buildmetadata != tt.buildmetadata {
				t.Errorf("Buildmetadata: have=%q,want=%q", have.Buildmetadata, tt.buildmetadata)
			}
		})
	}
}

// TestVersion_bad tests for invalid version strings
func TestVersion_bad(t *testing.T) {
	testCases := []string{
		"2.1",
		"1",
		"1.2",
		"1.2.3-0123",
		"1.2.3-0123.0123",
		"1.1.2+.123",
		"+invalid",
		"-invalid",
		"-invalid+invalid",
		"-invalid.01",
		"alpha",
		"alpha.beta",
		"alpha.beta.1",
		"alpha.1",
		"alpha+beta",
		"alpha_beta",
		"alpha.",
		"alpha..",
		"beta",
		"1.0.0-alpha_beta",
		"-alpha.",
		"1.0.0-alpha..",
		"1.0.0-alpha..1",
		"1.0.0-alpha...1",
		"1.0.0-alpha....1",
		"1.0.0-alpha.....1",
		"1.0.0-alpha......1",
		"1.0.0-alpha.......1",
		"01.1.1",
		"1.01.1",
		"1.1.01",
		"1.2",
		"1.2.3.DEV",
		"1.2-SNAPSHOT",
		"1.2.31.2.3----RC-SNAPSHOT.12.09.1--..12+788",
		"1.2-RC-SNAPSHOT",
		"-1.0.3-gamma+b7718",
		"+justmeta",
		"9.8.7+meta+meta",
		"9.8.7-whatever+meta+meta",
		"99999999999999999999999.999999999999999999.99999999999999999----RC-SNAPSHOT.12.09.1",
		"--------------------------------..12",
	}
	for _, versionString := range testCases {
		t.Run(versionString, func(t *testing.T) {
			_, err := NewVersion(versionString)
			if err == nil {
				t.Errorf("%q should have been an invalid version string", versionString)
			}
		})
	}
}
