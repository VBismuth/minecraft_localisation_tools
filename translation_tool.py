# -*- coding: utf-8 -*-
"""
Tool for translation
"""
import os
import sys
import json

LINECOUNT = 50
COLUMNCOUNT = 80
OUTPUT_AFFIX = 'output_'
CACHE_SUFFIX = '.cache'
CMD_OPTS = ('help', 'next', 'previous', 'move',
            'delete', 'create',
            'translate', 'auto-translate',
            'undo', 'reset', 'save',
            'quit', 'exit')


def _press_enter():
    input('\nPress enter to continue...')


def _separator(sep='-', n=COLUMNCOUNT):
    print(sep*n)


def print_message(text: str, pretext='',
                  length=COLUMNCOUNT-16,
                  max_split=LINECOUNT//4, ident=0):
    """ stub """
    ending: str = " <...>\n"
    print(pretext, text[:length], sep='', end='')
    n = 1
    while n <= len(text) // length and (max_split == 0 or n < max_split):
        current_text: str = text[length*n:length*(n+1)]
        print(ending, ' '*ident, current_text, sep='', end='')
        n += 1
    print(ending if n <= len(text) // length else '\n', end='')


def alanyze_command(cmd_text: str) -> (int, int):
    """ Returns cmd code, CMD_OPTS index+1, and repeat """
    cmd = cmd_text.lower().strip()
    res: int = 0
    if len(cmd) == 0:
        return (res, -1)

    for cmd_i in CMD_OPTS:
        res += 1
        if cmd_i[0] == cmd[0]:
            break
    else:
        res = 0
    numbers: list[int] = [int(i) for i in cmd.split(' ')
                          if str(i).isdigit()] or [-1]
    return (res, numbers[0])


def cmd_help(_n: None, _app: None):
    """ Help for the cmds """
    _clear_screen()
    print('Command list:')
    _separator()
    print('* Help - shows this message')
    print('* Next/previous (n) - move back or forward in translation key list')
    print('* Move (n) - to a certain postion in translation key list')
    print('* Delete (n) - delete translation key at position')
    print('* Create (n) - create translation key at position')
    print('* Translate - input your translation')
    print('* Auto-translation - use google translation (STUB)')
    print('* Undo - swap to previous translation')
    print('* Reset - change to default translation')
    print('* Save - save lang file')
    print('* Quit/exit - finish')
    _separator()
    print('Note: Using only one letter also works')
    print('Note 2: position starts from 0')

    _press_enter()


def cmd_not_found(_n: None, _app: None):
    """ Command-not-found message """
    _clear_screen()
    _separator('=')
    print("\nCommand not found")
    print("Enter help to see the list of commands")
    _separator()
    _press_enter()


def _stub(_n: None, _app: None):
    print('\nSTUB - Got:', _n)
    print(NotImplemented)
    _press_enter()


def ptr_next(n: int, app: dict):
    """ move pointer forth """

    pointer_addition: int = max(n, 1)
    app['pointer'] = min(app.get('pointer') + pointer_addition,
                         len(app.get('translation_keys'))-1)
    app['current_translation_key'] = app['translation_keys'][app['pointer']]


def ptr_previous(n: int, app: dict):
    """ move pointer back """

    pointer_substraction: int = max(n, 1)
    app['pointer'] = max(app.get('pointer') - pointer_substraction, 0)
    app['current_translation_key'] = app['translation_keys'][app['pointer']]


def ptr_move(n: int, app: dict):
    """ move pointer to a certain position """
    app['pointer'] = min(max(n, 0), len(app.get('translation_keys'))-1)
    app['current_translation_key'] = app['translation_keys'][app['pointer']]


def translate(_: None, app: dict):
    """ add new translation """
    _separator('=')
    print('Current:')
    print(app.get('data')[app.get('current_translation_key')][2])
    _separator()
    print('Add translation')
    i = input('> ')
    translation_data: list = app['data'][app.get('current_translation_key')]
    translation_data[1] = translation_data[2]
    translation_data[2] = i
    _dump_app(app)


def td_undo(_: None, app: dict):
    """ undo to the previous translation """
    data: list = app['data'][app.get('current_translation_key')]
    data[1], data[2] = data[2], data[1]
    _dump_app(app)


def td_reset(_: None, app: dict):
    """ undo to the default translation"""
    data: list = app['data'][app.get('current_translation_key')]
    data[1], data[2] = data[2], data[0]
    _dump_app(app)


def save_translation(_: None, app: dict):
    """ save json translation """
    data: dict = app.get('data')
    save_data: dict = {}
    for key in data:
        save_data[key] = data.get(key)[-1]
    dump_json(app.get('filepath'), save_data, exists_ok=True, only_ascii=False)
    _clear_screen()
    _separator()
    print(f'Saved as "{app.get('filename')}"')
    print(f'Dir: "{app.get('dir')}"')
    _separator()
    _press_enter()


def delete_key(n: int, app: dict):
    """ delete current key or key with index n"""
    if len(app.get('translation_keys')) == 1:
        print('Error: cannot delete last entry')
        _press_enter()
        return
    if len(app.get('translation_keys')) == 0:
        return
    if n <= -1:
        idx: int = app.get('pointer')
    else:
        idx: int = min(n, len(app.get('translation_keys'))-1)
    deleting = app.get('translation_keys').pop(idx)
    app.get('data').pop(deleting)
    app['pointer'] = min(app['pointer'], len(app.get('translation_keys'))-1)
    app['current_translation_key'] = app['translation_keys'][app['pointer']]
    _dump_app(app)


def create_key(n: int, app: dict):
    """ create key at curent pos or at index n """
    if n <= -1:
        idx: int = max(app.get('pointer'), 0)
    else:
        idx: int = min(n, len(app.get('translation_keys'))-1)
    _separator('=')
    i = input('\nNew key> ')
    app.get('translation_keys').insert(idx, i)
    app.get('data')[i] = [''] * 3
    app['current_translation_key'] = app['translation_keys'][app['pointer']]
    _dump_app(app)


def cmd_action(cmd_data: (int, int), _app: dict) -> bool:
    """ do an action """
    if len(cmd_data) < 2 or cmd_data[0] >= CMD_OPTS.index('quit') + 1:
        return True
    commands: (object,) = (cmd_not_found, cmd_help,
                           ptr_next, ptr_previous, ptr_move,
                           delete_key, create_key,
                           translate, _stub,
                           td_undo, td_reset,
                           save_translation)

    action_code: int = min(cmd_data[0], len(commands)-1)
    commands[action_code](cmd_data[1], _app)
    return False


def _clear_screen(n=LINECOUNT):
    print('\n'*(n-1))


def render(app_data: dict):
    """ render screen """
    _clear_screen()

    title: str = f'Translating "{app_data.get("filename")}" in '\
                 f'"{app_data.get("dirname")}"'
    title_decoration_size: int = (COLUMNCOUNT - len(title)) // 2
    translation_key: str = app_data.get('current_translation_key')
    translation_data: list = app_data.get('data').get(translation_key)
    pos: int = app_data.get('pointer')
    max_pos: int = len(app_data.get('translation_keys'))-1

    _separator()
    print('='*title_decoration_size, title, '='*title_decoration_size, sep='')
    print(f'\nTranslation key: "{translation_key}"')
    print(f'Position: {pos}/{max_pos}')
    if translation_data is not None and len(translation_data) == 3:
        print_message(translation_data[0], '\nDefault: ', max_split=1)
        print_message(translation_data[1], 'Previous: ', max_split=1)
        print_message(translation_data[2], 'Current: ', ident=9)
    else:
        print('\nInvalid data!')
    print()
    _separator()


def load_json(filepath: str) -> dict:
    """ Loads json file """
    res: dict = {}
    if not os.path.isfile(filepath):
        print(f"Error: file {os.path.basename(filepath)} does not exists!",
              file=sys.stderr)
        return res
    with open(filepath, 'r', encoding='utf-8') as f:
        res = json.load(f)
    return res


def dump_json(filepath: str, data: dict,
              exists_ok=False, only_ascii=True) -> bool:
    """ Dumps json file """
    if os.path.exists(filepath) and not exists_ok:
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
    print("A script for translation of minecraft lang files (like en_us.json)")
    print(f"\nUsage: {app} path/to/target [help|clean]")
    print("    Optional arguments:")
    print("        help  - show this message and exit")
    print("        clean - clean cache file and exit")


def _dump_app(app: dict, exists_ok=True):
    dump_json(app.get('cache_file'), app, exists_ok=exists_ok)


def setup_app(args: list) -> dict:
    """ Setup for the app """
    if args is None or len(args) == 0:
        print('Error: invalid args at main()', file=sys.stderr)
        return {}
    if not os.path.isfile(args[0]):
        print(f'Error: file "{os.path.basename(args[0])}" not found',
              file=sys.stderr)
        return {}
    filepath: str = os.path.abspath(args[0])
    dir_data: str = os.path.split(filepath)
    cachefile: str = os.path.join(dir_data[0], dir_data[1] + CACHE_SUFFIX)
    if os.path.isfile(cachefile):
        print('Loaded from cachefile')
        return load_json(cachefile)

    res: dict = {}
    res['dir'], res['filename'] = dir_data
    res['dirname']: str = os.path.basename(res.get('dir'))
    res['filepath']: str = filepath

    data: dict = load_json(os.path.abspath(args[0]))
    res['translation_keys']: list = list(data.keys())
    res['pointer']: int = 0
    res['current_translation_key'] = res['translation_keys'][res['pointer']]
    res['data'] = {}
    for key in data.keys():
        res['data'][key] = ([data.get(key)] or [""]) * 3
    res['cache_file'] = cachefile
    _dump_app(res)
    return res


def main(args: list) -> int:
    """ Main function """
    print(args)
    exiting: bool = False
    app: dict = setup_app(args)
    while not exiting:
        render(app)
        i = input('Use help command to see command list\ncmd> ')
        result: (int, int) = alanyze_command(i)
        exiting = cmd_action(result, app)
    return 0


if __name__ == "__main__":
    argv = sys.argv
    app_name = argv[0]
    if len(argv) < 2 or 'help' in argv:
        help_msg(app_name)
        sys.exit(int('help' not in argv))
    if not (os.path.isfile(str(argv[1])) and str(argv[1]).endswith('.json')):
        print('Error: invalid arguments provided', file=sys.stderr)
        help_msg(app_name)
        sys.exit(1)
    if 'clean' in argv and os.path.isfile(argv[1]+CACHE_SUFFIX):
        os.remove(argv[1]+CACHE_SUFFIX)
        print('Cache cleaned')
        sys.exit(0)
    sys.exit(main(argv[1:]))
