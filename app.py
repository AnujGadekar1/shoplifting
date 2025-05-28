from ultralytics import YOLO
import cv2

# Load trained YOLO model
model = YOLO("shoplifting_detector.pt")  

# Open video file
video_path = r"C:\Users\anujg\Downloads\Work_1\Shop\istockphoto-1391833001-640_adpp_is.mp4"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection
    results = model(frame)

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
            conf = box.conf[0].item()  # Confidence score
            cls = int(box.cls[0].item())  # Class index
            label = model.names[cls]  # Get class name

            # Define box color
            color = (0, 255, 0) if label == "normal" else (0, 0, 255)

            # Draw bounding box & confidence
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{label}: {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
