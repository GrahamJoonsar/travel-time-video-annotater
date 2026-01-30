
"""
Marker: This class represents a point in a video at a particular time and screen coordinates
Marker Manager: This class keeps track of all the markers for a particular instance of video,
                and is responsible for saving, reading, and displaying markers, among other functions.
"""

# Used for reading and writing the marker files
import json
from datetime import datetime

class Marker:
    def __init__(self, 
                 pos: tuple[int, int], 
                 frame_num: int,
                 id: int = None,
                 paired_id: int = None):
        
        # Both position and the frame number of the marker are neccesary for its appearance in the video feed
        self.pos = pos
        self.frame_num = frame_num
        
        # Marker manager will maintain uniqueness between IDs
        self.id = id

        # The id of the marker that this one is paired with
        self.paired_id = paired_id
    
    # Prints out the neccesary information for this marker
    def display(self):
        print(f"{self.id}: ({self.pos[0]}, {self.pos[1]}) | #{self.frame_num} | => {self.paired_id}")

    # Note, this does not include the marker's own ID
    def to_dict(self):
        return {
            "x": self.pos[0],
            "y": self.pos[1],
            "frame_num": self.frame_num,
            "paired_id": self.paired_id,
        }


# Class that collects marker instances for a specific video,
# ensuring that IDs are unique and paired IDs are managed properly
class Marker_Manager:
    HIGHEST_ID = 0 # Static class variable neccesary to keep IDs unique between markers
    def __init__(self):
        self.markers = {}
        self.frame_step = None

    def add_marker(self, pos: tuple[int, int], frame_num: int):
        Marker_Manager.HIGHEST_ID += 1
        self.markers[Marker_Manager.HIGHEST_ID] = Marker(
            pos,
            frame_num,
            Marker_Manager.HIGHEST_ID,
            None
        )
    
    # Your input should be a properly formatted JSON file with marker data,
    # function returns the frame_step and the video path in (int, str)
    # Function will error on FileNotFound, should be handled by user
    def read_markers(self, marker_path: str) -> tuple[int, str]:
        with open(marker_path) as f:
            # Erasing marker data possibly previously contained, and resetting HIGHEST ID
            self.markers = {}
            Marker_Manager.HIGHEST_ID = 0
            marker_data = json.load(f)
            # Retrieve header data then remove, leaving only marker data
            ret = (marker_data["frame_step"], marker_data["vid_path"])
            keys_to_remove = []
            for key in marker_data:
                if not key.isdigit():
                    keys_to_remove.append(key)
            for key in keys_to_remove:
                del marker_data[key]
            
            # Turn each marker entry into a Marker object
            for key in marker_data:
                self.markers[int(key)] = Marker(
                    pos=(marker_data[key]["x"], marker_data[key]["y"]),
                    frame_num=marker_data[key]["frame_num"],
                    id=int(key),
                    paired_id=marker_data[key]["paired_id"]
                )
                if Marker_Manager.HIGHEST_ID < int(key):
                    Marker_Manager.HIGHEST_ID = int(key)

            return ret


    # Writes the marker dataframe to the specified JSON path
    # Frame step and vid_path needed for JSON header
    def write_markers(self, marker_path: str, frame_step: int, vid_path: str):
        with open(marker_path, "w") as f:
            output_dict = {}

            # Adding header data
            output_dict["frame_step"] = frame_step
            output_dict["vid_path"] = vid_path
            formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            output_dict["date_modified"] = formatted_datetime

            for key in self.markers:
                output_dict[key] = self.markers[key].to_dict()
            json.dump(output_dict, f, indent=4)
        print("SAVED MARKERS")