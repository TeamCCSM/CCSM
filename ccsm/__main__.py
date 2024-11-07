import curses
import pickle
from pathlib import Path
from . import argument_parser
from .options import first_run


def setup_term():
    if curses.has_colors():
        curses.use_default_colors()
    curses.curs_set(0)


def get_main_path(main_path: Path) -> Path:
    main = main_path / ".ccsm"
    if not main.exists():
        main.mkdir(parents=True)
    return main


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
        
    stdscr.addstr(0, 0, str(options))
    stdscr.getch()

if __name__ == "__main__":
    args = argument_parser.parse_args()
    print(args)
    curses.wrapper(main, args)
