"""
CSV → JSON Reconstruction Script

Purpose
-------
Reconstruct the original JSON annotation format from a CSV file produced
by the companion json_to_csv script.

Function
--------
The CSV file contains:
1. Metadata stored as comment lines (# key: value) at the top.
2. Tabular annotation entries with columns:
   id, x, y, frame_num, paired_id

The script:
- Reads metadata from the CSV comment lines.
- Loads the annotation table using pandas.
- Reconstructs the numbered JSON structure.
- Writes the result to a JSON file.

Usage
-----
python csv_to_json.py input.csv [output.json]

AI Assistance Disclosure
------------------------
Portions of this script were generated with assistance from ChatGPT
(OpenAI GPT-5.3), March 2026. The output was reviewed and modified
by the author before use.
"""

import pandas as pd
import json
import os
import sys


def csv_to_json(csv_path, json_path=None):
    if json_path is None:
        json_path = os.path.splitext(csv_path)[0] + ".json"

    metadata = {}

    # Read metadata from comment lines
    with open(csv_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                line = line[1:].strip()
                if ":" in line:
                    k, v = line.split(":", 1)
                    metadata[k.strip()] = v.strip() if v.strip() != "" else None
                    if metadata[k.strip()].isdigit():
                        metadata[k.strip()] = int(metadata[k.strip()])
            else:
                break

    # Load table ignoring comment lines
    df = pd.read_csv(csv_path, comment="#")

    data = {}

    # Add metadata back
    data.update(metadata)

    # Reconstruct numbered entries
    for _, row in df.iterrows():
        key = str(int(row["id"]))
        data[key] = {
            "x": int(row["x"]),
            "y": int(row["y"]),
            "frame_num": int(row["frame_num"]),
            "paired_id": None if pd.isna(row["paired_id"]) else int(row["paired_id"])
        }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Converted {csv_path} -> {json_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python csv_to_json.py input.csv [output.json]")
        sys.exit(1)

    csv_file = sys.argv[1]
    json_file = sys.argv[2] if len(sys.argv) > 2 else None

    csv_to_json(csv_file, json_file)