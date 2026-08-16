# yolo_camera.py
import argparse
import sys
import time
import cv2
from ultralytics import YOLO
import torch
import os

def parse_args():
    p = argparse.ArgumentParser(description="YOLO live detection (no ROS)")
    p.add_argument("--model", default="yolo11n.pt", help="YOLO model path/name")
    p.add_argument("--source", default="/dev/video2", help="Camera index or path (e.g., 0, 1, or /dev/video0)")
    p.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    p.add_argument("--fps", type=float, default=10.0, help="Target processing FPS")
    return p.parse_args()

def open_capture(source):
    # Allow numeric camera index or string device path
    if isinstance(source, str) and source.isdigit():
        source = int(source)
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("❌ Cannot open camera/source:", source, file=sys.stderr)
        sys.exit(1)
    return cap

def main():
    args = parse_args()

    torch.set_num_threads(1)
    os.environ["OMP_NUM_THREADS"]="1"
    os.environ["MKL_NUM_THREADS"]="1"

    # Load model
    try:
        model = YOLO(args.model)
        model.to('cpu')
    except Exception as e:
        print(f"❌ Failed to load model '{args.model}': {e}", file=sys.stderr)
        sys.exit(1)

    cap = open_capture(args.source)
    window_name = "YOLO Detection (press 'q' to quit)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    frame_interval = 1.0 / max(args.fps, 0.1)  # seconds per frame
    try:
        while True:
            start_t = time.time()
            ok, frame = cap.read()
            if not ok:
                print("❌ Can't receive frame; exiting...", file=sys.stderr)
                break

            # Inference
            results = model(frame, conf=args.conf, verbose=False)
            annotated = results[0].plot()

            cv2.imshow(window_name, annotated)

            # Exit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("🛑 Quitting...")
                break

            # Simple pacing toward target FPS
            elapsed = time.time() - start_t
            remaining = frame_interval - elapsed
            if remaining > 0:
                time.sleep(remaining)

    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user.")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()