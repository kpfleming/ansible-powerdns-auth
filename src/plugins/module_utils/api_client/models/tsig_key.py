from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="TSIGKey")


@_attrs_define
class TSIGKey:
    """A TSIG key that can be used to authenticate NOTIFY, AXFR, and DNSUPDATE queries.

    Attributes:
        name (str | Unset): The name of the key
        id (str | Unset): The ID for this key, used in the TSIGkey URL endpoint.
        algorithm (str | Unset): The algorithm of the TSIG key
        key (str | Unset): The Base64 encoded secret key, empty when listing keys. MAY be empty when POSTing to have the
            server generate the key material
        type_ (str | Unset): Set to "TSIGKey"
    """

    name: str | Unset = UNSET
    id: str | Unset = UNSET
    algorithm: str | Unset = UNSET
    key: str | Unset = UNSET
    type_: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        id = self.id

        algorithm = self.algorithm

        key = self.key

        type_ = self.type_

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if id is not UNSET:
            field_dict["id"] = id
        if algorithm is not UNSET:
            field_dict["algorithm"] = algorithm
        if key is not UNSET:
            field_dict["key"] = key
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        id = d.pop("id", UNSET)

        algorithm = d.pop("algorithm", UNSET)

        key = d.pop("key", UNSET)

        type_ = d.pop("type", UNSET)

        tsig_key = cls(
            name=name,
            id=id,
            algorithm=algorithm,
            key=key,
            type_=type_,
        )

        return tsig_key
