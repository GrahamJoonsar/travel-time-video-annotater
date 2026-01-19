"""
vid_to_frames: This file takes in a video and selects specific frames from it to put into a specified folder

# Multithreaded video frame extraction pipeline
# Generated with assistance from ChatGPT (OpenAI), 2026
# Model: GPT-5.2
# Description: High-throughput producer–consumer pipeline for
#              video decoding, resizing, and parallel PNG saving.

TODO: Change this so that the numbers on the files are the true frame numbers.
"""

import cv2
import os
import threading
import queue

# ================= CONFIG =================

vid_path = r"C:\Users\gjoonsar3\Documents\travel-time-video-annotater\DJI_0022.MP4"
frame_step = 3
output_size = (1920, 1080)

NUM_RESIZE_WORKERS = 6   # CPU-bound
NUM_WRITE_WORKERS = 4    # I/O-bound
QUEUE_MAXSIZE = 64       # limits RAM usage

# =========================================

frame_folder_path = (
    os.path.dirname(vid_path)
    + "\\"
    + os.path.splitext(os.path.basename(vid_path))[0]
    + "_FRAMES\\"
)
os.makedirs(frame_folder_path, exist_ok=True)

read_queue = queue.Queue(maxsize=QUEUE_MAXSIZE)
write_queue = queue.Queue(maxsize=QUEUE_MAXSIZE)

STOP = object()


# ---------- Stage 1: Video Reader ----------

def reader():
    cap = cv2.VideoCapture(vid_path)
    frame_count = 0
    saved_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_step == 0:
            read_queue.put((saved_index, frame))
            saved_index += 1

        frame_count += 1

    cap.release()

    # signal resize workers to stop
    for _ in range(NUM_RESIZE_WORKERS):
        read_queue.put(STOP)


# ---------- Stage 2: Resizers ----------

def resizer():
    while True:
        item = read_queue.get()
        if item is STOP:
            write_queue.put(STOP)
            break

        idx, frame = item
        resized = cv2.resize(frame, output_size, interpolation=cv2.INTER_AREA)
        write_queue.put((idx, resized))


# ---------- Stage 3: Writers ----------

def writer():
    while True:
        item = write_queue.get()
        if item is STOP:
            break

        idx, frame = item
        out_path = os.path.join(frame_folder_path, f"{idx}.png")

        # PNG compression tuned for speed
        cv2.imwrite(
            out_path,
            frame,
            [cv2.IMWRITE_PNG_COMPRESSION, 3]
        )


# ================= RUN =================

print("PROCESSING VIDEO (MAX THROUGHPUT MODE)")

threads = []

threads.append(threading.Thread(target=reader, daemon=True))

for _ in range(NUM_RESIZE_WORKERS):
    threads.append(threading.Thread(target=resizer, daemon=True))

for _ in range(NUM_WRITE_WORKERS):
    threads.append(threading.Thread(target=writer, daemon=True))

for t in threads:
    t.start()

for t in threads:
    t.join()

print("STOPPED PROCESSING VIDEO")
