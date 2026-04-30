# ultrasonic + servo
import RPi.GPIO as GPIO
import time

# Pin config — update to match your wiring
TRIG = 5       # Ultrasonic trigger pin
ECHO = 6       # Ultrasonic echo pin
SERVO_PIN = 13  # Servo signal pin

# Servo sweep range
SERVO_MIN = 2.5   # ~0 degrees
SERVO_MAX = 12.5  # ~180 degrees
SERVO_MID = 7.5   # ~90 degrees (center, facing forward)


def setup():
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    global servo
    servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz for servo
    servo.start(SERVO_MID)
    time.sleep(0.5)


def get_distance():
    """Returns distance in cm using HC-SR04."""
    GPIO.output(TRIG, False)
    time.sleep(0.01)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

    timeout = time.time() + 0.04  # 40ms timeout

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None

    duration = pulse_end - pulse_start
    distance = round(duration * 17150, 2)  # convert to cm

    if distance < 2 or distance > 400:
        return None  # out of sensor range

    return distance


def set_angle(angle):
    """Rotate servo to given angle (0-180 degrees)."""
    duty = SERVO_MIN + (angle / 180.0) * (SERVO_MAX - SERVO_MIN)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.3)  # wait for servo to settle


def sweep():
    """
    Sweep servo from 0 to 180 degrees and back.
    Returns list of (angle, distance_cm) tuples.
    """
    readings = []

    for angle in range(0, 181, 15):  # step every 15 degrees
        set_angle(angle)
        dist = get_distance()
        readings.append((angle, dist))

    for angle in range(180, -1, -15):  # sweep back
        set_angle(angle)
        dist = get_distance()
        readings.append((angle, dist))

    set_angle(90)  # return to center
    return readings


def cleanup():
    servo.stop()
