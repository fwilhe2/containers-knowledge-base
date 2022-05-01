import pytest
import subprocess
import json

def run_command(command):
    print(command)
    output = subprocess.run(command, capture_output=True, check=True)
    stdout = output.stdout.decode("utf-8").rstrip()
    stderr = output.stderr.decode("utf-8").rstrip()
    return (stdout, stderr)

@pytest.mark.parametrize("command,expected", [
    ('bwrap --version', 0),
    ('conmon --version', 0),
    ('containerd --version', 0),
    ('crio --version', 0),
    ('crun --version', 0),
    ('ignite version', 0),
    ('podman --version', 0),
    ('podman info', 0),
    ('rootlesskit --version', 0),
    ('runc --version', 0),
    ('runsc --version', 0),
    ('skopeo --version', 0),
])
def test_crun_container_lifecycle(command, expected):
    stdout, stderr = run_command(command.split(' '))
    assert stdout != ""
    assert stderr == ""
