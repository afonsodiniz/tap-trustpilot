"""Trustpilot tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_trustpilot import streams


class TapTrustpilot(Tap):
    """Trustpilot tap class."""

    name = "tap-trustpilot"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.trustpilot.com/v1",
            description="The url for the API service",
        ),
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The key to authenticate against the API service",
        )
    ).to_dict()

    def discover_streams(self) -> list[streams.TrustpilotStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.Reviews(self)
        ]


if __name__ == "__main__":
    TapTrustpilot.cli()
