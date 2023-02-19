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
	"strconv"
	"strings"
)

// ---------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------

// Version contains the parsed components of a version string.
type Version struct {
	Major         int
	Minor         int
	Patch         int
	Prerelease    string
	Buildmetadata string
	VersionString string
}

// ---------------------------------------------------------------------
// Constructors
// ---------------------------------------------------------------------

// NewVersion parses a version string and returns a new Version from it.
//
// NOTE: The regular expression defined at https://semver.org does not
// include a leading "v", but this constructor does, for convenience in
// working with Go best practices.
func NewVersion(vs string) (Version, error) {
	p := new(Version)
	p.VersionString = vs
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
		errmsg := fmt.Sprintf("Invalid version string: %s", vs)
		return Version{}, errors.New(errmsg)
	}

	// Populate the structure
	p.Major, _ = strconv.Atoi(tokens[1])
	p.Minor, _ = strconv.Atoi(tokens[2])
	p.Patch, _ = strconv.Atoi(tokens[3])
	p.Prerelease = tokens[4]
	p.Buildmetadata = tokens[5]

	return *p, nil
}

// ---------------------------------------------------------------------
// Methods
// ---------------------------------------------------------------------

// Compare compares two versions and returns -1, 0, or 1, depending on
// whether this version is less than, equal to, or greater than the
// other version. The comparisons are done according to Section 11 of
// the specification.
//
// Note that build metadata is NOT considered in precedence comparisons,
// according to the specification.

func (self Version) Compare(other Version) int {
	switch {
	case self.Major < other.Major:
		return -1
	case self.Major > other.Major:
		return 1
	case self.Minor < other.Minor:
		return -1
	case self.Minor > other.Minor:
		return 1
	case self.Patch < other.Patch:
		return -1
	case self.Patch > other.Patch:
		return 1
	}

	// At this point, we know the three primary components are equal.

	// 11.3 A pre-release version has lower precedence than a normal
	// version

	if self.Prerelease == "" && other.Prerelease == "" {
		return 0
	}
	if self.Prerelease != "" && other.Prerelease == "" {
		return -1
	}
	if self.Prerelease == "" && other.Prerelease != "" {
		return 1
	}

	// 11.4 - Precedence for two pre-release versions with the same
	// major, minor, and patch must be determined by comparing each
	// dot-separated identifier from left to right until a difference is
	// found

	theseFields := strings.Split(self.Prerelease, ".")
	thoseFields := strings.Split(other.Prerelease, ".")

	// Need to make these two lists the same length for joint iteration
	for len(theseFields) < len(thoseFields) {
		theseFields = append(theseFields, "")
	}
	for len(theseFields) > len(thoseFields) {
		thoseFields = append(thoseFields, "")
	}

	for i := range theseFields {
		this := theseFields[i]
		that := thoseFields[i]

		// 11.4.4 Longer sets are greater than shorter sets
		if this == "" && that != "" {
			return -1
		}
		if this != "" && that == "" {
			return 1
		}

		if this != "" && that != "" {
			// 11.4.1 Integers are compared numerically
			if isNumeric(this) && isNumeric(that) {
				intthis, _ := strconv.Atoi(this)
				intthat, _ := strconv.Atoi(that)
				if intthis < intthat {
					return -1
				}
				if intthis > intthat {
					return 1
				}
			}
			// 11.4.3 Numerics are always less than non-numerics
			if isNumeric(this) && !isNumeric(that) {
				return -1
			}
			if !isNumeric(this) && isNumeric(that) {
				return 1
			}
			// 11.4.2 Nonnumeric fields are compared lexicographically
			if this < that {
				return -1
			}
			if this > that {
				return 1
			}
		}
	}

	// Welp, they must be equal
	return 0
}

// String returns a string representation of this Version
func (v Version) String() string {
	parts := []string{
		fmt.Sprintf("Major: %d", v.Major),
		fmt.Sprintf("Minor: %d", v.Minor),
		fmt.Sprintf("Patch: %d", v.Patch),
		fmt.Sprintf("Prerelease: %q", v.Prerelease),
		fmt.Sprintf("Buildmetadata: %q", v.Buildmetadata),
	}
	s := "Version{" + strings.Join(parts, ", ") + "}"
	return s
}

// ---------------------------------------------------------------------
// Functions
// ---------------------------------------------------------------------

// isNumeric returns true if the string is composed entirely of digits
func isNumeric(s string) bool {
	for _, ch := range s {
		if ch >= '0' && ch <= '9' {
			continue
		}
		return false
	}
	return true
}
