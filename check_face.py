import os
import face_recognition
import cv2
import numpy as np

known_face_encodings = []
known_face_names = []
attendance = []
print("Check faces loading...")
print("Press q for exit")
if not os.path.exists("Known_faces"):
    os.makedirs("Known_faces")
for file in os.listdir("Known_faces"):
    if file.lower().endswith((".jpg", ".jpeg", ".png")):
        image = face_recognition.load_image_file(f"Known_faces/{file}")
        face_encodings = face_recognition.face_encodings(image)
        if not face_encodings:
            print(f"Skip {file}: no face found")
            continue
        encoding = face_encodings[0]
        known_face_encodings.append(encoding)

        file_name = os.path.splitext(file)[0]
        if "_" in file_name:
            person_name, student_id = file_name.rsplit("_", 1)
            display_name = f"{person_name} ID-{student_id}"
        else:
            display_name = file_name
        known_face_names.append(display_name)
video_capture = cv2.VideoCapture(0)
while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locate = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locate)

    for (top, right, bottom, left), face_encoding in zip(face_locate, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            if name not in attendance:
                attendance.append(name)
                print(f"Checked in: {name}")
        top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, bottom - 10), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 255, 255), 2)
    cv2.imshow("Attendance system", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("Exit")
        break
video_capture.release()
cv2.destroyAllWindows()

 
