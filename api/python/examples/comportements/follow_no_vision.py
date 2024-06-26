from rosa import Rosa

import time

base_speed = 0.1
turn_ratio = 0.9
THRESHOLD_DIFFERENCE = 250
following_left_edge = True

timer = time.time()

def set_speed(rosa, ls, rs):
    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs

def set_straight(rosa):
    set_speed(rosa, base_speed, base_speed)

def set_right(rosa):
    left_wheel_speed = base_speed * (1 + turn_ratio)
    right_wheel_speed = base_speed * (1 - turn_ratio)

    set_speed(rosa,left_wheel_speed, right_wheel_speed)

def set_left(rosa):
    left_wheel_speed = base_speed * (1 - turn_ratio)
    right_wheel_speed = base_speed * (1 + turn_ratio)
    
    set_speed(rosa,left_wheel_speed, right_wheel_speed)


if __name__ == '__main__':
    rosa = Rosa('rosa.local', local_robot=False)
    
    rosa.leds.bottom.left.color = [0, 32, 32] 
    rosa.leds.bottom.right.color = [0, 32, 32]
    timer = time.time()
    while True:
        reflected = rosa.ground_reflected
        left_sensor = reflected[0]
        right_sensor = reflected[1]

        difference = abs(left_sensor - right_sensor)
        print(difference)
        print(left_sensor, right_sensor)
        print(following_left_edge)
        #set_speed(rosa, 0.0,0.0)
        #continue
        
        if difference < THRESHOLD_DIFFERENCE:
            if following_left_edge:
                set_right(rosa)
            else:
                set_left(rosa)
        else:
            set_straight(rosa)
            following_left_edge = left_sensor > right_sensor

        time.sleep(0.1)
        