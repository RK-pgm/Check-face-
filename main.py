import cv2
import os
if not os.path.exists("Known_faces"):
    os.makedirs("Known_faces")
name = input("Enter your name and surname: ")
student_ID = input("Enter your student ID: ")
video_capture = cv2.VideoCapture(0)
print("look at the camera and press q for capture or press q for exit")

while True:
    ret, frame = video_capture.read()
    cv2.imshow("Registering", frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord("s"):
        filename = f"Known_faces/{name}_{student_ID}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename} finish!")
        break
    elif key & 0xFF == ord("q"):
        print("Exit")
        break
video_capture.release()
cv2.destroyAllWindows()

        