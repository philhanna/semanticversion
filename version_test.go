package semver

import (
	"testing"
)

func TestNewVersion(t *testing.T) {
	tests := []struct {
		name          string
		want          Version
		wantErr       bool
	}{
		{"1.0.0-alpha", Version{
			Major: "1",
			Minor: "0",
			Patch: "0",
			Prerelease: "alpha",
			Buildmetadata: "",
		}, true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			have, _ := NewVersion(tt.name)
			want := tt.want
			if have != want {
				t.Errorf("have=%s,want=%v\n", have, want)
			}
		})
	}
}
