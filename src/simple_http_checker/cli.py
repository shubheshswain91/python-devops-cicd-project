import logging
import click
from .checker import check_urls
from typing import Collection

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s]  %(levelname)-8s - %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@click.command()
@click.argument("urls", nargs=-1, required=True)
@click.option(
    "--timeout",
    default=5,
    show_default=True,
    help="Timeout in seconds for each request",
)
@click.option(
    "--verbose", "-v", is_flag=True, help="Enable debug logging"
)
def main(urls: Collection[str], timeout: int, verbose: bool):
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug(
            "Verbose mode enabled. Set logging level to DEBUG."
        )

    logger.debug(f"Received urls: {urls}")
    logger.debug(f"Received timeout: {timeout}")
    logger.debug(f"Received verbose {verbose}")

    if not urls:
        logger.warning("No URLs provided to check. Exiting.")
        click.echo("Usage: check-urls [OPTIONS] URLS...")
        return

    logger.info(
        f"Starting URL check for {len(urls)} URLs with timeout {timeout} seconds."
    )
    results = check_urls(urls, timeout)

    click.echo("URL Availability Check Results:")
    for url, status in results.items():
        if "OK" in status:
            fg_color = "green"
        else:
            fg_color = "red"
        click.secho(
            f"{url:<40} -> \033[92m{status}\033[0m", fg=fg_color
        )  # Green for OK
