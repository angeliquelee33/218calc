from dataclasses import dataclass, field
import datetime
from decimal import Decimal
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, HistoryObserver, LoggingObserver
from app.operations import Operation

Number = Union[int, float, Decimal]
CalculationResult = Union[Number, str]

@dataclass
class CalculatorMemento:
    """Stores calculator state for undo/redo functionality."""
    history: List[Calculation]
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert memento to dictionary."""
        return {
            'history': [calc.to_dict() for calc in self.history],
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CalculatorMemento':
        """Create memento from dictionary."""
        return cls(
            history=[Calculation.from_dict(calc) for calc in data['history']],
            timestamp=datetime.datetime.fromisoformat(data['timestamp'])
        )

class Calculator:
    """Main calculator class implementing multiple patterns."""

    def __init__(self, config: Optional[CalculatorConfig] = None):
        if config is None:
            current_file = Path(__file__)
            project_root = current_file.parent.parent
            config = CalculatorConfig(base_dir=project_root)
        self.config = config
        self.config.validate()
        
        os.makedirs(self.config.log_dir, exist_ok=True)
        self._setup_logging()

        self.history: List[Calculation] = []
        self.operation_strategy: Optional[Operation] = None
        self.observers: List[HistoryObserver] = []
        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []
        
        self._setup_directories()
        
        try:
            self.load_history()
        except Exception as e:
            logging.warning(f"Could not load existing history: {e}")
        
        logging.info("Calculator initialized with configuration")

    def _setup_logging(self) -> None:
        try:
            log_file = self.config.log_file.resolve()
            logging.basicConfig(
                filename=str(log_file),
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                force=True
            )
            logging.info("Logging initialized successfully.")
        except Exception as e:
            print(f"Error setting up logging: {e}")
            raise

    def _setup_directories(self) -> None:
        self.config.history_dir.mkdir(parents=True, exist_ok=True)

    def add_observer(self, observer: HistoryObserver) -> None:
        self.observers.append(observer)
        logging.info(f"Added observer: {observer.__class__.__name__}")

    def remove_observer(self, observer: HistoryObserver) -> None:
        self.observers.remove(observer)
        logging.info(f"Removed observer: {observer.__class__.__name__}")

    def set_operation(self, operation: Operation) -> None:
        self.operation_strategy = operation
        logging.info(f"Set operation: {operation}")

    def perform_operation(self, a: Number, b: Number) -> CalculationResult:
        if not self.operation_strategy:
            raise OperationError("No operation set")

        try:
            a = float(a) if isinstance(a, (int, float, Decimal)) else a
            b = float(b) if isinstance(b, (int, float, Decimal)) else b

            result = self.operation_strategy.execute(a, b)
            calculation = Calculation(
                operation=str(self.operation_strategy),
                operand1=a,
                operand2=b,
                result=result,
                timestamp=datetime.datetime.now()
            )
            self.history.append(calculation)
            self.notify_observers(calculation)
            return result
        except ValidationError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"Operation failed: {e}")
            raise OperationError(f"Operation failed: {e}")

    def undo(self) -> bool:
        if not self.undo_stack:
            return False
        memento = self.undo_stack.pop()
        self.redo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = memento.history.copy()
        return True

    def redo(self) -> bool:
        if not self.redo_stack:
            return False
        memento = self.redo_stack.pop()
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = memento.history.copy()
        return True

    def save_history(self) -> None:
        try:
            self.config.history_dir.mkdir(parents=True, exist_ok=True)
            history_data = [
                {
                    'operation': calc.operation,
                    'operand1': calc.operand1,
                    'operand2': calc.operand2,
                    'result': calc.result,
                    'timestamp': calc.timestamp.isoformat(),
                }
                for calc in self.history
            ]
            pd.DataFrame(history_data).to_csv(self.config.history_file, index=False)
            logging.info("History saved successfully.")
        except Exception as e:
            logging.error(f"Failed to save history: {e}")
            raise OperationError(f"Failed to save history: {e}")

    def load_history(self) -> None:
        try:
            if self.config.history_file.exists():
                df = pd.read_csv(self.config.history_file)
                self.history = [
                    Calculation.from_dict(row)
                    for row in df.to_dict(orient="records")
                ]
                logging.info("History loaded successfully.")
            else:
                logging.info("No history file found.")
        except Exception as e:
            logging.error(f"Failed to load history: {e}")
            raise OperationError(f"Failed to load history: {e}")

    def clear_history(self) -> None:
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
        logging.info("History cleared")

    def notify_observers(self, calculation: Calculation) -> None:
        for observer in self.observers:
            observer.update(calculation)

def calculator_repl():
    calc = Calculator()
    calc.add_observer(LoggingObserver())
    print("Calculator REPL started. Type 'help' for commands.")
    while True:
        command = input("\nEnter command: ").strip().lower()
        if command == 'exit':
            calc.save_history()
            print("History saved successfully.")
            print("Exiting calculator REPL.")
            break
        elif command == 'help':
            print("\nAvailable commands: add, subtract, multiply, divide, exit")
        else:
            print(f"Executing command: {command}")
