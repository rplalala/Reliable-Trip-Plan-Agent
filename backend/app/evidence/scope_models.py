"""Shared subject scopes for requested and source-supported official facts."""

from enum import StrEnum


class SubjectScope(StrEnum):
    WHOLE_VENUE = "whole_venue"
    SUB_AREA = "sub_area"
    EXHIBITION = "exhibition"
    TICKET_PRODUCT = "ticket_product"
    UNKNOWN = "unknown"
