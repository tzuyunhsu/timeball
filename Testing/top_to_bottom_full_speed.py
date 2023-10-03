import RPi.GPIO as GPIO


# Pin definitions.
AIN1Pin = 6
AIN2Pin = 5

Topsensor_pin = 16
Midsensor_pin = 20
Bottomsensor_pin = 21


def setup():
    # Setup GPIO.
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(AIN1Pin, GPIO.OUT)
    GPIO.setup(AIN2Pin, GPIO.OUT)
    GPIO.setup(Topsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Midsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Bottomsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)



def forward():
    Topsensor_status = GPIO.input(Topsensor_pin)
    while Topsensor_status == 1:
        # Going forwards (going up) to the top.
        GPIO.output(AIN1Pin, GPIO.HIGH)
        GPIO.output(AIN2Pin, GPIO.LOW)


        Topsensor_status = GPIO.input(Topsensor_pin)


        # Check for the middle sensor trigger
        if GPIO.input(Midsensor_pin) == 0:
            print("Middle sensor triggered")


def backwards():
    Bottomsensor_status = GPIO.input(Bottomsensor_pin)
    while Bottomsensor_status == 1:
        # Going backwards (going down).
        GPIO.output(AIN1Pin, GPIO.LOW)
        GPIO.output(AIN2Pin, GPIO.HIGH)

        Bottomsensor_status = GPIO.input(Bottomsensor_pin)

        # Check for the middle sensor trigger
        if GPIO.input(Midsensor_pin) == 0:
            print("Middle sensor triggered")


def sequence():
    # Assume that the ball starts at the bottom position.
    while True:
        forward()
        backwards()



if __name__ == '__main__':
    setup()
    try:
        sequence()
    except KeyboardInterrupt:
        GPIO.cleanup()