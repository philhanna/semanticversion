// A semantic versioned version class
//
// See https://semver.org for a normative description of
// semantic versioning.
//
// The basic structure of a semantic version is major.minor.patch,
// where each component is an integer with no leading zeros.
// These three components are all required.
//
// A semantic version may also contain:
// - A prerelase component, which follows the first '-' and ends
// at the first '+', if any
// - A buildmetadata component, which follows the first '+'
// Both of these are optional.
//
// A change in the major version means that backwards incompatible
// changes have been introduced into the public API.  When the
// major version changes, the minor and patch versions must be
// reset to zero.
//
// A change in the minor version means that backwards compatible
// functionality has been added to the public API.  When the minor
// version changes, the patch version must be reset to zero.
//
// A change in the patch version means that backwards compatible
// bug fixes have been introduced.
//
// See the official documentation for a description of the
// prerelease and buildmetadata components.
//
// Semantic versions have a strict ordering; that is, any two
// are comparable according to a set of rules:
//
// 1. Precedence MUST be calculated by separating the version into
// major, minor, patch and pre-release identifiers in that order (Build
// metadata does not figure into precedence).
//
// 2. Precedence is determined by the first difference when comparing
// each of these identifiers from left to right as follows: Major,
// minor, and patch versions are always compared numerically.
//
// Example: 1.0.0 < 2.0.0 < 2.1.0 < 2.1.1.
//
// 3. When major, minor, and patch are equal, a pre-release version has
// lower precedence than a normal version:
//
// Example: 1.0.0-alpha < 1.0.0.
//
// 4. Precedence for two pre-release versions with the same major,
// minor, and patch version MUST be determined by comparing each dot
// separated identifier from left to right until a difference is found
// as follows:
//
//   - Identifiers consisting of only digits are compared numerically.
//
//   - Identifiers with letters or hyphens are compared lexically in
//     ASCII sort order.
//
//   - Numeric identifiers always have lower precedence than
//     non-numeric identifiers.
//
//   - A larger set of pre-release fields has a higher precedence
//     than a smaller set, if all of the preceding identifiers are
//     equal.
//
//     Example: 1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta
//     < 1.0.0-beta < 1.0.0-beta.2 < 1.0.0-beta.11
//     < 1.0.0-rc.1 < 1.0.0.
//
// See https://regex101.com/r/Ly7O1x/3/ for the regular expression used
// to parse the version string.
package semver

import (
	"errors"
	"fmt"
	"regexp"
	"strings"
)

// ---------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------

// Version contains the parsed components of a version string.
type Version struct {
	Major string
	Minor string
	Patch string
	Prerelease string
	Buildmetadata string
}

// ---------------------------------------------------------------------
// Constructors
// ---------------------------------------------------------------------

// NewVersion parses a version string and returns a new Version from it.
func NewVersion(vs string) (Version, error) {
	p := new(Version)
	reParts := []string{
		`^`,
		`v?`,
		`(?P<major>0|[1-9]\d*)`,
		`\.`,
		`(?P<minor>0|[1-9]\d*)`,
		`\.`,
		`(?P<patch>0|[1-9]\d*)`,
		`(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+`,
		`(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$`,
		}
	reString := strings.Join(reParts, "")
	re := regexp.MustCompile(reString)
	tokens := re.FindStringSubmatch(vs)
	if tokens == nil {
		return Version{}, errors.New("Invalid version string")
	}
	p.Major = tokens[1]
	p.Minor = tokens[2]
	p.Patch = tokens[3]
	p.Prerelease = tokens[4]
	p.Buildmetadata = tokens[5]

	return *p, nil
}

// String returns a string representation of this Version
func (v Version) String() string {
	parts := []string{
		fmt.Sprintf("Major: %q", v.Major),
		fmt.Sprintf("Minor: %q", v.Minor),
		fmt.Sprintf("Patch: %q", v.Patch),
		fmt.Sprintf("Prerelease: %q", v.Prerelease),
		fmt.Sprintf("Buildmetadata: %q", v.Buildmetadata),
	}
	s := "Version(" + strings.Join(parts, ", ") + ")"
	return s
}