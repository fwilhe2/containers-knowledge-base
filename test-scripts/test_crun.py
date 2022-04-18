import pytest
import subprocess
import json

def crun(args):
    command = ["crun"] + args
    print(command)
    output = subprocess.run(command, capture_output=True)
    stdout = output.stdout.decode("utf-8").rstrip()
    stderr = output.stderr.decode("utf-8").rstrip()
    return (stdout, stderr)

def test_crun_container_lifecycle():
    stdout, stderr = crun(['list', '--format=json'])
    parsed_stdout = json.loads(stdout)
    assert len(parsed_stdout) == 0
    assert stderr == ""

    stdout, stderr = crun(['create', '--console-socket=mySocket.sock', 'myContainer'])
    assert stdout == ""
    assert stderr == ""

    stdout, stderr = crun(['list', '--format=json'])
    parsed_stdout = json.loads(stdout)
    assert parsed_stdout[0]['id'] == 'myContainer'
    assert parsed_stdout[0]['status'] == 'created'
    assert stderr == ""

    stdout, stderr = crun(['start', 'myContainer'])
    assert stdout == ""
    assert stderr == ""

    stdout, stderr = crun(['list', '--format=json'])
    parsed_stdout = json.loads(stdout)
    assert parsed_stdout[0]['id'] == 'myContainer'
    assert parsed_stdout[0]['status'] == 'running'
    assert stderr == ""

    stdout, stderr = crun(['delete', '--force', 'myContainer'])
    assert stdout == ""
    assert stderr == ""

    stdout, stderr = crun(['list', '--format=json'])
    parsed_stdout = json.loads(stdout)
    assert len(parsed_stdout) == 0
    assert stderr == ""