from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="Record")


@_attrs_define
class Record:
    """The RREntry object represents a single record.

    Attributes:
        content (str): The content of this record
        disabled (bool | Unset): Whether or not this record is disabled. When unset, the record is not disabled
    """

    content: str
    disabled: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        disabled = self.disabled

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "content": content,
            }
        )
        if disabled is not UNSET:
            field_dict["disabled"] = disabled

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        content = d.pop("content")

        disabled = d.pop("disabled", UNSET)

        record = cls(
            content=content,
            disabled=disabled,
        )

        return record
