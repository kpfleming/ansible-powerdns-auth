from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Literal, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchResultRecord")


@_attrs_define
class SearchResultRecord:
    """
    Attributes:
        content (str | Unset):
        disabled (bool | Unset):
        name (str | Unset):
        object_type (Literal['record'] | Unset): set to "record"
        zone_id (str | Unset):
        zone (str | Unset):
        type_ (str | Unset):
        ttl (int | Unset):
    """

    content: str | Unset = UNSET
    disabled: bool | Unset = UNSET
    name: str | Unset = UNSET
    object_type: Literal["record"] | Unset = UNSET
    zone_id: str | Unset = UNSET
    zone: str | Unset = UNSET
    type_: str | Unset = UNSET
    ttl: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        disabled = self.disabled

        name = self.name

        object_type = self.object_type

        zone_id = self.zone_id

        zone = self.zone

        type_ = self.type_

        ttl = self.ttl

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if name is not UNSET:
            field_dict["name"] = name
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if zone_id is not UNSET:
            field_dict["zone_id"] = zone_id
        if zone is not UNSET:
            field_dict["zone"] = zone
        if type_ is not UNSET:
            field_dict["type"] = type_
        if ttl is not UNSET:
            field_dict["ttl"] = ttl

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        content = d.pop("content", UNSET)

        disabled = d.pop("disabled", UNSET)

        name = d.pop("name", UNSET)

        object_type = cast("Literal['record'] | Unset", d.pop("object_type", UNSET))
        if object_type != "record" and not isinstance(object_type, Unset):
            raise ValueError(f"object_type must match const 'record', got '{object_type}'")

        zone_id = d.pop("zone_id", UNSET)

        zone = d.pop("zone", UNSET)

        type_ = d.pop("type", UNSET)

        ttl = d.pop("ttl", UNSET)

        search_result_record = cls(
            content=content,
            disabled=disabled,
            name=name,
            object_type=object_type,
            zone_id=zone_id,
            zone=zone,
            type_=type_,
            ttl=ttl,
        )

        return search_result_record
