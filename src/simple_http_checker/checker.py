import logging
import requests
from typing import Collection

logger = logging.getLogger(__name__)




def check_urls(
    urls: Collection[str], timeout: int = 5
) -> dict[str, bool]:
    """
    Check the availability of a list of URLs.

    Args:
        urls (list[str]): A list of URLs to check.
        timeout (int): Timeout for each request in seconds.

    Returns:
        dict[str, bool]: A dictionary mapping each URL to its availability status.
    """
    logger.info(
        f"Starting URL availability check for {len(urls)} URLs with a timeout of {timeout} seconds."
    )
    results: dict[str, str] = {}
    for url in urls:
        try:
            logger.debug(f"Checking URL: {url}")
            response = requests.get(url, timeout=timeout)
            if response.ok:
                status = f"{response.status_code} OK"
            else:
                status = (
                    f"{response.status_code} {response.reason}"
                )

        except requests.exceptions.Timeout:
            status = "TIMEOUT"
            logger.warning(f"Request to {url} timed out.")
        except requests.exceptions.ConnectionError:
            status = "CONNECTION_ERROR"
            logger.warning(
                f"Connection error occurred while trying to reach {url}."
            )
        except requests.exceptions.RequestException as e:
            status = f"REQUEST_ERROR {type(e).__name__}"
            logger.error(
                f"An error occurred while requesting {url}: {e}",
                exc_info=True,
            )

        results[url] = status
        logger.debug(f"Checked URL: {url:<40} -> {status}")

    logger.info("Completed URL availability check.")
    return results
