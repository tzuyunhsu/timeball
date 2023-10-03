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

def forward():
    Topsensor_status = GPIO.input(Topsensor_pin)
    # Check for the top sensor trigger
    if GPIO.input(Topsensor_pin) == 0:
        print("Top sensor triggered!")
        time.sleep(0.3)
    while Topsensor_status == 1:
        # Going forwards (going up) to the top.
        GPIO.output(AIN1Pin, GPIO.HIGH)
        GPIO.output(AIN2Pin, GPIO.LOW)
        pwm.start(duty)

        Topsensor_status = GPIO.input(Topsensor_pin)


        # Check for the middle sensor trigger
        if GPIO.input(Midsensor_pin) == 0:
            print("Middle sensor triggered!")
            time.sleep(0.3)

    print("Top sensor reached!")
    pwm.ChangeDutyCycle(0)  # The ball is already on top.

def backwards():
    Bottomsensor_status = GPIO.input(Bottomsensor_pin)
    # Check for the bottom sensor trigger
    if GPIO.input(Bottomsensor_pin) == 0:
        print("Bottom sensor triggered!")
        time.sleep(0.3)
    while Bottomsensor_status == 1:
        # Going backwards (going down).
        GPIO.output(AIN1Pin, GPIO.LOW)
        GPIO.output(AIN2Pin, GPIO.HIGH)
        pwm.start(duty)

        Bottomsensor_status = GPIO.input(Bottomsensor_pin)

        # Check for the middle sensor trigger
        if GPIO.input(Midsensor_pin) == 0:
            print("Middle sensor triggered")
            time.sleep(0.3)

    print("Bottom sensor reached!")
    pwm.ChangeDutyCycle(0)

def sequence(cycle):
    # Assume that the ball starts at the bottom position.
    while cycle > 0:
        forward()
        backwards()
        destroy()
        print("One cycle is done!")
        cycle = cycle - 1

def destroy():
    pwm.stop()

if __name__ == '__main__':
    setup()
    try:
        cycle = 1 
        sequence(cycle)
    except KeyboardInterrupt:
        destroy()
        GPIO.cleanup()
