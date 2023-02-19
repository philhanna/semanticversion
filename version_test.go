package semver

import (
	"testing"
)

func TestNewVersion(t *testing.T) {
	tests := []struct {
		versionString string
		want          Version
		isGood        bool
	}{
		{"bad", Version{}, false},
		{"1.0.0-alpha", Version{
			Major:         1,
			Minor:         0,
			Patch:         0,
			Prerelease:    "alpha",
			Buildmetadata: "",
		}, true},
	}
	for _, tt := range tests {
		// For convenience, all tests are named after their version
		// string
		name := tt.versionString
		t.Run(name, func(t *testing.T) {
			have, err := NewVersion(tt.versionString)
			if err == nil && !tt.isGood {
				t.Errorf("%s should have failed. have=%s", name, have)
			}
			if err != nil && tt.isGood {
				t.Errorf("%s failed but shouldn't have. have=%s", name, have)
			}
			want := tt.want
			if have != want {
				t.Errorf("have=%s,want=%v\n", have, want)
			}
		})
	}
}
