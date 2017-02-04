from unittest import TestCase

from pygeneralsio import patch


class PatchTestCase(TestCase):

    def test_patch_ex1(self):
        # Example 1: patching a diff of [1, 1, 3] onto [0, 0] yields [0, 3].
        self.assertEquals(patch([0, 0], [1, 1, 3]), [0, 3])

    def test_patch_ex2(self):
        # Example 2: patching a diff of [0, 1, 2, 1] onto [0, 0] yields [2, 0].
        self.assertEquals(patch([0, 0], [0, 1, 2, 1]), [2, 0])
