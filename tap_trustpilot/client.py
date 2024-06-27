"""REST client handling, including TrustpilotStream base class."""

from __future__ import annotations

import sys
from typing import Any, Callable, Iterable

import requests
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]

SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"


class TrustpilotStream(RESTStream):
    """Trustpilot stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.trustpilot.com/v1"
        

    records_jsonpath = "$.reviews[*]"

    # Set this value or override `get_new_paginator`.
    # next_page_token_jsonpath = "$.next_page"  # noqa: S105

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="apiKey",
            value=self.config.get("api_key", ""),
            location="header",
        )

    # @property
    # def http_headers(self) -> dict:
    #     """Return the http headers needed.

    #     Returns:
    #         A dictionary of HTTP headers.
    #     """
    #     headers = {}
    #     if "user_agent" in self.config:
    #         headers["User-Agent"] = self.config.get("user_agent")
    #     # If not using an authenticator, you may also provide inline auth headers:
    #     # headers["Private-Token"] = self.config.get("auth_token")  # noqa: ERA001
    #     return headers

    # def get_url_params(
    #     self,
    #     context: dict | None,  # noqa: ARG002
    #     next_page_token: Any | None,  # noqa: ANN401
    # ) -> dict[str, Any]:
    #     """Return a dictionary of values to be used in URL parameterization.

    #     Args:
    #         context: The stream context.
    #         next_page_token: The next page index or value.

    #     Returns:
    #         A dictionary of URL query parameters.
    #     """
    #     params: dict = {}
    #     if next_page_token:
    #         params["page"] = next_page_token
    #     if self.replication_key:
    #         params["sort"] = "asc"
    #         params["order_by"] = self.replication_key
    #     return params


    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

