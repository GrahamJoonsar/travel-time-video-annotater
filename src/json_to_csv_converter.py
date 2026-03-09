"""
JSON → CSV Conversion Script for Marker Data

Purpose
-------
This script converts marker annotation data stored in a JSON file into a CSV file.

Function
--------
The input JSON file contains:
1. Metadata fields describing the source video and annotation state
   (e.g., frame_step, vid_path, date_modified).
2. Numbered keys (Marker IDs) ("1", "2", "3", ...) representing annotation entries
   containing x/y pixel coordinates, frame numbers, and optional paired IDs.

The script:
- Reads the JSON file.
- Separates metadata fields from annotation entries.
- Converts the numbered annotation entries into a pandas DataFrame.
- Writes the DataFrame to CSV.
- Preserves metadata by writing it as commented lines (#) at the top
  of the CSV file so that it is stored once while remaining compatible
  with CSV readers.

Usage
-----
python json_to_csv.py input.json [output.csv]

Notes
-----
When reading the resulting CSV with pandas, metadata lines can be ignored with:
    pd.read_csv("file.csv", comment="#")

AI Assistance Disclosure
------------------------
Portions of this script were generated with assistance from ChatGPT
(OpenAI GPT-5.3), March 2026. The output was reviewed and modified
by the author before use.
"""
import json
import pandas as pd
import os
import sys


def json_to_csv(json_path, csv_path=None):
    if csv_path is None:
        csv_path = os.path.splitext(json_path)[0] + ".csv"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract metadata
    metadata_keys = ["frame_step", "vid_path", "date_modified"]
    metadata = {k: data.get(k) for k in metadata_keys}

    # Extract numbered entries
    rows = []
    for key, value in data.items():
        if key.isdigit() and isinstance(value, dict):
            rows.append({
                "id": int(key),
                "x": value.get("x"),
                "y": value.get("y"),
                "frame_num": value.get("frame_num"),
                "paired_id": value.get("paired_id")
            })

    df = pd.DataFrame(rows).sort_values("id")

    # Write metadata + dataframe
    with open(csv_path, "w", encoding="utf-8") as f:
        for k, v in metadata.items():
            f.write(f"# {k}: {v}\n")
        df.to_csv(f, index=False)

    print(f"Converted {json_path} -> {csv_path}")


if __name__ == "__main__":
    json_file = sys.argv[1]
    csv_file = sys.argv[2] if len(sys.argv) > 2 else None
    json_to_csv(json_file, csv_file)