"""
    List of all tests for entrypoint.py, using pytest framework.
"""

import os
import pytest # pylint: disable=import-error

def abs_path(executable):
    """Build manually (expected) executable absolute path"""
    return os.path.join(pytest.executables_folder, executable)

def test_entrypoint_executables(hook):
    """
    Basic test without configuration to check
    if entrypoint run each dogecoin executables.
    """
    ## Constant variable for test
    test_environ = {
        "DATADIR" : pytest.datadir,
        "USER" : pytest.user,
        "PATH" : pytest.PATH,
            }

    result_environ = {
        "USER" : pytest.user,
        "PATH" : pytest.PATH,
            }

    ## Test basic command with `dogecoind`
    test_args = ["dogecoind"]

    result_args = [
            abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-printtoconsole",
            ]
    hook.test(test_args, test_environ, result_args, result_environ)
    assert hook.result == hook.reference

    ## Test empty command with `dogecoin-cli`
    test_args = ["dogecoin-cli"]

    result_args = [
            abs_path("dogecoin-cli"),
            f"-datadir={pytest.datadir}",
            ]

    hook.test(test_args, test_environ, result_args, result_environ)
    assert hook.result == hook.reference

    ## Test basic command with `dogecoin-tx`
    tx_result_env = {
        "USER" : pytest.user,
        "PATH" : pytest.PATH,
        "DATADIR" : pytest.datadir,
            }

    test_args = ["dogecoin-tx"]

    result_args = [
            abs_path("dogecoin-tx"),
            ]
    hook.test(test_args, test_environ, result_args, tx_result_env)
    assert hook.result == hook.reference

def test_environment_vars(hook):
    """
    Verify if environment is converted to arguments,
    control that arguments are removed from the environment.
    """
    #Control environment variables with values
    test_args = ["dogecoind"]
    test_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            "DATADIR" : pytest.datadir,
            "MAXCONNECTIONS" : "150",
            "PAYTXFEE" : "0.01"
            }

    result_args = [
            abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-paytxfee=0.01",
            "-maxconnections=150",
            "-printtoconsole",
            ]
    result_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            }
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

    #Control environment variables with empty values
    test_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            "DATADIR" : pytest.datadir,
            "TESTNET" : "",
            "DAEMON" : "",
            }

    result_args = [
            abs_path("dogecoind"),
            "-daemon",
            f"-datadir={pytest.datadir}",
            "-testnet",
            "-printtoconsole",
            ]
    result_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            }
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

def test_arguments(hook):
    """Verifying arguments are being kept appropriatly"""
    #Verify arguments with values
    test_args = ["dogecoind", "-maxconnections=150", "-paytxfee=0.01"]
    test_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            "DATADIR" : pytest.datadir,
            }

    result_args = [
            abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-maxconnections=150",
            "-paytxfee=0.01",
            "-printtoconsole",
            ]
    result_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            }
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

    #Verify arguments without values
    test_args = ["dogecoind", "-daemon", "-testnet"]
    test_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            "DATADIR" : pytest.datadir,
            }

    result_args = [
            abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-daemon",
            "-testnet",
            "-printtoconsole",
            ]
    result_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            }
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

    #Mixing arguments with and without values
    test_args = ["dogecoind", "-daemon", "-maxconnections=150"]
    test_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            "DATADIR" : pytest.datadir,
            }

    result_args = [
            abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-daemon",
            "-maxconnections=150",
            "-printtoconsole",
            ]
    result_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            }
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

def test_arguments_double_dash(hook):
    """Check arguments formates with double-dash like `--testnet`"""
    test_args = ["dogecoind", "--maxconnections=150", "--paytxfee=0.01"]
    test_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            "DATADIR" : pytest.datadir,
            }

    result_args = [
            abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "--maxconnections=150",
            "--paytxfee=0.01",
            "-printtoconsole",
            ]
    result_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            }
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

def test_mixing_argument_and_env(hook):
    """Configure container with arguments and environment variables"""
    test_args = ["dogecoind", "-maxconnections=150", "-daemon"]
    test_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            "DATADIR" : pytest.datadir,
            "TESTNET" : "",
            }

    result_args = [
            abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-maxconnections=150",
            "-daemon",
            "-testnet",
            "-printtoconsole",
            ]
    result_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            }
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

def test_equal_argv_and_env(hook):
    """Check arguments and environment with identical variables"""
    test_args = ["dogecoind", "-maxconnections=150", "-daemon"]
    test_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            "DATADIR" : pytest.datadir,
            "MAXCONNECTIONS" : "150",
            "DAEMON" : "",
            }

    result_args = [
            abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-maxconnections=150",
            "-maxconnections=150",
            "-daemon",
            "-daemon",
            "-printtoconsole",
            ]
    result_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            }
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

    #Same variable with different value for env & arguments.
    test_args = ["dogecoind", "-maxconnections=130", "-daemon"]
    test_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            "DATADIR" : pytest.datadir,
            "MAXCONNECTIONS" : "150",
            "DAEMON" : "1",
            }

    result_args = [
            abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-maxconnections=130",
            "-maxconnections=150",
            "-daemon",
            "-daemon=1",
            "-printtoconsole",
            ]
    result_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            }
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

def test_help_debug(hook):
    """
    Test option with dash like `-help-debug` if working
    properly in environment.
    """
    test_args = ["dogecoind"]
    test_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            "DATADIR" : pytest.datadir,
            "HELP_DEBUG" : "",
            }

    result_args = [
            abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-help-debug",
            "-printtoconsole",
            ]
    result_env = {
            "USER" : pytest.user,
            "PATH" : pytest.PATH,
            }
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

def test_datadir(hook, host):
    """
    Verify if datadir can be changed and created proprely.

    Verify datadir metada, if it's owned by script user (dogecoin).
    """
    #Use a unique directory for this test
    tmp_datadir = "/tmp/datadir_test"
    datadir_argument = f"-datadir={tmp_datadir}"

    test_args = ["dogecoind", datadir_argument]
    test_environ = {
        "USER" : pytest.user,
        "PATH" : pytest.PATH,
            }

    result_args = [
            abs_path("dogecoind"),
            datadir_argument,
            "-printtoconsole",
            ]
    result_environ = {
        "USER" : pytest.user,
        "PATH" : pytest.PATH,
            }

    #Run test to generate datadir
    hook.test(test_args, test_environ, result_args, result_environ)
    assert hook.result == hook.reference

    #Test datadir metadata
    datadir_folder = host.file(tmp_datadir)
    assert datadir_folder.user == pytest.user
    assert datadir_folder.group == pytest.user
    assert datadir_folder.mode == 0o755
