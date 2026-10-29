#!/usr/bin/env python
"""Server startup script."""

import click
from waitress import serve

from autonumber.wsgi import application


@click.command()
@click.option(
    '--listen',
    default='0.0.0.0:3000',
    help='Address and port to listen on. Default is "0.0.0.0:3000".',
    metavar='[ADDRESS]:PORT',
)
@click.option(
    '--url-scheme',
    envvar='URL_SCHEME',
    type=click.Choice(['http', 'https']),
    default='http',
    show_default=True,
    help='Public URL scheme used by the application.',
)
def run(listen: str, url_scheme: str):
    serve(application, listen=listen, threads=8, url_scheme=url_scheme)
