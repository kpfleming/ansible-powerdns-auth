from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Literal, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchResultComment")


@_attrs_define
class SearchResultComment:
    """
    Attributes:
        content (str | Unset):
        name (str | Unset):
        object_type (Literal['comment'] | Unset): set to "comment"
        zone_id (str | Unset):
        zone (str | Unset):
        type_ (str | Unset):
    """

    content: str | Unset = UNSET
    name: str | Unset = UNSET
    object_type: Literal["comment"] | Unset = UNSET
    zone_id: str | Unset = UNSET
    zone: str | Unset = UNSET
    type_: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        name = self.name

        object_type = self.object_type

        zone_id = self.zone_id

        zone = self.zone

        type_ = self.type_

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
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

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        content = d.pop("content", UNSET)

        name = d.pop("name", UNSET)

        object_type = cast("Literal['comment'] | Unset", d.pop("object_type", UNSET))
        if object_type != "comment" and not isinstance(object_type, Unset):
            raise ValueError(f"object_type must match const 'comment', got '{object_type}'")

        zone_id = d.pop("zone_id", UNSET)

        zone = d.pop("zone", UNSET)

        type_ = d.pop("type", UNSET)

        search_result_comment = cls(
            content=content,
            name=name,
            object_type=object_type,
            zone_id=zone_id,
            zone=zone,
            type_=type_,
        )

        return search_result_comment
