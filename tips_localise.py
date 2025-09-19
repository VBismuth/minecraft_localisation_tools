# -*- coding: utf-8 -*-
""" A script to localize tips """
import os
import sys
import json
from shutil import rmtree


BASENAME = 'society_tips'
OUTPUTDIR = 'tl_out'


def _target_dir_exists(target: str) -> bool:
    return os.path.isdir(target)


def ask_user(prompt: str, ending='y/N> ') -> bool:
    """ ask user option """
    answer = input(f"{prompt} {ending}")
    return any(x in answer.lower() for x in ('y', '1', 'j', 'д', 's'))


def work_load(target: str) -> bool:
    """ loading target """
    output_dir: str = os.path.join(target, OUTPUTDIR)
    print('Starting')
    if _target_dir_exists(output_dir):
        if not ask_user(f'Dir "{output_dir}" exists. Delete?'):
            print('Could not create output_dir: it already exists',
                  file=sys.stderr)
            return False
        rmtree(output_dir)
        print('Deleted')
    os.mkdir(output_dir)
    print(f'Created output_dir as "{output_dir}"')
    if not _target_dir_exists(output_dir):
        print('Could not create output_dir',
              file=sys.stderr)
        return False

    files: list[str] = file_listing(target)
    print('Processing')
    translation_dict: dict = {}
    for file in files:
        print('  File:', file, end=' .')
        tip_data: dict = load_tip(os.path.join(target, file))
        print('.', end='')
        processed: dict = process_tip(tip_data, file.removesuffix('.json'),
                                      BASENAME)
        print('.', end='')
        dump_json(file, output_dir, processed.get('new_tip'))
        print('. Done ', end='')
        translation_dict.update(processed.get('localize'))
        print('& Dumped')
    dump_json('en_us.json', output_dir, translation_dict)
    print('Dumped en_us.json')
    print('Done')
    return True


def load_tip(path: str) -> dict:
    """ loads tip """
    with open(path, 'r', encoding='utf-8') as f:
        json_data: dict = json.load(f)
    return json_data


def process_tip(data: dict, name: str,
                name_prefix: str) -> dict:
    """ loading tip from data and generate new """
    tip_data: dict = data.copy()
    tip: str = tip_data.get('tip').pop('text')
    gen_name: str = '.'.join((name_prefix, 'tip', name))

    tip_data['tip'].update({'translate': gen_name})
    out_line: dict = {gen_name: tip}
    return {'new_tip': tip_data, 'localize': out_line}


def file_listing(target: str, ext: str = '.json') -> list[str]:
    """ list files in dir """
    raw_data: list = os.listdir(target)
    data: list = [x for x in raw_data if str(x).endswith(ext) and
                  os.path.isfile(x)]
    return data


def dump_json(name: str, path: str, data: dict) -> None:
    """ dump json file """
    with open(os.path.join(path, name), 'w+', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def main(argv: list[str]) -> None:
    """ main function """
    app_name: str = argv.pop(0)
    if len(argv) < 1 or 'help' in argv:
        print("Script to make current "
              "tips (for tips minecraft mod) localizable")
        print(f"    Usage: {app_name} path/to/target")
        sys.exit(int('help' not in argv))

    targ = os.path.abspath(argv[0])
    sys.exit(int(not work_load(targ)))


if __name__ == "__main__":
    main(sys.argv)
