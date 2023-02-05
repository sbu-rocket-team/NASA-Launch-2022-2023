import time
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN)
GPIO.setup(6, GPIO.IN)
GPIO.setup(7, GPIO.OUT) # motor control GPIO pin

counts_per_rotation = 12
position = 0
gear_ratio = 298

speeds = []
times = []

def read_drv5013(channel):
    global position
    if channel == 5:
        if GPIO.input(5) == GPIO.HIGH:
            if GPIO.input(6) == GPIO.LOW:
                position += 1
            else:
                position -= 1
    return position / counts_per_rotation

GPIO.add_event_detect(5, GPIO.RISING, callback=read_drv5013)

start_time = time.time()

degree_of_rotation = 90 # desired degree of rotation
desired_position = degree_of_rotation * (counts_per_rotation / 360) * gear_ratio

GPIO.output(7, GPIO.HIGH) # start the motor

while True:
    elapsed_time = time.time() - start_time
    rotations_per_second = (position / counts_per_rotation) / elapsed_time
    speed = rotations_per_second / gear_ratio
    speeds.append(speed)
    times.append(elapsed_time)
    if position >= desired_position:
        break
    time.sleep(0.1)

GPIO.output(7, GPIO.LOW) # stop the motor

plt.plot(times, speeds)
plt.xlabel("Time (s)")
plt.ylabel("Speed (RPM)")
plt.title("Motor Speed Over Time")
plt.show()