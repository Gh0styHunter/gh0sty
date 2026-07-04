"""Configuration manager module loading, validating, and persisting configurations."""

import json
from pathlib import Path
from typing import Any

from gh0sty.core.constants import (
    CONFIG_FILE,
    DEFAULT_FORMAT,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_THREADS,
    DEFAULT_TIMEOUT,
)
from gh0sty.core.exceptions import ConfigError

DEFAULT_SETTINGS: dict[str, Any] = {
    "default_output_dir": str(DEFAULT_OUTPUT_DIR),
    "threads": DEFAULT_THREADS,
    "timeout": DEFAULT_TIMEOUT,
    "default_format": DEFAULT_FORMAT,
}


class ConfigManager:
    """Manages system configurations stored in JSON format."""

    def __init__(self, config_path: Path = CONFIG_FILE) -> None:
        self.config_path = config_path
        self._settings: dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Loads configuration from file or initializes defaults."""
        try:
            if not self.config_path.exists():
                self._settings = DEFAULT_SETTINGS.copy()
                self.save()
                return

            with open(self.config_path, encoding="utf-8") as f:
                data = json.load(f)
                self._settings = DEFAULT_SETTINGS.copy()
                self._settings.update(data)
        except json.JSONDecodeError as e:
            raise ConfigError(f"Falha ao carregar configurações: {e}") from e
        except Exception as e:
            raise ConfigError(f"Falha ao carregar configurações: {e}") from e

    def save(self) -> None:
        """Saves current configuration to the config path."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=4)
        except Exception as e:
            raise ConfigError(f"Falha ao salvar configurações: {e}") from e

    def get(self, key: str) -> Any:
        """Gets a configuration setting.

        Args:
            key: Config key name.

        Returns:
            The configured value or default.
        """
        return self._settings.get(key, DEFAULT_SETTINGS.get(key))

    def set(self, key: str, value: Any) -> None:
        """Sets a configuration setting and persists it.

        Args:
            key: Config key name.
            value: Value to store.
        """
        if key not in DEFAULT_SETTINGS:
            raise ConfigError(f"Parâmetro inválido: '{key}'")

        expected_type = type(DEFAULT_SETTINGS[key])

        # Attempt safe coercion
        if expected_type is float and isinstance(value, int):
            value = float(value)
        elif expected_type is int and isinstance(value, str):
            try:
                value = int(value)
            except ValueError as e:
                raise ConfigError(
                    f"Tipo de dado inválido para o parâmetro '{key}'"
                ) from e
        elif expected_type is float and isinstance(value, str):
            try:
                value = float(value)
            except ValueError as e:
                raise ConfigError(
                    f"Tipo de dado inválido para o parâmetro '{key}'"
                ) from e

        if not isinstance(value, expected_type):
            raise ConfigError(
                f"Tipo de dado inválido para o parâmetro '{key}'"
            )

        self._settings[key] = value
        self.save()

    def get_all(self) -> dict[str, Any]:
        """Returns all configuration settings."""
        return self._settings.copy()


# Global config instance
config_manager = ConfigManager()
