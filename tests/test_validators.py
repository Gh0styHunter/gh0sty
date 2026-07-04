"""Unit tests for IP, domain, and port validator utilities."""

import pytest

from gh0sty.core.exceptions import ValidationError
from gh0sty.utils.validators import (
    clean_target,
    is_valid_domain,
    is_valid_ip,
    is_valid_ipv4,
    is_valid_ipv6,
    parse_ports,
)


def test_ipv4_validation() -> None:
    assert is_valid_ipv4("127.0.0.1") is True
    assert is_valid_ipv4("192.168.1.254") is True
    assert is_valid_ipv4("256.0.0.1") is False
    assert is_valid_ipv4("localhost") is False
    assert is_valid_ipv4("2001:db8::") is False


def test_ipv6_validation() -> None:
    assert is_valid_ipv6("2001:db8::") is True
    assert is_valid_ipv6("::1") is True
    assert is_valid_ipv6("127.0.0.1") is False
    assert is_valid_ipv6("2001:db8::g") is False


def test_ip_validation() -> None:
    assert is_valid_ip("10.0.0.1") is True
    assert is_valid_ip("::1") is True
    assert is_valid_ip("google.com") is False


def test_domain_validation() -> None:
    assert is_valid_domain("google.com") is True
    assert is_valid_domain("sub.domain.co.uk") is True
    assert is_valid_domain("my-domain.org") is True
    assert is_valid_domain("http://google.com") is True
    assert is_valid_domain("invalid_domain") is False
    assert is_valid_domain("-domain.com") is False
    assert is_valid_domain("domain-.com") is False


def test_clean_target() -> None:
    assert clean_target("http://example.com/path?query=1") == "example.com"
    assert clean_target("https://[2001:db8::1]:8443/page") == "2001:db8::1"
    assert clean_target("192.168.1.50:8080") == "192.168.1.50"


def test_parse_ports() -> None:
    assert len(parse_ports("common")) == 20
    assert len(parse_ports("")) == 20

    assert parse_ports("80,443") == [80, 443]
    assert parse_ports(" 22,  80 , 443 ") == [22, 80, 443]

    assert parse_ports("80-83") == [80, 81, 82, 83]
    assert parse_ports("83-80") == [80, 81, 82, 83]

    assert parse_ports("22,80-82,443") == [22, 80, 81, 82, 443]
    assert parse_ports("80,80-82") == [80, 81, 82]


def test_parse_ports_exceptions() -> None:
    with pytest.raises(ValidationError):
        parse_ports("0")
    with pytest.raises(ValidationError):
        parse_ports("65536")
    with pytest.raises(ValidationError):
        parse_ports("80-90-100")
    with pytest.raises(ValidationError):
        parse_ports("abc")
    with pytest.raises(ValidationError):
        parse_ports("80-abc")
