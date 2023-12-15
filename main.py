import cv2
import pytube
import time
import keyboard
from playsound import playsound
import threading

def get_video_link():
    while True:
        video_link = input("Enter YouTube video link: ")
        try:
            youtube = pytube.YouTube(video_link)
            return youtube.streams.get_highest_resolution().url
        except pytube.exceptions.RegexMatchError:
            print("Invalid YouTube video link. Please try again.")

def play_audio(audio_file):
    threading.Thread(target=playsound, args=(audio_file,)).start()

def main():
    video_url = get_video_link()
    cap = cv2.VideoCapture(video_url)
    if not cap.isOpened():
        print("Error opening video stream or file.")
        return

    # Get the width and height of the video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a resizable window
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Video', width, height)

    # Set the initial position to the beginning of the video
    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

    frame_pos = 0
    frame_step = 4  # Number of frames to jump when user presses 'a' or 'd'
    max_frame = 0

    duration = 120  # Countdown duration in seconds

    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Video', frame)

        played = False

        while not keyboard.is_pressed('a') and not keyboard.is_pressed('d'):
            # Calculate the remaining time for the countdown
            elapsed_time = int(time.time() - start_time)
            remaining_time = max(0, duration - elapsed_time)

            # Clear the frame before drawing the timer text
            frame_copy = frame.copy()

            # Draw the timer text on the frame
            timer = f"Timer: {remaining_time} sec"
            cv2.putText(frame_copy, timer, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            frame_number = f"Frame: {frame_pos}"
            cv2.putText(frame_copy, frame_number, (width - 160, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            cv2.imshow('Video', frame_copy)
            if remaining_time <= 0 and not played:
                play_audio("Alarm1.wav")
                played = True
            cv2.waitKey(1)
            if keyboard.is_pressed('q'):
                break

        if keyboard.is_pressed('a'):
            frame_pos = max(0, frame_pos - frame_step)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            
            time.sleep(0.5)
        elif keyboard.is_pressed('d'):
            frame_pos = min(cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1, frame_pos + frame_step)
            print ("Frame_pos : ", frame_pos)
            print ("max_frame : ", max_frame)
            if frame_pos > max_frame:
                max_frame = frame_pos
                start_time = time.time()  # Update start time on key press
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)            
            time.sleep(0.5)
        elif keyboard.is_pressed('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
