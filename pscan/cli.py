from typing import Optional

import typer
from typing_extensions import Annotated

import socket
import threading
import concurrent.futures
from itertools import repeat

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
        timeout: Annotated[int, typer.Option(help="Set tcp connection timeout in miliseconds")] = 0,
        max_threads: Annotated[int, typer.Option(help="Specify the max number of threads for vanilla_scan")] = 4):
    if timeout != 0:
        timeout = .001 * timeout
        socket.setdefaulttimeout(timeout)

    if port != 0:
        typer.echo(f"Scanning {host}:{port}")
        test_connection(host, port)
    else:
        typer.echo("Starting vanilla scan")
        vanilla_scan(host, max_threads)

    return

def test_connection(host: str, port: int):
    try:
        s = socket.create_connection((host, port))
        s.close()
        typer.echo(f"Port: {port} is open")
    except:
        pass

def vanilla_scan(host: str, max_threads: int):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(test_connection, repeat(host), range(1, 2**16))
