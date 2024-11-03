import curses
import ui_forge
from typing import Union, Tuple
from pathlib import Path
from . import menus, common, options


def path_validator(path: str) -> bool:
    new_path = Path(path)
    return new_path.exists() and new_path.is_dir()


def platform_select(start_y: int = 0) -> common.Platforms:
    platform_win = curses.newwin(2, 27, start_y, 0)
    platform = ui_forge.selection_ui(platform_win, menus.platform_select)
    return platform


def linux_steam_path_select(current_type: common.SteamTypes, start_y: int = 0) -> Path:
    editor_win = curses.newwin(3, curses.COLS - 1, start_y, 0)
    return Path(
        ui_forge.editor_ui(
            editor_win,
            str(options.steam_paths[current_type]),
            path_validator,
            header="Please input the path of steam, ending with the directory named 'Steam' (Will reset your input if the path is invalid/doesn't exist).",
        )
    )


class Unhandlable:
    pass


def handle_get_options_error(
    options_instance: Union[options.Options, options.GetOptionsError]
) -> Union[Unhandlable, Tuple[options.Options, bool, bool]]:
    platform_overwritten = False
    steam_path_overwritten = False

    while isinstance(options_instance, options.GetOptionsError):
        match options_instance:
            case options.GetOptionsError.Platform:
                header_win = curses.newwin(2, curses.COLS - 1)
                header_win.addstr(0, 0, "Failed to retrieve platform")
                header_win.addstr(1, 0, "Override?")
                header_win.refresh()
                yes_no_win = curses.newwin(2, 6, 2, 0)
                override = ui_forge.selection_ui(yes_no_win, menus.yes_no)
                if override:
                    options_instance = options.Options.get_defaults(
                        platform_override=platform_select()
                    )
                    platform_overwritten = True
                else:
                    return Unhandlable()

            case options.GetOptionsError.SteamType:
                header_win = curses.newwin(2, curses.COLS - 1)
                header_win.addstr(0, 0, "Default steam path does not appear to exist.")
                header_win.addstr(1, 0, "Override?")
                header_win.refresh()
                yes_no_win = curses.newwin(2, 6, 2, 0)
                override = ui_forge.selection_ui(yes_no_win, menus.yes_no)
                if override:
                    options_instance = options.Options.get_defaults(
                        steam_type_override=common.SteamTypes.Custom,
                        steam_path_override=linux_steam_path_select(
                            common.SteamTypes.LinuxNative
                        ),
                    )
                    steam_path_overwritten = True
                else:
                    return Unhandlable()

            case options.GetOptionsError.CustomTypeNoPathOverride:
                return Unhandlable()

    return (options_instance, platform_overwritten, steam_path_overwritten)


def main() -> Union[options.Options, Unhandlable]:
    platform_overwritten = False
    steam_path_overwritten = False

    options_instance = options.Options.get_defaults()
    options_instance_and_data = handle_get_options_error(options_instance)
    if isinstance(options_instance_and_data, Unhandlable):
        return Unhandlable()
    options_instance, platform_overwritten, steam_path_overwritten = (
        options_instance_and_data
    )

    welcome_displayed = False
    if not platform_overwritten:
        header_win = curses.newwin(3, curses.COLS - 1)
        header_win.addstr(0, 0, "Looks like this is your first run.")
        welcome_displayed = True
        header_win.addstr(1, 0, f"Detected Platform: {options_instance.platform}")
        header_win.addstr(
            2, 0, "Override? (SEVERAL THINGS MAY BREAK IF YOU CHOOSE THE WRONG ONE)"
        )
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

        if not options_instance.steam_path.exists() and not steam_path_overwritten:
            header_win = curses.newwin(1, curses.COLS - 1)
            header_win.addstr("Default steam path does not appear to exist.")
            header_win.refresh()
            options_instance.steam_type = common.SteamTypes.Custom
            options_instance.steam_path = linux_steam_path_select(
                common.SteamTypes.Windows, start_y=1
            )

    if (
        options_instance.platform == common.Platforms.Linux
        and not steam_path_overwritten
    ):
        override_steam_path: bool
        if welcome_displayed:
            header_win = curses.newwin(2, curses.COLS - 1)
            header_win.addstr(
                0, 0, f"Detected Steam Path: {options_instance.steam_path}"
            )
            header_win.addstr(1, 0, "Override?")
            header_win.refresh()
            yes_no_win = curses.newwin(2, 6, 2, 0)
            override_steam_path = ui_forge.selection_ui(
                yes_no_win, menus.yes_no, start_line=1
            )
        else:
            header_win = curses.newwin(3, curses.COLS - 1)
            header_win.addstr(0, 0, "Looks like this is your first run.")
            header_win.addstr(
                1, 0, f"Detected Steam Path: {options_instance.steam_path}"
            )
            header_win.addstr(2, 0, "Override?")
            header_win.refresh()
            yes_no_win = curses.newwin(2, 6, 3, 0)
            override_steam_path = ui_forge.selection_ui(
                yes_no_win, menus.yes_no, start_line=1
            )

        header_win.clear()
        header_win.refresh()

        if override_steam_path:
            options_instance.steam_type = common.SteamTypes.Custom
            options_instance.steam_path = linux_steam_path_select(
                common.SteamTypes.LinuxNative
            )

    installed = options_instance.steam_path.exists()

    if not installed:
        pass

    return options_instance
