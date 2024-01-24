from typing import Optional

import typer
from typing_extensions import Annotated

import socket
import threading
import time

from pscan import __app_name__, __version__

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.command()
def main(
        host: Annotated[str, typer.Argument(help="Host that you want to scan")],
        port: Annotated[int, typer.Option(help="Port that you want to scan")] = 0,
        timeout: Annotated[int, typer.Option(help="Set tcp connection timeout in miliseconds")] = 0):
    if timeout != 0:
        timeout = .001 * timeout
        socket.setdefaulttimeout(timeout)

    if port != 0:
        typer.echo(f"Scanning {host}:{port}")
        test_connection(host, port)
    else:
        typer.echo("Starting vanilla scan")
        vanilla_scan(host)

    return

def test_connection(host: str, port: int):
    try:
        s = socket.create_connection((host, port))
        s.close()
        typer.echo(f"Port: {port} is open")
    except:
        pass

def vanilla_scan(host: str):
    for port in range(1, 2**16):
        test_connection(host, port)
        
