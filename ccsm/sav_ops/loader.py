from pathlib import Path
from typing import Any, Dict, List
from SavConverter import read_sav
from SavConverter.SavToJson import to_json_structure


def sav_to_list(props) -> List[Dict[Any, Any]]:
    savJSON = []
    for prop in props:
        savJSON.append(to_json_structure(prop))
    return savJSON


def load(save_path: Path) -> List[Dict[Any, Any]]:
    return sav_to_list(read_sav(str(save_path)))
