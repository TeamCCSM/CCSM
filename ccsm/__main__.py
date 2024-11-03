import curses
import pickle
import os
from pathlib import Path
from .first_run import first_run

def main(stdscr):
    if curses.has_colors():
        curses.use_default_colors()
    curses.curs_set(0)
    
    main = Path(os.getcwd()) / '.ccsm'
    if not main.exists():
        main.mkdir()
    options_file = main / 'options.ccsm'
    
    options = None
    if not options_file.exists():
        options = first_run()
        options_file.write_bytes(pickle.dumps(options))
    else:
        options = pickle.loads(options_file.read_bytes())
    
    stdscr.addstr(0, 0, str(options))
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
