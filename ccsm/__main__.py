import curses
import pickle
import ui_forge
import json
from ui_forge import items
from collections import OrderedDict
from pathlib import Path
from pathvalidate import sanitize_filename
from . import argument_parser, sav_ops
from .options import first_run, Options


def setup_term():
    if curses.has_colors():
        curses.use_default_colors()
    curses.curs_set(0)


def get_main_path(main_path: Path) -> Path:
    main = main_path / ".ccsm"
    if not main.exists():
        main.mkdir(parents=True)
    return main.resolve()


def save_current_save(options: Options, main_path: Path, window: curses.window):
    editor_win = curses.newwin(*window.getmaxyx(), *window.getbegyx())
    backup_path = ui_forge.editor_ui(editor_win, header="Enter the name of the backup")
    backup_path = sanitize_filename(backup_path)
    backup_path = main_path / "backups" / backup_path
    if not backup_path.exists():
        backup_path.mkdir(parents=True)

    (backup_path / "backup.ccsmbase").write_bytes(
        pickle.dumps(sav_ops.load(options.save_path / "SaveSlot.sav"))
    )

    current_save = sav_ops.load(options.save_path / "SaveSlot.sav")
    current_save = sav_ops.to_neocrab(current_save)

    (backup_path / "backup.neocrab").write_text(json.dumps(current_save, indent=2))


def generate_backup_list(main_path: Path) -> OrderedDict[str, items.OptionItem]:
    backup_selection = {}
    backups_path = main_path / "backups"
    for backup_path in backups_path.iterdir():
        backup_selection[backup_path.name] = items.OptionItem(value=backup_path)
    return OrderedDict(backup_selection)


def load_backup(options: Options, main_path: Path, window: curses.window):
    selection_win = curses.newwin(*window.getmaxyx(), *window.getbegyx())
    selection_path = ui_forge.selection_ui(
        selection_win, options=generate_backup_list(main_path)
    )
    if not isinstance(selection_path, Path):
        return

    save_path = options.save_path / "SaveSlot.sav"
    base = pickle.loads((selection_path / "backup.ccsmbase").read_bytes())
    if not isinstance(base, list):
        return

    selection_neocrab = json.loads((selection_path / "backup.neocrab").read_text())
    merged_save = sav_ops.merge_neocrab(selection_neocrab, base)
    
    Path('./test_.json').write_text(json.dumps(selection_neocrab, indent=2))
    Path('./test.json').write_text(json.dumps(merged_save, indent=2))

    save_path.write_bytes(sav_ops.dump(merged_save))


def main(stdscr: curses.window, args: argument_parser.Args):
    setup_term()

    main = get_main_path(args.main_path)
    options_file = main / "options.ccsm"

    options = None
    if not options_file.exists():
        options = first_run.main()
        if isinstance(options, first_run.UnhandlableError):
            return
        options_file.write_bytes(pickle.dumps(options))
    else:
        options = pickle.loads(options_file.read_bytes())

    win = curses.newwin(curses.LINES - 1, curses.COLS - 1)
    ui_forge.dict_ui(
        win,
        OrderedDict(
            {
                "Quit": items.Item(exit_after_action=True),
                "Backup Current Run": items.RunFunctionItem(
                    function=save_current_save, args=(options, main, win)
                ),
                "Load Backup": items.RunFunctionItem(
                    function=load_backup, args=(options, main, win)
                ),
            }
        ),
    )


if __name__ == "__main__":
    args = argument_parser.parse_args()
    curses.wrapper(main, args)
