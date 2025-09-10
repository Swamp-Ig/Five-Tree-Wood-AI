"""
Configuration management for Five Tree Wood AI.
"""

import os

# Global configuration directory
_CONF_DIR = None


def setup_config(conf_dir=None):
    """
    Set up the configuration directory.

    Args:
        conf_dir: str, path to configuration directory. If None, uses ./conf
    """
    global _CONF_DIR  # pylint: disable=global-statement

    if conf_dir is None:
        _CONF_DIR = os.path.join(os.getcwd(), "conf")
    else:
        _CONF_DIR = conf_dir

    # Ensure the directory exists
    os.makedirs(_CONF_DIR, exist_ok=True)

    print(f"Using configuration directory: {_CONF_DIR}")


def get_config_dir():
    """
    Get the current configuration directory.

    Returns:
        str: Path to the configuration directory

    Raises:
        RuntimeError: If configuration has not been set up
    """
    if _CONF_DIR is None:
        raise RuntimeError("Configuration not initialized. Call setup_config() first.")
    return _CONF_DIR


def get_model_path():
    """
    Get the path to the model file.

    Returns:
        str: Path to the aircon_model.pkl file
    """
    return os.path.join(get_config_dir(), "aircon_model.pkl")


def get_onnx_model_path():
    """
    Get the path to the ONNX model file.

    Returns:
        str: Path to the rf_model.onnx file
    """
    return os.path.join(get_config_dir(), "rf_model.onnx")
