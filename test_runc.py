import pytest
import subprocess
import json

def runc(args):
    command = ["runc"] + args
    print(command)
    output = subprocess.run(command, capture_output=True)
    stdout = output.stdout.decode("utf-8").rstrip()
    stderr = output.stderr.decode("utf-8").rstrip()
    return (stdout, stderr)

def test_runc_container_lifecycle():
    stdout, stderr = runc(['list', '--format=json'])
    parsed_stdout = json.loads(stdout)
    assert not parsed_stdout
    assert stderr == ""

    stdout, stderr = runc(['create', '--console-socket=mySocket.sock', 'myContainer'])
    assert stdout == ""
    assert stderr == ""

    stdout, stderr = runc(['list', '--format=json'])
    parsed_stdout = json.loads(stdout)
    assert parsed_stdout[0]['id'] == 'myContainer'
    assert parsed_stdout[0]['status'] == 'created'
    assert stderr == ""

    stdout, stderr = runc(['start', 'myContainer'])
    assert stdout == ""
    assert stderr == ""

    stdout, stderr = runc(['list', '--format=json'])
    parsed_stdout = json.loads(stdout)
    assert parsed_stdout[0]['id'] == 'myContainer'
    assert parsed_stdout[0]['status'] == 'stopped'
    assert stderr == ""

    stdout, stderr = runc(['delete', 'myContainer'])
    assert stdout == ""
    assert stderr == ""

    stdout, stderr = runc(['list', '--format=json'])
    parsed_stdout = json.loads(stdout)
    assert len(parsed_stdout) == 0
    assert stderr == ""