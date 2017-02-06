from unittest import TestCase

from generalsio import _patch


class PatchTestCase(TestCase):

    def test_patch_example1(self):
        # Example 1: patching a diff of [1, 1, 3] onto [0, 0] yields [0, 3].
        old = [0, 0]
        new = [0, 3]
        diff = [1, 1, 3]
        self.assertEquals(_patch(old, diff), new)

    def test_patch_example2(self):
        # Example 2: patching a diff of [0, 1, 2, 1] onto [0, 0] yields [2, 0].
        old = [0, 0]
        new = [2, 0]
        diff = [0, 1, 2, 1]
        self.assertEquals(_patch(old, diff), new)

    def test_patch_start_change(self):
        old = [0, 0, 0, 0, 0, 0, 0, 0]
        new = [9, 9, 9, 0, 0, 0, 0, 0]
        diff = [0, 3, 9, 9, 9, 5]
        self.assertEquals(_patch(old, diff), new)

    def test_patch_ending_change(self):
        old = [0, 0, 0, 0, 0, 0, 0, 0]
        new = [0, 0, 0, 0, 0, 0, 0, 1]
        diff = [7, 1, 1]
        self.assertEquals(_patch(old, diff), new)

    def test_patch_two_changes(self):
        old = [0, 0, 0, 0, 0, 0, 0, 0]
        new = [0, 2, 5, 0, 0, 0, 3, 0]
        diff = [1, 2, 2, 5, 3, 1, 3, 1]
        self.assertEquals(_patch(old, diff), new)

    def test_patch_replace(self):
        old = [8, 8, 8, 8, 8, 8, 8, 8]
        new = [3, 3, 3, 3, 3, 3, 3, 3]
        diff = [0, 8, 3, 3, 3, 3, 3, 3, 3, 3]
        self.assertEquals(_patch(old, diff), new)

    def test_patch_same(self):
        old = [8, 8, 8, 8, 8, 8, 8, 8]
        new = [8, 8, 8, 8, 8, 8, 8, 8]
        diff = [8, 0]
        self.assertEquals(_patch(old, diff), new)

    def test_patch_same_half_pair(self):
        old = [8, 8, 8, 8, 8, 8, 8, 8]
        new = [8, 8, 8, 8, 8, 8, 8, 8]
        diff = [8]
        self.assertEquals(_patch(old, diff), new)


