import cv2 as cv

from rosa import Rosa


if __name__ == '__main__':
    rosa = Rosa('rosa.local', local_robot=False)

    while True:
        # We can access the last frame from the robot camera using:
        # It will automatically updated with the most up-to-date image
        img = rosa.camera.last_frame

        if img is None:
            continue

        cv.imshow('rosa', img)
        cv.waitKey(20)
