import os
import platform


def project_path() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def is_windows() -> bool:
    return any(platform.win32_ver())
