# -*- coding: utf-8 -*-
"""
Merging two minecraft lang files
by appending missing parts from first to the last
"""
import os
import sys
import json

OUTPUT_AFFIX = 'output_'


def load_json(filepath: str) -> dict:
    """ Loads json file """
    res: dict = {}
    if not os.path.isfile(filepath) or not filepath.endswith('.json'):
        print(f"Error: file {os.path.basename(filepath)} does not exists!",
              file=sys.stderr)
        return res
    with open(filepath, 'r', encoding='utf-8') as f:
        res = json.load(f)
    return res


def dump_json(filepath: str, data: dict, only_ascii=True) -> bool:
    """ Dumps json file """
    if os.path.exists(filepath):
        print(f"Error: file {os.path.basename(filepath)} is already exists!",
              file=sys.stderr)
        return False
    if not isinstance(data, dict) or len(data) == 0:
        print('Error: invalid data! Got:', data, file=sys.stderr)
        return False

    with open(filepath, 'w+', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=only_ascii)
    return True


def fill_empty(lang_data: dict):
    """ fills empty entries """
    if not isinstance(lang_data, dict):
        print('Error: got invalid arg at fill_empty()', file=sys.stderr)
    for key in lang_data:
        if lang_data.get(key) is not None and lang_data.get(key) != '':
            continue
        name: str = ' '.join(str(i).capitalize() for i in
                             str(key).rsplit('.', maxsplit=1)[-1].split('_'))
        lang_data[key] = name


def help_msg(app: str):
    """ help message """
    print("A script to fill empty translation keys by their name")
    print(f"    Usage: {os.path.basename(app)} path/to/target")


def main(args: list[str]) -> None:
    """ Main function """
    target_file: str = args[1]
    res_name: str = OUTPUT_AFFIX + os.path.basename(target_file)
    data: dict = load_json(target_file)
    fill_empty(data)
    dump_json(res_name, data)
    sys.exit(0)


if __name__ == "__main__":
    argv = sys.argv
    app_name = argv[0]
    if len(argv) < 2 or 'help' in argv:
        help_msg(app_name)
        sys.exit(int('help' not in argv))
    if not os.path.isfile(str(argv[1])) or not str(argv[1]).endswith('.json'):
        print('Error: invalid arguments provided', file=sys.stderr)
        help_msg(app_name)
        sys.exit(1)
    main(argv)
