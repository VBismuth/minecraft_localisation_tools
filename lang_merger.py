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


def help_msg(app: str):
    """ help message """
    print("A script to merge 2 language files (like output_en_us.json) ",
          "by appending missing parts from source file to target file")
    print(f"    Usage: {os.path.basename(app)} path/to/souce path/to/target")


def merge_data(source_data: dict, target_data: dict) -> dict:
    """ Merging dicts """
    if not isinstance(source_data, dict):
        print('Error: invalid source_data provided', file=sys.stderr)
        return {}
    if not isinstance(target_data, dict):
        print('Error: invalid target_data provided', file=sys.stderr)
        return {}
    data = target_data.copy()
    for key in source_data.keys():
        if key in data and len(data.get(key)) != 0:
            continue
        data[key] = source_data.get(key)
    return data


def main(args: list[str]) -> None:
    """ Main function """
    source_file, target_file = args[1:3]
    res_name: str = OUTPUT_AFFIX + os.path.basename(target_file)
    print(f'Merging files {os.path.basename(source_file)} '
          f'and {os.path.basename(target_file)} into {res_name}')
    print('Processing .', end='')
    data_src: dict = load_json(source_file)
    print('.', end='')
    data_trg: dict = load_json(target_file)
    print('.', end='')
    result: dict = merge_data(data_src, data_trg)
    print('. Done')
    dump_json(res_name, result, False)
    print('Dumped as', os.path.abspath(res_name))
    sys.exit(0)


if __name__ == "__main__":
    argv = sys.argv
    app_name = argv[0]
    if len(argv) < 3 or 'help' in argv:
        help_msg(app_name)
        sys.exit(int('help' not in argv))
    if not all(os.path.isfile(str(i)) and str(i).endswith('.json')
               for i in argv[1:3]):
        print('Error: invalid arguments provided', file=sys.stderr)
        help_msg(app_name)
        sys.exit(1)
    main(argv)
