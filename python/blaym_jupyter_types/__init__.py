from importlib.resources import files
from pathlib import Path

from . import _generated
from ._generated import *  # noqa: F401,F403

__all__ = [
    name
    for name, obj in vars(_generated).items()
    if getattr(obj, "__module__", None) == _generated.__name__
] + ["schema_path"]


def schema_path() -> Path:
    """Path of the JSON Schema bundle shipped inside this package."""
    return Path(
        str(files(__package__).joinpath("schema", "blaym-jupyter-contracts.schema.json"))
    )
