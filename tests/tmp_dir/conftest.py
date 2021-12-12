"""
    Pytest configuration file for tests fixtures and global variables.

    Pytest fixtures are used to arrange and clean up tests environment.
    See: https://docs.pytest.org/en/6.2.x/fixture.html
"""

import os
import tempfile
import pytest # pylint: disable=import-error
from entrypoint_hook import EntrypointHook, Command

def pytest_configure():
    """Declare global variables to use across tests"""
    #User used for tests
    pytest.user = os.environ["USER"]

    #Perform tests in a temporary directory, used as datadir
    pytest.directory = tempfile.TemporaryDirectory()
    pytest.datadir = pytest.directory.name

    #PATH environment variable is changed during tests,
    #keep a fixed value this way
    pytest.PATH = os.environ["PATH"]
    pytest.executables_folder = "/usr/local/bin"

@pytest.fixture
def hook():
    """
    Prepare & cleanup EntrypointHook for tests.
    Enable/disable entrypoint system calls.
    """
    test_hook = EntrypointHook()
    yield test_hook
    test_hook.reset_hooks()

def pytest_assertrepr_compare(left, right):
    """Override error messages of AssertionError on test failure."""
    #Display comparison of result command and an expected execve command.
    if isinstance(left, Command) and isinstance(right, Command):
        assert_msg = ["fail"]
        assert_msg.append("======= Result =======")
        assert_msg.extend(str(left).splitlines())
        assert_msg.append("======= Expected =======")
        assert_msg.extend(str(right).splitlines())
        assert_msg.append("======= Diff =======")
        assert_msg.extend(left.diff(right))
        return assert_msg
    return None
