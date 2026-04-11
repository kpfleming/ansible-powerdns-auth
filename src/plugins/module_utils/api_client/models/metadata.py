from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="Metadata")


@_attrs_define
class Metadata:
    """Represents zone metadata

    Attributes:
        kind (str | Unset): Name of the metadata
        metadata (list[str] | Unset): Array with all values for this metadata kind.
    """

    kind: str | Unset = UNSET
    metadata: list[str] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind

        metadata: list[str] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if kind is not UNSET:
            field_dict["kind"] = kind
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        kind = d.pop("kind", UNSET)

        metadata = cast("list[str]", d.pop("metadata", UNSET))

        return cls(
            kind=kind,
            metadata=metadata,
        )
