import curses
from dataclasses import dataclass
import ui_forge
from typing import Optional, Union, Tuple
from . import menus, common, options


def platform_select(start_y: int = 0) -> common.Platforms:
    platform_win = curses.newwin(2, 10, start_y, 0)
    platform = ui_forge.selection_ui(platform_win, menus.platform_select)
    return platform


def linux_steam_version_select(start_y: int = 0) -> common.SteamTypes:
    select_win = curses.newwin(2, 10, start_y, 0)
    steam_type = ui_forge.selection_ui(select_win, menus.linux_steam_version_select)
    return steam_type


@dataclass
class Unhandlable:
    pass


def handle_get_options_error(
    options_instance: Union[options.Options, options.GetOptionsError]
) -> Union[Unhandlable, Tuple[options.Options, bool, bool]]:
    platform_overwritten = False
    steam_type_overwritten = False

    while isinstance(options_instance, options.GetOptionsError):
        match options_instance:
            case options.GetOptionsError.Platform:
                header_win = curses.newwin(2, curses.COLS - 1)
                header_win.addstr(0, 0, "Failed to retrieve platform")
                header_win.addstr(1, 0, "Override?")
                header_win.refresh()
                yes_no_win = curses.newwin(2, 6, 2, 0)
                override = ui_forge.selection_ui(yes_no_win, menus.yes_no, start_line=1)
                if override:
                    options_instance = options.Options.get_defaults(
                        platform_override=platform_select(start_y=1)
                    )
                    platform_overwritten = True
                else:
                    return Unhandlable()

            case options.GetOptionsError.SteamType:
                header_win = curses.newwin(1, curses.COLS - 1)
                header_win.addstr(0, 0, "Failed to retrieve steam type")
                header_win.addstr(1, 0, "Override?")
                header_win.refresh()
                yes_no_win = curses.newwin(2, 6, 2, 0)
                override = ui_forge.selection_ui(yes_no_win, menus.yes_no, start_line=1)
                if override:
                    options_instance = options.Options.get_defaults(
                        steam_type_override=linux_steam_version_select(start_y=1)
                    )
                    steam_type_overwritten = True
                else:
                    return Unhandlable()

    return (options_instance, platform_overwritten, steam_type_overwritten)


def first_run() -> Optional[options.Options]:
    platform_overwritten = False
    steam_type_overwritten = False

    options_instance = options.Options.get_defaults()
    if isinstance(options_instance, options.GetOptionsError):
        options_instance = handle_get_options_error(options_instance)
        if isinstance(options_instance, Unhandlable):
            return
        options_instance, platform_overwritten, steam_type_overwritten = (
            options_instance
        )

    welcome_displayed = False
    if not platform_overwritten:
        header_win = curses.newwin(3, curses.COLS - 1)
        header_win.addstr(0, 0, "Looks like this is your first run.")
        welcome_displayed = True
        header_win.addstr(1, 0, f"Detected Platform: {options_instance.platform}")
        header_win.addstr(2, 0, "Override?")
        header_win.refresh()

        yes_no_win = curses.newwin(2, 6, 3, 0)
        override_platform = ui_forge.selection_ui(
            yes_no_win, menus.yes_no, start_line=1
        )

        header_win.clear()
        header_win.refresh()

        if override_platform:
            options_instance.platform = platform_select()
            if options_instance.platform == common.Platforms.Windows:
                options_instance.steam_type = common.SteamTypes.Windows
                options_instance.steam_path = options.steam_paths[common.SteamTypes.Windows]

    if options_instance.platform == common.Platforms.Linux and not steam_type_overwritten:
        if welcome_displayed:
            header_win = curses.newwin(2, curses.COLS - 1)
            header_win.addstr(
                0, 0, f"Detected Steam Type: {options_instance.steam_type}"
            )
            header_win.addstr(1, 0, "Override?")
            header_win.refresh()
        else:
            header_win = curses.newwin(3, curses.COLS - 1)
            header_win.addstr(0, 0, "Looks like this is your first run.")
            header_win.addstr(
                1, 0, f"Detected Steam Type: {options_instance.steam_type}"
            )
            header_win.addstr(2, 0, "Override?")
            header_win.refresh()

        yes_no_win = curses.newwin(2, 6, 3, 0)
        override_steam_type = ui_forge.selection_ui(
            yes_no_win, menus.yes_no, start_line=1
        )

        header_win.clear()
        header_win.refresh()

        if override_steam_type:
            options_instance.steam_path = options.steam_paths[
                linux_steam_version_select()
            ]

    return options_instance
