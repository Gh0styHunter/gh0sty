"""Unit tests for config manager module."""

import pytest

from typing import Any

from gh0sty.core.config import ConfigManager
from gh0sty.core.exceptions import ConfigError


def test_config_defaults(tmp_path: Any) -> None:
    config_file = tmp_path / "config.json"
    manager = ConfigManager(config_path=config_file)

    # Defaults check
    assert manager.get("threads") == 10
    assert manager.get("timeout") == 5.0
    assert manager.get("default_format") == "json"
    assert config_file.exists() is True


def test_config_updates(tmp_path: Any) -> None:
    config_file = tmp_path / "config.json"
    manager = ConfigManager(config_path=config_file)

    # Success updates
    manager.set("threads", 20)
    assert manager.get("threads") == 20

    manager.set("timeout", 2.5)
    assert manager.get("timeout") == 2.5

    # File persistence check
    new_manager = ConfigManager(config_path=config_file)
    assert new_manager.get("threads") == 20
    assert new_manager.get("timeout") == 2.5


def test_config_validation(tmp_path: Any) -> None:
    config_file = tmp_path / "config.json"
    manager = ConfigManager(config_path=config_file)

    # Invalid key
    with pytest.raises(ConfigError, match="Parâmetro inválido"):
        manager.set("nonexistent_key", "value")

    # Invalid value type (triggers type error matching regex "Tipo de dado inválido")
    with pytest.raises(ConfigError, match="Tipo de dado inválido"):
        manager.set("threads", "twenty")

    with pytest.raises(ConfigError, match="Tipo de dado inválido"):
        manager.set("timeout", "two point five")

    # Float coercion from int/str
    manager.set("timeout", 10)
    assert manager.get("timeout") == 10.0

    manager.set("timeout", "7.5")
    assert manager.get("timeout") == 7.5
