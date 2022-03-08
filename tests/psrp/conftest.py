import os
import typing as t

import pytest

import psrp


def which(program: str) -> t.Optional[str]:
    for path in os.environ.get("PATH", "").split(os.pathsep):
        exe = os.path.join(path, program)
        if os.path.isfile(exe) and os.access(exe, os.X_OK):
            return exe

    return None


PWSH_PATH = which("pwsh.exe" if os.name == "nt" else "pwsh")


@pytest.fixture(scope="function")
def psrp_proc() -> t.Iterator[psrp.ConnectionInfo]:
    if not PWSH_PATH:
        pytest.skip("Process integration test requires pwsh")

    yield psrp.ProcessInfo(executable=PWSH_PATH)


@pytest.fixture(scope="function")
def psrp_wsman() -> t.Iterator[psrp.ConnectionInfo]:
    server = os.environ.get("PYPSRP_SERVER", "server2019.domain.test")
    username = os.environ.get("PYPSRP_USERNAME", "vagrant-domain@DOMAIN.TEST")
    password = os.environ.get("PYPSRP_PASSWORD", "VagrantPass1")
    auth = os.environ.get("PYPSRP_AUTH", "negotiate")
    port = int(os.environ.get("PYPSRP_PORT", "5985"))

    if not server:
        pytest.skip("WSMan integration tests requires PYPSRP_SERVER to be defined")

    conn_info = psrp.WSManConnectionData(
        server=server,
        port=port,
        username=username,
        password=password,
        auth=auth,  # type: ignore[arg-type]
        encryption="never",
    )

    yield psrp.WSManInfo(conn_info)


@pytest.fixture(scope="function")
def psrp_ssh() -> t.Iterator[psrp.ConnectionInfo]:
    pytest.skip("TODO: Create SSH connection info")