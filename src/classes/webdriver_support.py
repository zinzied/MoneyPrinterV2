import os
import shutil
from datetime import datetime

from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


def build_firefox_service() -> Service:
    """
    Resolve a Firefox WebDriver service with resilient fallbacks.

    Priority:
    1) GECKODRIVER_PATH environment variable (if valid file path)
    2) webdriver_manager download
    3) geckodriver found on PATH
    """
    configured = os.environ.get("GECKODRIVER_PATH", "").strip()
    if configured:
        if os.path.isfile(configured):
            return Service(configured)
        raise RuntimeError(
            f"GECKODRIVER_PATH is set but invalid: {configured}. "
            "Point it to geckodriver.exe or unset it."
        )

    try:
        return Service(GeckoDriverManager().install())
    except Exception as download_error:
        local_driver = shutil.which("geckodriver")
        if local_driver:
            return Service(local_driver)

        raise RuntimeError(
            "Could not download geckodriver and no local geckodriver was found. "
            "Install geckodriver manually, add it to PATH, or set GECKODRIVER_PATH."
        ) from download_error


def prepare_firefox_profile(source_profile_path: str, workspace_root: str) -> str:
    """
    Create a writable, throwaway copy of a Firefox profile for Selenium.
    This avoids preference-write failures on locked/read-only original profiles.
    """
    if not os.path.isdir(source_profile_path):
        raise ValueError(
            f"Firefox profile path does not exist or is not a directory: {source_profile_path}"
        )

    profiles_root = os.path.join(workspace_root, ".mp", "firefox_profiles")
    os.makedirs(profiles_root, exist_ok=True)

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    dest_profile = os.path.join(profiles_root, f"profile_{run_id}")

    ignore_names = shutil.ignore_patterns(
        "parent.lock",
        ".parentlock",
        "lock",
        "lockfile",
        "Invalidprefs.js",
        "user.js",
        "prefs.js",
        "compatibility.ini",
        "xulstore.json",
        "geckodriver.exe",
    )
    shutil.copytree(source_profile_path, dest_profile, ignore=ignore_names)
    return dest_profile
