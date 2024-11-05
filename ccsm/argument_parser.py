from dataclasses import dataclass
from pathlib import Path
import argparse


@dataclass
class Args:
    main_path: Path


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        prog="CCSM", description="A WIP Save Manager for Crab Champions"
    )
    parser.add_argument("-p", "--path", type=Path, default=Path.home())
    args = parser.parse_args()
    return Args(args.path)
