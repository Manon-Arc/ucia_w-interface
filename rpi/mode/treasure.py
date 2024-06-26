import logging
import cv2 as cv

# from controller.thymio.controller import ThymioController
# from vision.camera import Camera
# from tasks.base import Task
from rosa import Rosa
from time import sleep
# from vision import detect_objects


chosen = None
chosen_bonus = 0
_home_distance = 0.0
_scan_distance = 0.0
_scan_speed = 0.03
logger = logging.getLogger(__name__)

def set_led_color(rosa, color):
    """Set LED color based on the robot's current state."""
    if color == 'blue':
        rosa.leds.bottom.left.color = [0, 0, 32] 
        rosa.leds.bottom.right.color = [0, 0, 32]
    elif color == 'red':
        rosa.leds.bottom.left.color = [32, 0, 0] 
        rosa.leds.bottom.right.color = [32, 0, 0]
    elif color == 'green':
        rosa.leds.bottom.left.color = [0, 32, 0]
        rosa.leds.bottom.right.color = [0, 32, 0]

def flush(rosa):
    """Reset chosen, flush image buffer."""
    global _home_distance
    global chosen
    global chosen_bonus
    logger.info(f"COLLECTOR flush buffers")
    chosen = None
    chosen_bonus = 0
    _home_distance = 0.0
    for i in range(3):
        # _ = rosa.camera.last_frame
        sleep(0.2)

def set_speed(rosa, ls, rs):
    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs

def choose_object(rosa, threshold=0.4):
    """
    Choose an object according to policy.
    Here, the object with the highest confidence.
    """
    found = None
    
    # print(rosa.camera.last_detection)
    
    print(rosa.camera)
    if rosa.camera.last_detection is None:
        set_led_color(rosa, 'red')
        rosa.sound.system(1)
        return []
    
    try:
        print("last_detection", rosa.camera.last_detection)
        found = desirable(rosa.camera.last_detection)
    except ValueError:
        logger.warn("COLLECTOR ignore exception in Yolo3 rectangle drawing!")
    if not found:
        return []
    object = sorted(found, key=lambda v: v.confidence)[0]
    if object.confidence < threshold:
        return []
    logger.info(
        f"COLLECTOR choosing {object.label} at {object.center} score {object.confidence}"
    )
    return object

def desirable(objects):
    """Decide whether we want this kind of object."""
    print(objects)
    return [x for x in objects if (x.label == "star" or x.label== "cube" or x.label == "ball")]

def scan(rosa):
    """Look around, turning slowly clockwise."""
    # self.logger.info(f"COLLECTOR scanning, dist {self._scan_distance}")
    global _scan_distance
    global _scan_speed
    if abs(_scan_distance) > 100:
        _scan_speed = -_scan_speed
    set_speed(rosa, _scan_speed, -_scan_speed * 0.2)
    _scan_distance += _scan_speed / 0.03 * 2
    set_led_color(rosa, 'blue')

def stop(rosa):
    """Stop turning."""
    set_speed(rosa, 0, 0)

def track(rosa, object, multiplier=0.6):
    """
    Turn towards chosen object.
    Convert delta ±170 ~ ±45° ~ ± 900 ms at speed 0.25
    """
    heading = object.center[0] - 170
    speed = 0.25 if heading > 0 else -0.25
    duration = abs(heading / 170.0 * 0.900 * multiplier)
    logger.info(
        f"COLLECTOR tracking {object.label} object at heading {heading}"
    )
    set_speed(rosa, speed, -speed)
    sleep(duration)
    stop(rosa)

def is_close(object, multiplier=0.4, threshold=-10):
    """Do we think this object is close enough to grab?"""
    global _home_distance
    azimuth = (200 - object.center[0]) * multiplier
    decision = azimuth < threshold or _home_distance > 2
    logger.info(
        f"COLLECTOR is {object.label} at az {azimuth} ({_home_distance} from home) close? {'Yes' if decision else 'No'}"
    )
    return decision

def grab(rosa, object, backup=2.0):
    """Grab the object and bring it back home."""
    logger.info(
        f"COLLECTOR grab {object.label} then back up additional {backup}"
    )
    set_led_color(rosa, 'green')
    set_speed(rosa, 0.2, 0.2)
    sleep(6)
    set_speed(rosa,-0.25, 0.25)
    sleep(3.6)
    set_speed(rosa,0.20, 0.20)
    sleep(2.0 + backup)
    set_speed(rosa,-0.2, -0.2)
    sleep(1)
    set_speed(rosa,0.30, -0.30)
    sleep(3.0)
    set_speed(rosa, 0, 0)
    rosa.sound.system(4)
    set_led_color(rosa, 'blue')


def good_candidate(chosen_obj):
    """Remember whether chosen_obj and chosen agree about the object."""
    global chosen
    global chosen_bonus
    if chosen:
        if chosen and chosen.label == chosen.label:
            chosen_bonus += 1
            logger.info(
                f"COLLECTOR good {chosen.label} bonus {chosen_bonus}"
            )
        return True
    if chosen:
        logger.info(f"COLLECTOR lost {chosen.label}")
    chosen = None
    chosen_bonus = 0
    return False

if __name__ == '__main__':
    rosa = Rosa('rosa.local')
    
    while True:
        # img = rosa.camera.last_frame
        # if img is None:
        #     continue

        chosen = choose_object(rosa)
        print(chosen)
        
        if not good_candidate(chosen) or chosen_bonus < 0:
            # Scan clockwise
            scan(rosa)
            flush(rosa)
            continue
        
        if chosen.confidence > 0.7 or chosen_bonus > 2:
            print(f"COLLECTOR high confidence for {chosen.label}")

            track(rosa, chosen)
            if is_close(chosen):
                grab(rosa, chosen, backup=_home_distance)
                flush(rosa)
            else:
                set_speed(rosa, 0.1, 0.1)
                # Polling interval imposes backup ~ 1200 ms @
                _home_distance += 0.3
        else:
            # Try to stabilize choice
            set_speed(rosa, 0.06, 0.06)
            chosen_bonus -= 1
            logger.info(
                f"COLLECTOR try to focus on {chosen.label}, "
                f"bonus now {chosen_bonus}"
            )

        sleep(0.016)