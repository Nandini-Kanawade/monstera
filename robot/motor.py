# L298N control
import RPi.GPIO as GPIO

# L298N pin mapping — update these to match your wiring
IN1 = 17  # Motor A direction 1
IN2 = 18  # Motor A direction 2
IN3 = 22  # Motor B direction 1
IN4 = 23  # Motor B direction 2
ENA = 24  # Motor A enable (PWM speed)
ENB = 25  # Motor B enable (PWM speed)

SPEED = 70  # Default speed 0-100


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in [IN1, IN2, IN3, IN4, ENA, ENB]:
        GPIO.setup(pin, GPIO.OUT)

    global pwm_a, pwm_b
    pwm_a = GPIO.PWM(ENA, 1000)
    pwm_b = GPIO.PWM(ENB, 1000)
    pwm_a.start(0)
    pwm_b.start(0)


def _set_speed(speed=SPEED):
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)


def forward(speed=SPEED):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    _set_speed(speed)


def backward(speed=SPEED):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    _set_speed(speed)


def turn_left(speed=SPEED):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    _set_speed(speed)


def turn_right(speed=SPEED):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    _set_speed(speed)


def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    _set_speed(0)


def cleanup():
    stop()
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
