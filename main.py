#imports
import cv2
import mediapipe as mp
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(BASE_DIR, 'test/multiple.jpg')

#Function for face detection

def process_image(img, face_detection):
    H, W, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    out = face_detection.process(img_rgb)
    if out.detections is not None:
        for detection in out.detections:
            bbox = detection.location_data.relative_bounding_box
            x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height

            x1 = int(x1 * W) 
            y1 = int(y1 * H)
            w = int(w * W)
            h = int(h * H)

            face_roi = img[y1:y1+h, x1:x1+w]
            if face_roi.size != 0:
                face_roi = cv2.GaussianBlur(face_roi, (99, 99), 30)
                img[y1:y1+h, x1:x1+w] = face_roi

            img = cv2.rectangle(img, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 10)
    return img

args = argparse.ArgumentParser()
args.add_argument("--mode", default="image")
args.add_argument("--file_path", default=img_path)
args = args.parse_args()

mp_face_detection = mp.solutions.face_detection
with mp_face_detection.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.5) as face_detection:
    if args.mode == "image":
        img = cv2.imread(args.file_path)
        if img is None:
            raise ValueError("Image not found. Check test.jpg path.")
        img = process_image(img, face_detection)
        cv2.imshow('face', img)
        cv2.waitKey(0)
    elif args.mode == "webcam":
            webcam = cv2.VideoCapture(0)
            while True:
                ret, frame = webcam.read()
                if not ret:
                    break
                frame = process_image(frame, face_detection)
                cv2.imshow('frame', frame)
                if cv2.waitKey(40) & 0xFF == ord('q'):
                    break
            webcam.release()
            cv2.destroyAllWindows()

            
    
