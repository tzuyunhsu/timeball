import RPi.GPIO as GPIO
import time

# Pin definitions.
pwmPin = 26
AIN1Pin = 5
AIN2Pin = 6

Topsensor_pin = 16
Midsensor_pin = 20
Bottomsensor_pin = 21

duty = 50
frequency = 50

def setup():
    # Setup GPIO.
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(pwmPin, GPIO.OUT)
    GPIO.setup(AIN1Pin, GPIO.OUT)
    GPIO.setup(AIN2Pin, GPIO.OUT)
    GPIO.setup(Topsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Midsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Bottomsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    global pwm
    pwm = GPIO.PWM(pwmPin, frequency)

def sensor():
    # Top sensor triggered
    if GPIO.input(Topsensor_pin) == 0:
        print("Top sensor triggered!")
        time.sleep(0.3)
    # Mid sensor triggered
    if GPIO.input(Midsensor_pin) == 0:
        print("Mid sensor triggered!")
        time.sleep(0.3)
    # Bottom sensor triggered
    if GPIO.input(Bottomsensor_pin) == 0:
        print("Bottom sensor triggered!")
        time.sleep(0.3)

def test():
    # Assume that the ball starts at the bottom position.
    while True:
        sensor()

def destroy():
    pwm.stop()

if __name__ == '__main__':
    setup()
    try:
       test()
    except KeyboardInterrupt:
        destroy()
        GPIO.cleanup()
