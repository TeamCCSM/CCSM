from pathlib import Path
from typing import Any, Dict, List
from SavConverter.SavToJson import to_json_structure
from SavConverter.SavReader import SavReader


def sav_to_list(props) -> List[Dict[Any, Any]]:
    savJSON = []
    for prop in props:
        savJSON.append(to_json_structure(prop))
    return savJSON


def load(save_path: Path) -> List[Dict[Any, Any]]:
    sav_reader = SavReader(save_path.read_bytes())
    properties = sav_reader.read_whole_buffer()
    return sav_to_list(properties)
