import pytest
from entrypoint_hook import EntrypointHook, Command

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
