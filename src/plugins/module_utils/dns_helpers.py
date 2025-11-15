# SPDX-FileCopyrightText: 2025 Kevin P. Fleming <kevin@km6g.us>
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-

import dns.exception
import dns.name


class DNSNameError(Exception):
    """The supplied DNS name was not valid."""

    def __init__(self, name, location, e):
        super().__init__(f"Invalid DNS name in '{location}': {name} - {e}")


def validate_dns_name(name, location):
    try:
        return dns.name.from_text(name).to_text()
    except dns.exception.DNSException as e:
        raise DNSNameError(name, location, e) from None
