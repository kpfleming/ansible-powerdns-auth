from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="Views")


@_attrs_define
class Views:
    """
    Attributes:
        views (list[str] | Unset): An array of view names
    """

    views: list[str] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        views: list[str] | Unset = UNSET
        if not isinstance(self.views, Unset):
            views = self.views

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if views is not UNSET:
            field_dict["views"] = views

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        views = cast("list[str]", d.pop("views", UNSET))

        return cls(
            views=views,
        )
