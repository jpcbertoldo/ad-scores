"""
# DATA_DIR=${SCRIPT_DIR}/data
# TABLES_FNAME="evaluation-tables.json"
# TABLES_FPATH=${DATA_DIR}/${TABLES_FNAME}
"""
from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path
import warnings
import humanize


DATA_DIR = Path(__file__).parent / "data"
assert DATA_DIR.is_dir(), f"{DATA_DIR} is not a directory"

TABLES_FPATH = DATA_DIR / "evaluation-tables.json"
assert TABLES_FPATH.is_file(), f"{TABLES_FPATH} is not a file"

TABLES_FILTERED_FPATH = DATA_DIR / "evaluation-tables-filtered.json"

if TABLES_FILTERED_FPATH.is_file():
    warnings.warn(f"{TABLES_FILTERED_FPATH.name} will be overwritten")

data = json.load(TABLES_FPATH.open())
print(f"{len(data)=}")

# task names as in the json
TASK_ANOMALY_DETECTION = "Anomaly Detection"

# dataset names as in the json
DATASET_MVTECAD = "MVTec AD"


@dataclass(frozen=True, order=True)
class Sota:
    task: str
    dataset: str


# (task, dataset)
sotas = {
    Sota(TASK_ANOMALY_DETECTION, DATASET_MVTECAD),
}

tasks_selected = {sota.task for sota in sotas}
print(f"{len(tasks_selected)=}")
print(f"{', '.join(tasks_selected)}")

datasets_ptask = {
    task: {sota.dataset for sota in sotas if sota.task == task}
    for task in tasks_selected
}
print(f"{dict(map(lambda kv: (kv[0], len(kv[1])), datasets_ptask.items()))=}")


def filter_datasets(task: dict) -> dict:
    global datasets_ptask
    datasets_selected = datasets_ptask[task["task"]]
    task = deepcopy(task)
    task["datasets"] = [
        dataset for dataset in task["datasets"] 
        if dataset["dataset"] in datasets_selected
    ]
    return task

data = [
    filter_datasets(task) 
    for task in data 
    if task["task"] in tasks_selected
]
print(f"{len(data)=}")
print(f"{dict(map(lambda t: (t['task'], len(t['datasets'])), data))=}")


print(f"{TABLES_FILTERED_FPATH.name} will be written")

with TABLES_FILTERED_FPATH.open("w") as f:
    json.dump(data, f, indent=2, )
    f.write("\n")
    

# print difference of file sizes
print(f"{humanize.naturalsize(TABLES_FPATH.stat().st_size, binary=True)=}")
print(f"{humanize.naturalsize(TABLES_FILTERED_FPATH.stat().st_size, binary=True)=}")
print(f"{humanize.naturalsize(TABLES_FPATH.stat().st_size - TABLES_FILTERED_FPATH.stat().st_size, binary=True)=}")
