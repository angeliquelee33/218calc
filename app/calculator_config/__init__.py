from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Optional
import os
import logging

from dotenv import load_dotenv
from app.exceptions import ConfigurationError

# Load environment variables from .env file if available
load_dotenv()

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).resolve().parent.parent

@dataclass
class CalculatorConfig:
    """Calculator configuration settings."""
    base_dir: Path
    max_history_size: int = 500  # Updated default to match test expectation
    auto_save: bool = True
    precision: int = 2
    max_input_value: Decimal = Decimal("1000000")
    default_encoding: str = "utf-8"

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        max_history_size: Optional[int] = None,
        auto_save: Optional[bool] = None,
        precision: Optional[int] = None,
        max_input_value: Optional[Decimal] = None,
        default_encoding: Optional[str] = None
    ):
        self.base_dir = base_dir or get_project_root()
        self.max_history_size = max_history_size or 500
        self.auto_save = auto_save if auto_save is not None else True
        self.precision = precision or 2
        self.max_input_value = max_input_value or Decimal("1000000")
        self.default_encoding = default_encoding or "utf-8"

    @property
    def history_dir(self) -> Path:
        return self.base_dir / "history"

    @property
    def log_dir(self) -> Path:
        return self.base_dir / "logs"

    @property
    def log_file(self) -> Path:
        return self.log_dir / "calculator.log"

    @property
    def history_file(self) -> Path:
        return self.history_dir / "calculator_history.csv"

    def validate(self):
        """Validate configuration settings."""
        if not isinstance(self.max_history_size, int) or self.max_history_size <= 0:
            raise ConfigurationError("Max history size must be a positive integer.")
        if not isinstance(self.max_input_value, Decimal) or self.max_input_value <= 0:
            raise ConfigurationError("Max input value must be a positive decimal.")
        if not isinstance(self.precision, int) or self.precision < 0:
            raise ConfigurationError("Precision must be a non-negative integer.")
        logging.info("Configuration validated successfully.")
