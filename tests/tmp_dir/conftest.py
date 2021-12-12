import pytest
import os
import tempfile
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
    test_hook._reset_hooks()

def pytest_assertrepr_compare(op, left, right):
    """Override error messages of AssertionError on test failure."""
    #Display comparison of result command and an expected execve command.
    if type(left) is Command and type(right) is Command:
        assert_msg = ["fail"]
        assert_msg.append("======= Result =======")
        assert_msg.extend(str(left).splitlines())
        assert_msg.append("======= Expected =======")
        assert_msg.extend(str(right).splitlines())
        assert_msg.append("======= Diff =======")
        assert_msg.extend(left.diff(right))
        return assert_msg
