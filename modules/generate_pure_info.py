import json
from pathlib import Path


def build_pure_info():
    if not Path('./pure_info.json').is_file():
        infos_with_questions = json.loads(Path("./info_data.json").read_text()).get('persons')
        pure_info = [single_info.get('info') for single_info in infos_with_questions]
        with open('pure_info.json', 'w') as f:
            json.dump(pure_info, f, )


if __name__ == '__main__':
    build_pure_info()
