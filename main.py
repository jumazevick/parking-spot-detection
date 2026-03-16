import cv2
import pickle
import os
from detection.spot_detector import is_occupied

# Global variables
drawing = False
start_point = (-1, -1)
end_point = (-1, -1)
parking_spots = []

def draw_rectangle(event, x, y, flags, param):
    global drawing, start_point, end_point, parking_spots

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            end_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        # Add the rectangle to parking spots
        parking_spots.append((start_point, end_point))

def main():
    video_path = 'data/parking_vid_loop.mp4'
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video")
        return

    # Read the first frame
    ret, frame = cap.read()
    if not ret:
        print("Error reading frame")
        return

    cap.release()

    # Open a window of the first frame and set mouse callback
    cv2.namedWindow('Define Parking Spots')
    cv2.setMouseCallback('Define Parking Spots', draw_rectangle)

    print("Instructions:")
    print("- Click and drag to draw rectangles for parking spots.")
    print("- Press 'c' to clear all spots.")
    print("- Press 's' to save spots and exit.")
    print("- Press 'q' to quit without saving.")

    while True:
        temp_frame = frame.copy()

        # Draw existing rectangles
        for spot in parking_spots:
            cv2.rectangle(temp_frame, spot[0], spot[1], (0, 255, 0), 2)

        # Draw current rectangle being drawn
        if drawing and start_point != (-1, -1) and end_point != (-1, -1):
            cv2.rectangle(temp_frame, start_point, end_point, (255, 0, 0), 2)

        cv2.imshow('Define Parking Spots', temp_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            parking_spots.clear()
        elif key == ord('s'):
            # Save parking spots
            with open('parking_spots.pkl', 'wb') as f:
                pickle.dump(parking_spots, f)
            print(f"Saved {len(parking_spots)} parking spots to parking_spots.pkl")
            cv2.destroyWindow('Define Parking Spots')
            # Proceed to detection
            detect_occupancy(video_path, parking_spots)
            break

    cv2.destroyAllWindows()

def detect_occupancy(video_path, spots):
    if not spots:
        print("No parking spots defined.")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video for detection")
        return

    print("Starting occupancy detection. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            # If video ends, loop back (assuming it's a loop video)
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        statuses = []
        for spot in spots:
            x1, y1 = spot[0]
            x2, y2 = spot[1]
            # Ensure coordinates are in order
            x_min, x_max = min(x1, x2), max(x1, x2)
            y_min, y_max = min(y1, y2), max(y1, y2)

            # Crop the spot
            spot_img = frame[y_min:y_max, x_min:x_max]

            # Determine if occupied using the detection module
            occupied = is_occupied(spot_img)
            statuses.append(occupied)
            color = (0, 0, 255) if occupied else (0, 255, 0)  # Red for occupied, Green for free

            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)

        # Count free spots
        free_count = statuses.count(False)
        occupied_count = statuses.count(True)

        # Add text annotations
        cv2.putText(frame, "Green: Free, Red: Occupied", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Total Spots: {len(statuses)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Free Spots: {free_count}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow('Parking Spot Detection', frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
