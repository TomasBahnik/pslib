import datetime
import os
import re
import subprocess
from pathlib import Path
from typing import List

import typer

START_ITER_REGEXP = r"Starting\siteration\s(\d+)"
START_ITER = re.compile(START_ITER_REGEXP)

NOTIFY_TRANSACTION = 'Notify: Transaction'
START_TRX = re.compile(NOTIFY_TRANSACTION + r"\s\"(.*)\"\sstarted")
# ended with a "Pass" status (Duration: 0.8570 Wasted Time: 0.3640)
TRX_COMMON = r"\s\"(.*)\"\sended\swith\sa\s\"(.*)\"\sstatus"
END_TRX = re.compile(NOTIFY_TRANSACTION + TRX_COMMON)
END_TRX_PASSED = re.compile(r".*\(Duration:\s(\d+\.\d+)\sWasted\sTime:\s(\d+\.\d+)\)")
# (Duration: 14.7360 Think Time: 0.0010 Wasted Time: 3.5380)
END_TRX_PASSED_THINK_TIME = \
    re.compile(r".*\(Duration:\s(\d+\.\d+)\sThink\sTime:\s(\d+\.\d+)\sWasted\sTime:\s(\d+\.\d+)\)")
# t=00006915ms
LOG_TIMESTAMP_RE = re.compile(r"t=(\d+)ms")
# Virtual User Script started at : 2020-10-05 11:27:34
SCRIPT_STARTED_RE = re.compile(r"Virtual User Script.+(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})")
# {"operationName":"GetApplicationMode","variables":{}
# TODO operationName -> OPERATION_NAME const can't escape '\' in f strings use """?
# OPERATION_NAME_START = r"{\"operationName\":\"(\w+)\",\"variables\":(\{.*\})"
OPERATION_NAME_START = r"{\"operationName\":\"(\w+)\","
OPERATION_NAME_START_RE = re.compile(OPERATION_NAME_START)

# load steps and actions from output.txt
# used as LOG_TIMESTAMP_RE = re.compile(r"t=(\d+)ms")
# t=00029357ms: Step 21: Click on Browse button started    [MsgId: MMSG-205180]	[MsgId: MMSG-205180]
SCRIPT_STEP_OUTPUT_RE = r't=(\d+)ms:\sStep\s([\d\.]+):\s([a-zA-Z\s"]+[\w"])\s{4}'
SCRIPT_STEP_OUTPUT_RE_COMPILED = re.compile(SCRIPT_STEP_OUTPUT_RE)


def list_files(folder: Path, file_type: str = '.txt'):
    # traverse root directory, and list directories as dirs and files as files
    file_type_files: List[Path] = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(file_type):
                l_f = Path(root, file)
                file_type_files.append(l_f)
    return file_type_files


def archive_folder(src_path: Path, dest_path: Path, dest_base_file_name: str):
    """
    Create tar gz from 2nd to last dir of src_folder
    archive file name = dest_file_name + datatime stamp + suffix
    """
    dt = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
    src_parts = src_path.parts
    os.makedirs(dest_path, exist_ok=True)
    dest_file_name = Path(str(dest_base_file_name) + "-" + dt + ".tar.gz")
    typer.echo(f"archive {src_parts[-1]} -> {dest_file_name}")
    # -C change dir to second to last backup dir and archive only this one
    cmd = ['tar', '-C', str(Path(*src_parts[:-1])), '-czf', str(Path(dest_path, dest_file_name)), src_parts[-1]]
    p = subprocess.run(cmd)
    return p
