import json
from typing import List
from pathlib import Path, PosixPath
import os

BASE_URL = "https://www.worldsurfleague.com"

def build_path(url: str, folder_name: str = None) -> PosixPath:
    """ Returns the file path used to dump the data according to the URL argument """

    split_url =  (
        url
        .removeprefix(f"{BASE_URL}/")
        .replace("-", "_")
    ).split("/")

    root_path = "scrapper/data"
    file_name = "_".join(split_url[1:])
    
    if folder_name:
        data_path = os.path.join(folder_name, f"{file_name}.json")
    else:
        data_path = os.path.join(split_url[0], f"{file_name}.json")

    return Path(os.path.join(root_path, data_path))

def write_json(file_path: PosixPath, data) -> None:
    """ Writes the data into the file provided as argument """

    # create folder if it doesn't exists
    dir = file_path.parent
    if not dir.exists():
        dir.mkdir(parents = True)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def read_txt(file_path: str) -> List:
    """ Reads the file provided as argument """
    with open(file_path, "r") as f:
        data = f.read()
    return data.splitlines()