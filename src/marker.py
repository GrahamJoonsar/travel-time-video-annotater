
"""
Marker: This class represents a point in a video at a particular time and screen coordinates
Marker Manager: This class keeps track of all the markers for a particular instance of video,
                and is responsible for saving, reading, and displaying markers, among other functions.

TODO: Change the marker saving and reading to work with json instead.
"""

# Used for reading and writing the marker files
import json
from datetime import datetime

class Marker:
    HIGHEST_ID = 0 # Static class variable neccesary to keep IDs unique between markers
    def __init__(self, 
                 pos: tuple[int, int], 
                 frame_num: int,
                 id: int = None,
                 paired_id: int = None):
        
        # Both position and the frame number of the marker are neccesary for its appearance in the video feed
        self.pos = pos
        self.frame_num = frame_num
        
        # When setting a new ID, do one larger than the previous highest
        if id is None:
            self.id = Marker.HIGHEST_ID + 1
            Marker.HIGHEST_ID = self.id
        else:
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

class Marker_Manager:
    def __init__(self):
        self.markers = {}
    
    # Your input should be a properly formatted JSON file with marker data
    def read_markers(self, marker_path: str):
        # TODO
        pass


    # Writes the marker dataframe to the specified JSON path
    # Frame step and vid_path needed for JSON header
    def write_markers(self, marker_path: str, frame_step: int, vid_path: str):
        with open(marker_path, "w") as f:
            output_dict = {}
            output_dict["frame_step"] = frame_step
            output_dict["vid_path"] = vid_path
            formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            output_dict["date_modified"] = formatted_datetime

            for key in self.markers:
                output_dict[key] = self.markers[key].to_dict()
            json.dump(output_dict, f, indent=4)
        print("SAVED MARKERS")