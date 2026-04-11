from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.zone_kind import ZoneKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rr_set import RRSet


T = TypeVar("T", bound="Zone")


@_attrs_define
class Zone:
    """This represents an authoritative DNS Zone.

    Attributes:
        id (str | Unset): Opaque zone id (string), assigned by the server, should not be interpreted by the application.
            Guaranteed to be safe for embedding in URLs.
        name (str | Unset): Name of the zone (e.g. “example.com.”) MUST have a trailing dot
        type_ (str | Unset): Set to “Zone”
        url (str | Unset): API endpoint for this zone
        kind (ZoneKind | Unset): Zone kind, one of “Native”, “Master”, “Slave”, “Producer”, “Consumer”
        rrsets (list[RRSet] | Unset): RRSets in this zone (for zones/{zone_id} endpoint only; omitted during GET on the
            .../zones list endpoint)
        serial (int | Unset): The SOA serial number
        notified_serial (int | Unset): The SOA serial notifications have been sent out for
        edited_serial (int | Unset): The SOA serial as seen in query responses. Calculated using the SOA-EDIT metadata,
            default-soa-edit and default-soa-edit-signed settings
        masters (list[str] | Unset): List of IP addresses configured as a master for this zone (“Slave” type zones only)
        dnssec (bool | Unset): Whether or not this zone is DNSSEC signed (inferred from presigned being true XOR
            presence of at least one cryptokey with active being true)
        nsec3param (str | Unset): The NSEC3PARAM record
        nsec3narrow (bool | Unset): Whether or not the zone uses NSEC3 narrow
        presigned (bool | Unset): Whether or not the zone is pre-signed
        soa_edit (str | Unset): The SOA-EDIT metadata item
        soa_edit_api (str | Unset): The SOA-EDIT-API metadata item
        api_rectify (bool | Unset): Whether or not the zone will be rectified on data changes via the API
        zone (str | Unset): MAY contain a BIND-style zone file when creating a zone
        catalog (str | Unset): The catalog this zone is a member of
        account (str | Unset): MAY be set. Its value is defined by local policy
        nameservers (list[str] | Unset): MAY be sent in client bodies during creation, and MUST NOT be sent by the
            server. Simple list of strings of nameserver names, including the trailing dot. Not required for slave zones.
        master_tsig_key_ids (list[str] | Unset): The id of the TSIG keys used for master operation in this zone
        slave_tsig_key_ids (list[str] | Unset): The id of the TSIG keys used for slave operation in this zone
        last_check (int | Unset):
    """

    id: str | Unset = UNSET
    name: str | Unset = UNSET
    type_: str | Unset = UNSET
    url: str | Unset = UNSET
    kind: ZoneKind | Unset = UNSET
    rrsets: list[RRSet] | Unset = UNSET
    serial: int | Unset = UNSET
    notified_serial: int | Unset = UNSET
    edited_serial: int | Unset = UNSET
    masters: list[str] | Unset = UNSET
    dnssec: bool | Unset = UNSET
    nsec3param: str | Unset = UNSET
    nsec3narrow: bool | Unset = UNSET
    presigned: bool | Unset = UNSET
    soa_edit: str | Unset = UNSET
    soa_edit_api: str | Unset = UNSET
    api_rectify: bool | Unset = UNSET
    zone: str | Unset = UNSET
    catalog: str | Unset = UNSET
    account: str | Unset = UNSET
    nameservers: list[str] | Unset = UNSET
    master_tsig_key_ids: list[str] | Unset = UNSET
    slave_tsig_key_ids: list[str] | Unset = UNSET
    last_check: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.rr_set import RRSet

        id = self.id

        name = self.name

        type_ = self.type_

        url = self.url

        kind: str | Unset = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        rrsets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.rrsets, Unset):
            rrsets = []
            for rrsets_item_data in self.rrsets:
                rrsets_item = rrsets_item_data.to_dict()
                rrsets.append(rrsets_item)

        serial = self.serial

        notified_serial = self.notified_serial

        edited_serial = self.edited_serial

        masters: list[str] | Unset = UNSET
        if not isinstance(self.masters, Unset):
            masters = self.masters

        dnssec = self.dnssec

        nsec3param = self.nsec3param

        nsec3narrow = self.nsec3narrow

        presigned = self.presigned

        soa_edit = self.soa_edit

        soa_edit_api = self.soa_edit_api

        api_rectify = self.api_rectify

        zone = self.zone

        catalog = self.catalog

        account = self.account

        nameservers: list[str] | Unset = UNSET
        if not isinstance(self.nameservers, Unset):
            nameservers = self.nameservers

        master_tsig_key_ids: list[str] | Unset = UNSET
        if not isinstance(self.master_tsig_key_ids, Unset):
            master_tsig_key_ids = self.master_tsig_key_ids

        slave_tsig_key_ids: list[str] | Unset = UNSET
        if not isinstance(self.slave_tsig_key_ids, Unset):
            slave_tsig_key_ids = self.slave_tsig_key_ids

        last_check = self.last_check

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_
        if url is not UNSET:
            field_dict["url"] = url
        if kind is not UNSET:
            field_dict["kind"] = kind
        if rrsets is not UNSET:
            field_dict["rrsets"] = rrsets
        if serial is not UNSET:
            field_dict["serial"] = serial
        if notified_serial is not UNSET:
            field_dict["notified_serial"] = notified_serial
        if edited_serial is not UNSET:
            field_dict["edited_serial"] = edited_serial
        if masters is not UNSET:
            field_dict["masters"] = masters
        if dnssec is not UNSET:
            field_dict["dnssec"] = dnssec
        if nsec3param is not UNSET:
            field_dict["nsec3param"] = nsec3param
        if nsec3narrow is not UNSET:
            field_dict["nsec3narrow"] = nsec3narrow
        if presigned is not UNSET:
            field_dict["presigned"] = presigned
        if soa_edit is not UNSET:
            field_dict["soa_edit"] = soa_edit
        if soa_edit_api is not UNSET:
            field_dict["soa_edit_api"] = soa_edit_api
        if api_rectify is not UNSET:
            field_dict["api_rectify"] = api_rectify
        if zone is not UNSET:
            field_dict["zone"] = zone
        if catalog is not UNSET:
            field_dict["catalog"] = catalog
        if account is not UNSET:
            field_dict["account"] = account
        if nameservers is not UNSET:
            field_dict["nameservers"] = nameservers
        if master_tsig_key_ids is not UNSET:
            field_dict["master_tsig_key_ids"] = master_tsig_key_ids
        if slave_tsig_key_ids is not UNSET:
            field_dict["slave_tsig_key_ids"] = slave_tsig_key_ids
        if last_check is not UNSET:
            field_dict["last_check"] = last_check

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.rr_set import RRSet

        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        type_ = d.pop("type", UNSET)

        url = d.pop("url", UNSET)

        _kind = d.pop("kind", UNSET)
        kind: ZoneKind | Unset
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = ZoneKind(_kind)

        _rrsets = d.pop("rrsets", UNSET)
        rrsets: list[RRSet] | Unset = UNSET
        if _rrsets is not UNSET:
            rrsets = []
            for rrsets_item_data in _rrsets:
                rrsets_item = RRSet.from_dict(rrsets_item_data)

                rrsets.append(rrsets_item)

        serial = d.pop("serial", UNSET)

        notified_serial = d.pop("notified_serial", UNSET)

        edited_serial = d.pop("edited_serial", UNSET)

        masters = cast("list[str]", d.pop("masters", UNSET))

        dnssec = d.pop("dnssec", UNSET)

        nsec3param = d.pop("nsec3param", UNSET)

        nsec3narrow = d.pop("nsec3narrow", UNSET)

        presigned = d.pop("presigned", UNSET)

        soa_edit = d.pop("soa_edit", UNSET)

        soa_edit_api = d.pop("soa_edit_api", UNSET)

        api_rectify = d.pop("api_rectify", UNSET)

        zone = d.pop("zone", UNSET)

        catalog = d.pop("catalog", UNSET)

        account = d.pop("account", UNSET)

        nameservers = cast("list[str]", d.pop("nameservers", UNSET))

        master_tsig_key_ids = cast("list[str]", d.pop("master_tsig_key_ids", UNSET))

        slave_tsig_key_ids = cast("list[str]", d.pop("slave_tsig_key_ids", UNSET))

        last_check = d.pop("last_check", UNSET)

        zone = cls(
            id=id,
            name=name,
            type_=type_,
            url=url,
            kind=kind,
            rrsets=rrsets,
            serial=serial,
            notified_serial=notified_serial,
            edited_serial=edited_serial,
            masters=masters,
            dnssec=dnssec,
            nsec3param=nsec3param,
            nsec3narrow=nsec3narrow,
            presigned=presigned,
            soa_edit=soa_edit,
            soa_edit_api=soa_edit_api,
            api_rectify=api_rectify,
            zone=zone,
            catalog=catalog,
            account=account,
            nameservers=nameservers,
            master_tsig_key_ids=master_tsig_key_ids,
            slave_tsig_key_ids=slave_tsig_key_ids,
            last_check=last_check,
        )

        return zone
