from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="CacheFlushResult")


@_attrs_define
class CacheFlushResult:
    """The result of a cache-flush

    Attributes:
        count (float | Unset): Amount of entries flushed
        result (str | Unset): A message about the result like "Flushed cache"
    """

    count: float | Unset = UNSET
    result: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        result = self.result

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        count = d.pop("count", UNSET)

        result = d.pop("result", UNSET)

        cache_flush_result = cls(
            count=count,
            result=result,
        )

        return cache_flush_result
