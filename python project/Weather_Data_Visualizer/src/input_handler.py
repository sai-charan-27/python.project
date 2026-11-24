"""
Input Handler Module
File: src/input_handler.py
Purpose: Safely collect and validate interactive terminal input from users without crashes.
"""

from datetime import datetime
from typing import Optional


def get_integer_input(
    prompt: str,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None,
    default: Optional[int] = None,
) -> int:
    """
    Safely request an integer from user.
    Retries until valid integer in [min_val, max_val] is provided.
    """
    prompt_str = prompt
    if default is not None:
        prompt_str = f"{prompt} [{default}]: "
    else:
        prompt_str = f"{prompt}: "

    while True:
        try:
            raw = input(prompt_str).strip()
            if not raw and default is not None:
                return default
            val = int(raw)
            if min_val is not None and val < min_val:
                print(f"Error: Value must be at least {min_val}. Please try again.")
                continue
            if max_val is not None and val > max_val:
                print(f"Error: Value must be at most {max_val}. Please try again.")
                continue
            return val
        except ValueError:
            print("Error: Invalid integer. Please enter a valid whole number.")
        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled.")
            if default is not None:
                return default
            raise


def get_float_input(
    prompt: str,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    default: Optional[float] = None,
) -> float:
    """
    Safely request a floating-point number from user.
    Retries until valid number in [min_val, max_val] is provided.
    """
    prompt_str = prompt
    if default is not None:
        prompt_str = f"{prompt} [{default}]: "
    else:
        prompt_str = f"{prompt}: "

    while True:
        try:
            raw = input(prompt_str).strip()
            if not raw and default is not None:
                return default
            val = float(raw)
            if min_val is not None and val < min_val:
                print(f"Error: Value must be at least {min_val}. Please try again.")
                continue
            if max_val is not None and val > max_val:
                print(f"Error: Value must be at most {max_val}. Please try again.")
                continue
            return val
        except ValueError:
            print("Error: Invalid number. Please enter a numeric decimal value.")
        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled.")
            if default is not None:
                return default
            raise


def get_date_input(
    prompt: str,
    date_format: str = "%Y-%m-%d",
    default: Optional[str] = None,
) -> str:
    """
    Safely request a date string matching date_format (default YYYY-MM-DD).
    """
    prompt_str = prompt
    if default is not None:
        prompt_str = f"{prompt} (format: YYYY-MM-DD) [{default}]: "
    else:
        prompt_str = f"{prompt} (format: YYYY-MM-DD): "

    while True:
        try:
            raw = input(prompt_str).strip()
            if not raw and default is not None:
                return default
            parsed = datetime.strptime(raw, date_format)
            if parsed.year < 1900 or parsed.year > 2100:
                print("Error: Year out of reasonable range (1900-2100). Please try again.")
                continue
            return raw
        except ValueError:
            print(f"Error: Invalid date format. Please use format {date_format} (e.g. 2026-11-24).")
        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled.")
            if default is not None:
                return default
            raise


def get_text_input(
    prompt: str,
    allow_empty: bool = False,
    default: Optional[str] = None,
) -> str:
    """
    Safely request string input from user.
    """
    prompt_str = prompt
    if default is not None:
        prompt_str = f"{prompt} [{default}]: "
    else:
        prompt_str = f"{prompt}: "

    while True:
        try:
            raw = input(prompt_str).strip()
            if not raw and default is not None:
                return default
            if not raw and not allow_empty:
                print("Error: This field cannot be left blank. Please enter a value.")
                continue
            return raw
        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled.")
            if default is not None:
                return default
            raise


def confirm(prompt: str = "Do you want to proceed?", default: bool = True) -> bool:
    """
    Prompt user for a Yes/No confirmation.
    """
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        try:
            raw = input(prompt + suffix).strip().lower()
            if not raw:
                return default
            if raw in ("y", "yes", "1", "true"):
                return True
            if raw in ("n", "no", "0", "false"):
                return False
            print("Please enter 'y' for yes or 'n' for no.")
        except (KeyboardInterrupt, EOFError):
            return default
