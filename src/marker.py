
"""
Marker: This class represents a point in a video at a particular time and screen coordinates

TODO: Create class body
"""

# Used for reading and writing the marker files
import pandas as pd

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
    
    def display(self):
        print(f"{self.id}: ({self.pos[0]}, {self.pos[1]}) | #{self.frame_num} | => {self.paired_id}")

class Marker_Manager:
    def __init__(self):
        self.markers = {}
    
    # Your input should be a properly formatted CSV file with marker data
    def read_markers(self, marker_path: str):
        marker_df = pd.read_csv(marker_path)
        for _, row in marker_df.iterrows():
            self.markers[row['id']] = Marker(
                (row['x'], row['y']),
                row['frame_num'],
                row['id'],
                row['paired_id']
            )


    # Writes the marker dataframe to the specified CSV path
    def write_markers(self, marker_path: str):
        marker_df = pd.DataFrame({'id': [], 'paired_id': [], 'x': [], 'y': [], 'frame_num': []})
        for _, marker in self.markers.items():
            marker_df.loc[len(marker_df)] = [
                marker.id,
                marker.paired_id,
                marker.pos[0],
                marker.pos[1],
                marker.frame_num
            ]
        marker_df.to_csv(marker_path)
            

# testing
if __name__ == '__main__':
    mm = Marker_Manager()
    mm.read_markers('test.csv')
    for k, v in mm.markers.items():
        v.display()