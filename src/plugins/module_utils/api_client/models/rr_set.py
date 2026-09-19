from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.comment import Comment
    from ..models.record import Record


T = TypeVar("T", bound="RRSet")


@_attrs_define
class RRSet:
    """This represents a Resource Record Set (all records with the same name and type).

    Attributes:
        name (str): Name for record set (e.g. “www.powerdns.com.”)
        type_ (str): Type of this record (e.g. “A”, “PTR”, “MX”)
        ttl (int): DNS TTL of the records, in seconds. MUST NOT be included when changetype is set to “DELETE”.
        records (list[Record]): All records in this RRSet. When updating Records, this is the list of new records
            (replacing the old ones). Must be empty when changetype is set to DELETE. An empty list results in deletion of
            all records (and comments).
        changetype (str | Unset): MUST be added when updating the RRSet. Must be REPLACE or DELETE. With DELETE, all
            existing RRs matching name and type will be deleted, including all comments. With REPLACE: when records is
            present, all existing RRs matching name and type will be deleted, and then new records given in records will be
            created. If no records are left, any existing comments will be deleted as well. When comments is present, all
            existing comments for the RRs matching name and type will be deleted, and then new comments given in comments
            will be created.
        comments (list[Comment] | Unset): List of Comment. Must be empty when changetype is set to DELETE. An empty list
            results in deletion of all comments. modified_at is optional and defaults to the current server time.
    """

    name: str
    type_: str
    ttl: int
    records: list[Record]
    changetype: str | Unset = UNSET
    comments: list[Comment] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.comment import Comment
        from ..models.record import Record

        name = self.name

        type_ = self.type_

        ttl = self.ttl

        records = []
        for records_item_data in self.records:
            records_item = records_item_data.to_dict()
            records.append(records_item)

        changetype = self.changetype

        comments: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.comments, Unset):
            comments = []
            for comments_item_data in self.comments:
                comments_item = comments_item_data.to_dict()
                comments.append(comments_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "type": type_,
                "ttl": ttl,
                "records": records,
            }
        )
        if changetype is not UNSET:
            field_dict["changetype"] = changetype
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.comment import Comment
        from ..models.record import Record

        d = dict(src_dict)
        name = d.pop("name")

        type_ = d.pop("type")

        ttl = d.pop("ttl")

        records = []
        _records = d.pop("records")
        for records_item_data in _records:
            records_item = Record.from_dict(records_item_data)

            records.append(records_item)

        changetype = d.pop("changetype", UNSET)

        _comments = d.pop("comments", UNSET)
        comments: list[Comment] | Unset = UNSET
        if _comments is not UNSET:
            comments = []
            for comments_item_data in _comments:
                comments_item = Comment.from_dict(comments_item_data)

                comments.append(comments_item)

        rr_set = cls(
            name=name,
            type_=type_,
            ttl=ttl,
            records=records,
            changetype=changetype,
            comments=comments,
        )

        return rr_set
