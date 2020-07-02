import unittest

from semver.version import Version


class TestSemanticTestCases(unittest.TestCase):
    #   Test data taken from https://regex101.com/r/Ly7O1x/3/

    # GOOD STRINGS

    def test_0_0_4(self):
        version_string = '0.0.4'
        version = Version(version_string)
        self.assertEqual('0', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('4', version.patch)

    def test_1_2_3(self):
        version_string = '1.2.3'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('2', version.minor)
        self.assertEqual('3', version.patch)

    def test_10_20_30(self):
        version_string = '10.20.30'
        version = Version(version_string)
        self.assertEqual('10', version.major)
        self.assertEqual('20', version.minor)
        self.assertEqual('30', version.patch)

    def test_1_1_2_prerelease_meta(self):
        version_string = '1.1.2-prerelease+meta'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('1', version.minor)
        self.assertEqual('2', version.patch)
        self.assertEqual('prerelease', version.prerelease)
        self.assertEqual('meta', version.buildmetadata)

    def test_1_1_2_meta(self):
        version_string = '1.1.2+meta'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('1', version.minor)
        self.assertEqual('2', version.patch)
        self.assertEqual('meta', version.buildmetadata)

    def test_1_1_2_meta_valid(self):
        version_string = '1.1.2+meta-valid'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('1', version.minor)
        self.assertEqual('2', version.patch)
        self.assertEqual('meta-valid', version.buildmetadata)

    def test_1_0_0_alpha(self):
        version_string = '1.0.0-alpha'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('alpha', version.prerelease)

    def test_1_0_0_beta(self):
        version_string = '1.0.0-beta'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('0', version.patch)
        self.assertEqual('beta', version.prerelease)

    def test_1_0_0_alpha_beta(self):
        version_string = '1.0.0-alpha.beta'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('0', version.patch)
        self.assertEqual('alpha.beta', version.prerelease)

    def test_1_0_0_alpha_beta_1(self):
        version_string = '1.0.0-alpha.beta.1'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('0', version.patch)
        self.assertEqual('alpha.beta.1', version.prerelease)

    def test_1_0_0_alpha_1(self):
        version_string = '1.0.0-alpha.1'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('0', version.patch)
        self.assertEqual('alpha.1', version.prerelease)

    def test_1_0_0_alpha0_valid(self):
        version_string = '1.0.0-alpha0.valid'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('0', version.patch)
        self.assertEqual('alpha0.valid', version.prerelease)

    def test_1_0_0_alpha_0valid(self):
        version_string = '1.0.0-alpha.0valid'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('alpha.0valid', version.prerelease)

    def test_1_0_0_alpha_a_b_c_somethinglong_build_1_aef_1_its_okay(self):
        version_string = '1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('0', version.patch)
        self.assertEqual('alpha-a.b-c-somethinglong', version.prerelease)
        self.assertEqual('build.1-aef.1-its-okay', version.buildmetadata)

    def test_1_0_0_rc_1_build_1(self):
        version_string = '1.0.0-rc.1+build.1'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('0', version.patch)
        self.assertEqual('rc.1', version.prerelease)
        self.assertEqual('build.1', version.buildmetadata)

    def test_2_0_0_rc_1_build_123(self):
        version_string = '2.0.0-rc.1+build.123'
        version = Version(version_string)
        self.assertEqual('2', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('0', version.patch)
        self.assertEqual('rc.1', version.prerelease)
        self.assertEqual('build.123', version.buildmetadata)

    def test_1_2_3_beta(self):
        version_string = '1.2.3-beta'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('2', version.minor)
        self.assertEqual('3', version.patch)
        self.assertEqual('beta', version.prerelease)

    def test_10_2_3_DEV_SNAPSHOT(self):
        version_string = '10.2.3-DEV-SNAPSHOT'
        version = Version(version_string)
        self.assertEqual('10', version.major)
        self.assertEqual('2', version.minor)
        self.assertEqual('3', version.patch)
        self.assertEqual('DEV-SNAPSHOT', version.prerelease)

    def test_1_2_3_SNAPSHOT_123(self):
        version_string = '1.2.3-SNAPSHOT-123'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('2', version.minor)
        self.assertEqual('3', version.patch)
        self.assertEqual('SNAPSHOT-123', version.prerelease)

    def test_1_0_0(self):
        version_string = '1.0.0'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('0', version.patch)

    def test_2_0_0(self):
        version_string = '2.0.0'
        version = Version(version_string)
        self.assertEqual('2', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('0', version.patch)

    def test_1_1_7(self):
        version_string = '1.1.7'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('1', version.minor)
        self.assertEqual('7', version.patch)

    def test_2_0_0_build_1848(self):
        version_string = '2.0.0+build.1848'
        version = Version(version_string)
        self.assertEqual('2', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('0', version.patch)
        self.assertEqual('build.1848', version.buildmetadata)

    def test_2_0_1_alpha_1227(self):
        version_string = '2.0.1-alpha.1227'
        version = Version(version_string)
        self.assertEqual('2', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('1', version.patch)
        self.assertEqual('alpha.1227', version.prerelease)

    def test_1_0_0_alpha_beta2(self):
        version_string = '1.0.0-alpha+beta'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('0', version.patch)
        self.assertEqual('alpha', version.prerelease)
        self.assertEqual('beta', version.buildmetadata)

    def test_1_2_3____RC_SNAPSHOT_12_9_1___12_788(self):
        version_string = '1.2.3----RC-SNAPSHOT.12.9.1--.12+788'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('2', version.minor)
        self.assertEqual('3', version.patch)
        self.assertEqual('---RC-SNAPSHOT.12.9.1--.12', version.prerelease)
        self.assertEqual('788', version.buildmetadata)

    def test_1_2_3____R_S_12_9_1___12_meta(self):
        version_string = '1.2.3----R-S.12.9.1--.12+meta'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('2', version.minor)
        self.assertEqual('3', version.patch)
        self.assertEqual('---R-S.12.9.1--.12', version.prerelease)
        self.assertEqual('meta', version.buildmetadata)

    def test_1_2_3____RC_SNAPSHOT_12_9_1___12(self):
        version_string = '1.2.3----RC-SNAPSHOT.12.9.1--.12'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('2', version.minor)
        self.assertEqual('3', version.patch)
        self.assertEqual('---RC-SNAPSHOT.12.9.1--.12', version.prerelease)

    def test_1_0_0_0_build_1_rc_10000aaa_kk_0_1(self):
        version_string = '1.0.0+0.build.1-rc.10000aaa-kk-0.1'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('0', version.patch)
        self.assertEqual('0.build.1-rc.10000aaa-kk-0.1', version.buildmetadata)

    def test_99999999999999999999999_999999999999999999_99999999999999999(self):
        version_string = '99999999999999999999999.999999999999999999.99999999999999999'
        version = Version(version_string)
        self.assertEqual('99999999999999999999999', version.major)
        self.assertEqual('999999999999999999', version.minor)
        self.assertEqual('99999999999999999', version.patch)

    def test_1_0_0_0A_is_legal(self):
        version_string = '1.0.0-0A.is.legal'
        version = Version(version_string)
        self.assertEqual('1', version.major)
        self.assertEqual('0', version.minor)
        self.assertEqual('0', version.patch)
        self.assertEqual('0A.is.legal', version.prerelease)

    # BAD_STRINGS

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            Version('2.1')

    def test_1(self):
        with self.assertRaises(ValueError):
            Version('1')

    def test_1_2(self):
        with self.assertRaises(ValueError):
            Version('1.2')

    def test_1_2_3_0123(self):
        with self.assertRaises(ValueError):
            Version('1.2.3-0123')

    def test_1_2_3_0123_0123(self):
        with self.assertRaises(ValueError):
            Version('1.2.3-0123.0123')

    def test_1_1_2__123(self):
        with self.assertRaises(ValueError):
            Version('1.1.2+.123')

    def test__invalid(self):
        with self.assertRaises(ValueError):
            Version('+invalid')

    def test__invalid(self):
        with self.assertRaises(ValueError):
            Version('-invalid')

    def test__invalid_invalid(self):
        with self.assertRaises(ValueError):
            Version('-invalid+invalid')

    def test__invalid_01(self):
        with self.assertRaises(ValueError):
            Version('-invalid.01')

    def test_alpha(self):
        with self.assertRaises(ValueError):
            Version('alpha')

    def test_alpha_beta(self):
        with self.assertRaises(ValueError):
            Version('alpha.beta')

    def test_alpha_beta_1(self):
        with self.assertRaises(ValueError):
            Version('alpha.beta.1')

    def test_alpha_1(self):
        with self.assertRaises(ValueError):
            Version('alpha.1')

    def test_alpha_beta(self):
        with self.assertRaises(ValueError):
            Version('alpha+beta')

    def test_alpha_beta(self):
        with self.assertRaises(ValueError):
            Version('alpha_beta')

    def test_alpha_(self):
        with self.assertRaises(ValueError):
            Version('alpha.')

    def test_alpha__(self):
        with self.assertRaises(ValueError):
            Version('alpha..')

    def test_beta(self):
        with self.assertRaises(ValueError):
            Version('beta')

    def test_1_0_0_alpha_beta(self):
        with self.assertRaises(ValueError):
            Version('1.0.0-alpha_beta')

    def test__alpha_(self):
        with self.assertRaises(ValueError):
            Version('-alpha.')

    def test_1_0_0_alpha__(self):
        with self.assertRaises(ValueError):
            Version('1.0.0-alpha..')

    def test_1_0_0_alpha__1(self):
        with self.assertRaises(ValueError):
            Version('1.0.0-alpha..1')

    def test_1_0_0_alpha___1(self):
        with self.assertRaises(ValueError):
            Version('1.0.0-alpha...1')

    def test_1_0_0_alpha____1(self):
        with self.assertRaises(ValueError):
            Version('1.0.0-alpha....1')

    def test_1_0_0_alpha_____1(self):
        with self.assertRaises(ValueError):
            Version('1.0.0-alpha.....1')

    def test_1_0_0_alpha______1(self):
        with self.assertRaises(ValueError):
            Version('1.0.0-alpha......1')

    def test_1_0_0_alpha_______1(self):
        with self.assertRaises(ValueError):
            Version('1.0.0-alpha.......1')

    def test_01_1_1(self):
        with self.assertRaises(ValueError):
            Version('01.1.1')

    def test_1_01_1(self):
        with self.assertRaises(ValueError):
            Version('1.01.1')

    def test_1_1_01(self):
        with self.assertRaises(ValueError):
            Version('1.1.01')

    def test_1_2(self):
        with self.assertRaises(ValueError):
            Version('1.2')

    def test_1_2_3_DEV(self):
        with self.assertRaises(ValueError):
            Version('1.2.3.DEV')

    def test_1_2_SNAPSHOT(self):
        with self.assertRaises(ValueError):
            Version('1.2-SNAPSHOT')

    def test_1_2_31_2_3____RC_SNAPSHOT_12_09_1____12_788(self):
        with self.assertRaises(ValueError):
            Version('1.2.31.2.3----RC-SNAPSHOT.12.09.1--..12+788')

    def test_1_2_RC_SNAPSHOT(self):
        with self.assertRaises(ValueError):
            Version('1.2-RC-SNAPSHOT')

    def test__1_0_3_gamma_b7718(self):
        with self.assertRaises(ValueError):
            Version('-1.0.3-gamma+b7718')

    def test__justmeta(self):
        with self.assertRaises(ValueError):
            Version('+justmeta')

    def test_9_8_7_meta_meta(self):
        with self.assertRaises(ValueError):
            Version('9.8.7+meta+meta')

    def test_9_8_7_whatever_meta_meta(self):
        with self.assertRaises(ValueError):
            Version('9.8.7-whatever+meta+meta')

    def test_99999999999999999999999_999999999999999999_99999999999999999____RC_SNAPSHOT_12_09_1__________________________________12(
            self):
        with self.assertRaises(ValueError):
            Version(
                '99999999999999999999999.999999999999999999.99999999999999999----RC-SNAPSHOT.12.09.1--------------------------------..12')
