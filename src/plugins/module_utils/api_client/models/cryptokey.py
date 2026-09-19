from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.cryptokey_keytype import CryptokeyKeytype
from ..types import UNSET, Unset

T = TypeVar("T", bound="Cryptokey")


@_attrs_define
class Cryptokey:
    """Describes a DNSSEC cryptographic key

    Attributes:
        type_ (str | Unset): set to "Cryptokey"
        id (int | Unset): The internal identifier, read only
        keytype (CryptokeyKeytype | Unset):
        active (bool | Unset): Whether or not the key is in active use
        published (bool | Unset): Whether or not the DNSKEY record is published in the zone
        dnskey (str | Unset): The DNSKEY record for this key
        ds (list[str] | Unset): An array of DS records for this key
        cds (list[str] | Unset): An array of DS records for this key, filtered by CDS publication settings
        privatekey (str | Unset): The private key in ISC format
        algorithm (str | Unset): The name of the algorithm of the key, should be a mnemonic
        bits (int | Unset): The size of the key
    """

    type_: str | Unset = UNSET
    id: int | Unset = UNSET
    keytype: CryptokeyKeytype | Unset = UNSET
    active: bool | Unset = UNSET
    published: bool | Unset = UNSET
    dnskey: str | Unset = UNSET
    ds: list[str] | Unset = UNSET
    cds: list[str] | Unset = UNSET
    privatekey: str | Unset = UNSET
    algorithm: str | Unset = UNSET
    bits: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        id = self.id

        keytype: str | Unset = UNSET
        if not isinstance(self.keytype, Unset):
            keytype = self.keytype.value

        active = self.active

        published = self.published

        dnskey = self.dnskey

        ds: list[str] | Unset = UNSET
        if not isinstance(self.ds, Unset):
            ds = self.ds

        cds: list[str] | Unset = UNSET
        if not isinstance(self.cds, Unset):
            cds = self.cds

        privatekey = self.privatekey

        algorithm = self.algorithm

        bits = self.bits

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if id is not UNSET:
            field_dict["id"] = id
        if keytype is not UNSET:
            field_dict["keytype"] = keytype
        if active is not UNSET:
            field_dict["active"] = active
        if published is not UNSET:
            field_dict["published"] = published
        if dnskey is not UNSET:
            field_dict["dnskey"] = dnskey
        if ds is not UNSET:
            field_dict["ds"] = ds
        if cds is not UNSET:
            field_dict["cds"] = cds
        if privatekey is not UNSET:
            field_dict["privatekey"] = privatekey
        if algorithm is not UNSET:
            field_dict["algorithm"] = algorithm
        if bits is not UNSET:
            field_dict["bits"] = bits

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = d.pop("type", UNSET)

        id = d.pop("id", UNSET)

        _keytype = d.pop("keytype", UNSET)
        keytype: CryptokeyKeytype | Unset
        if isinstance(_keytype, Unset):
            keytype = UNSET
        else:
            keytype = CryptokeyKeytype(_keytype)

        active = d.pop("active", UNSET)

        published = d.pop("published", UNSET)

        dnskey = d.pop("dnskey", UNSET)

        ds = cast("list[str]", d.pop("ds", UNSET))

        cds = cast("list[str]", d.pop("cds", UNSET))

        privatekey = d.pop("privatekey", UNSET)

        algorithm = d.pop("algorithm", UNSET)

        bits = d.pop("bits", UNSET)

        cryptokey = cls(
            type_=type_,
            id=id,
            keytype=keytype,
            active=active,
            published=published,
            dnskey=dnskey,
            ds=ds,
            cds=cds,
            privatekey=privatekey,
            algorithm=algorithm,
            bits=bits,
        )

        return cryptokey
