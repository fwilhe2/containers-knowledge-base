import pytest
import subprocess

def run_command(command):
    print(command)
    # check=True already fails the test on a non-zero exit status.
    output = subprocess.run(command, capture_output=True, check=True)
    stdout = output.stdout.decode("utf-8").rstrip()
    stderr = output.stderr.decode("utf-8").rstrip()
    return (stdout, stderr)

@pytest.mark.parametrize("command", [
    'bwrap --version',
    'conmon --version',
    'containerd --version',
    'crio --version',
    'crun --version',
    'ctop -v',
    'flintlockd version',
    'ignite version',
    'podman --version',
    'podman info',
    'rootlesskit --version',
    'runc --version',
    # 'runsc --version',
    'skopeo --version',
    # podman 5 networking. netavark and aardvark-dns install into
    # libexec/podman, which is deliberately not on PATH.
    '/usr/local/libexec/podman/netavark --version',
    '/usr/local/libexec/podman/aardvark-dns --version',
    'pasta --version',
])
def test_tool_runs_and_reports_itself(command):
    # Deliberately not asserting that stderr is empty: plenty of these write
    # informational lines there, and doing so made `podman info` fail purely
    # because it warned about the cgroup manager.
    stdout, _ = run_command(command.split(' '))
    assert stdout != ""
