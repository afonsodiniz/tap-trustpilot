"""Stream type classes for tap-trustpilot."""

from __future__ import annotations

import sys
import typing as t

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_trustpilot.client import TrustpilotStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"

class Reviews(TrustpilotStream):
    """Stream for Reviews endpoint"""

    name = "reviews"
    path = "/business-units/64675b1c8598295b662c37f2/all-reviews"
    primary_keys = ["id"]

    schema_filepath = SCHEMAS_DIR / "reviews.json" 


