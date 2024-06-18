from pathlib import Path


def build_pure_info():
    if not Path('./pure_info.json').is_file():
        json.loads()
