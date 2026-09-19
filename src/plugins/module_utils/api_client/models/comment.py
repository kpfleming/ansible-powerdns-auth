from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="Comment")


@_attrs_define
class Comment:
    """A comment about an RRSet.

    Attributes:
        content (str | Unset): The actual comment
        account (str | Unset): Name of an account that added the comment
        modified_at (int | Unset): Timestamp of the last change to the comment
    """

    content: str | Unset = UNSET
    account: str | Unset = UNSET
    modified_at: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        account = self.account

        modified_at = self.modified_at

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if account is not UNSET:
            field_dict["account"] = account
        if modified_at is not UNSET:
            field_dict["modified_at"] = modified_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        content = d.pop("content", UNSET)

        account = d.pop("account", UNSET)

        modified_at = d.pop("modified_at", UNSET)

        comment = cls(
            content=content,
            account=account,
            modified_at=modified_at,
        )

        return comment
