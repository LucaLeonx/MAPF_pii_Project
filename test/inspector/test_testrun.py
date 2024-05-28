import pytest

import globals


class TestTestRun:
    def test_from_dict(self):
        assert globals.test_run().name == "Test1"
