import RPi.GPIO as GPIO


# Pin definitions.
pwmPin_1 = 6
pwmPin_2 = 5

Topsensor_pin = 16
Midsensor_pin = 20
Bottomsensor_pin = 21

duty = 50
frequency = 50

def setup():
    # Setup GPIO.
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(pwmPin_1, GPIO.OUT)
    GPIO.setup(pwmPin_2, GPIO.OUT)
    GPIO.setup(Topsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Midsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Bottomsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Set up the PWM channel
    global pwm_1
    global pwm_2
    pwm_1 = GPIO.PWM(pwmPin_1, frequency)
    pwm_2 = GPIO.PWM(pwmPin_2, frequency)

def forward():
    Topsensor_status = GPIO.input(Topsensor_pin)
    while Topsensor_status == 1:
        # Going forwards (going up) to the top.
        pwm_1.start(duty)
        pwm_2.start(0)

        Topsensor_status = GPIO.input(Topsensor_pin)


        # Check for the middle sensor trigger
        if GPIO.input(Midsensor_pin) == 0:
            print("Middle sensor triggered")

    pwm_1.ChangeDutyCycle(0)  # The ball is already on top.
    pwm_2.ChangeDutyCycle(0)  # The ball is already on top.
def backwards():
    Bottomsensor_status = GPIO.input(Bottomsensor_pin)
    while Bottomsensor_status == 1:
        # Going backwards (going down).
        pwm_2.start(duty)
        pwm_1.start(0)

        Bottomsensor_status = GPIO.input(Bottomsensor_pin)

        # Check for the middle sensor trigger
        if GPIO.input(Midsensor_pin) == 0:
            print("Middle sensor triggered")

    pwm_1.ChangeDutyCycle(0)
    pwm_2.ChangeDutyCycle(0)

def sequence():
    # Assume that the ball starts at the bottom position.
    while True:
        forward()
        backwards()

def destroy():
    pwm_1.stop()
    pwm_2.stop()

if __name__ == '__main__':
    setup()
    try:
        sequence()
    except KeyboardInterrupt:
        destroy()
        GPIO.cleanup()