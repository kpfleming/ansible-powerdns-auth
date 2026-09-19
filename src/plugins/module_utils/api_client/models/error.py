from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="Error")


@_attrs_define
class Error:
    """Returned when the server encounters an error, either in client input or internally

    Attributes:
        error (str): A human readable error message
        errors (list[str] | Unset): Optional array of multiple errors encountered during processing
    """

    error: str
    errors: list[str] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        errors: list[str] | Unset = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
            }
        )
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        error = d.pop("error")

        errors = cast("list[str]", d.pop("errors", UNSET))

        error = cls(
            error=error,
            errors=errors,
        )

        return error
