# -*- coding: utf-8 -*-
""" counting lines in lang files and show stat for every file """

import os
import sys
import json


OUTPUT = "lang_stat_output.txt"


def lang_seeker(dirpath: str, lang_code: str) -> dict:
    """ Looks through the dirs in search for lang files and
        returns the dict of their mod names and paths
    """
    res: dict = {}
    if not os.path.isdir(dirpath):
        print(f"Error: dir '{dirpath}' not found", file=sys.stderr)
        return res
    for item in os.listdir(dirpath):
        l_path: str = os.path.join(dirpath, item, 'lang', f'{lang_code}.json')
        if not os.path.isfile(l_path):
            continue
        res[item] = l_path
    return res


def lang_lines_counter(filepath: str) -> int:
    """ count lines """
    if not os.path.isfile(filepath) or not filepath.endswith('.json'):
        print(f"Error: file '{filepath}' not found or invalid")
        return 0
    with open(filepath, 'r', encoding='utf-8') as f:
        return len(json.load(f))


def statistic_counter(lang_files: dict) -> (int, dict):
    """ counts translated lines """
    total: int = 0
    mod_stat: dict = {}
    for mod_name in lang_files:
        stat: int = lang_lines_counter(lang_files.get(mod_name))
        if stat <= 0:
            continue
        total += stat
        mod_stat[mod_name] = stat
    return total, mod_stat


def form_stats_text(total: int, stats: dict) -> str:
    """ turns stat into text """
    text: list[str] = ['Translation Statistics']
    text.append('Total translated: ' + str(total) + ' lines')
    max_key_length: int = max(len(key) for key in stats)
    text += [str(key) + ': ' + ' '*(max_key_length - len(key)) +
             str(stats[key]) + ' lines' for key in stats]

    max_line_lenght: int = max(len(i) for i in text)
    title_decoration_lenght: int = (max_line_lenght - len(text[0])) // 2

    res: str = '=' * title_decoration_lenght + text[0] +\
        '=' * title_decoration_lenght + '\n\n'
    res += text[1] + '\n\n'
    res += '-' * max_line_lenght + '\n'
    res += 'Translated files\n'
    res += '-' * max_line_lenght + '\n'
    res += '\n'.join(text[2:])
    res += '\n' + '-' * max_line_lenght
    return res


def help_msg(name: str):
    """ help message """
    print('Simple script for counting lang files (in kubejs assets)')
    print('Usage:', name, 'path/to/assets', 'lang_code')
    print('\nNote: saves stats into', OUTPUT)


def main(args: list) -> int:
    """ Main function """
    target: str = args[0]
    lang_code: str = args[1]

    dir_data: dict = lang_seeker(target, lang_code)
    if not isinstance(dir_data, dict) or len(dir_data) < 1:
        print('Error: something went wrong at lang_seeker()', file=sys.stderr)
        return 1

    stat_data: (int, dict) = statistic_counter(dir_data)
    if len(stat_data) < 2 or len(stat_data[1]) < 1:
        print('Error: something went wrong at statistic_counter()',
              file=sys.stderr)
        return 2

    stat_text: str = form_stats_text(*stat_data)
    print(stat_text)
    with open(OUTPUT, 'w+', encoding='utf-8') as f:
        f.write(stat_text + '\n')

    return 0


if __name__ == "__main__":
    argv = sys.argv
    app_name = argv[0]
    if len(argv) < 2 or 'help' in argv or '-h' in argv:
        help_msg(app_name)
        sys.exit(int('help' not in argv))
    if not (os.path.isdir(str(argv[1])) and len(str(argv[2])) != 0):
        print('Error: invalid arguments provided', file=sys.stderr)
        help_msg(app_name)
        sys.exit(1)
    sys.exit(main(argv[1:]))
