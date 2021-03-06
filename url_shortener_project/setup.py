from os import makedirs
from pathlib import Path


def create_dirs(base: Path, apps: list[str]) -> None:
    makedirs(base / 'database', exist_ok=True)
    makedirs(base / 'static', exist_ok=True)
    makedirs(base / 'media', exist_ok=True)
    makedirs(base / 'templates', exist_ok=True)

    for app in apps:
        makedirs(base / app / 'static' / app, exist_ok=True)
        makedirs(base / app / 'templates' / app, exist_ok=True)


def get_static_dirs(apps: list[str]) -> list[str]:
    result_list = []
    for app in apps:
        result_list.append(f"{app}/static/")
    return result_list


def get_template_dirs(apps: list[str]) -> list[str]:
    result_list = []
    for app in apps:
        result_list.append(f"{app}/templates/")
    return result_list
