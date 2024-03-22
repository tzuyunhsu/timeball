import RPi.GPIO as GPIO


# Pin definitions
AIN1Pin = 6
AIN2Pin = 5

GPIO.setwarnings(False)

def setup():
    # Set up GPIO
    GPIO.setmode(GPIO.BCM)

    # Set up the pins
    GPIO.setup(AIN1Pin, GPIO.OUT)
    GPIO.setup(AIN2Pin, GPIO.OUT)


def backward():
    # Going forward (going up)

    GPIO.output(AIN1Pin, GPIO.HIGH)
    GPIO.output(AIN2Pin, GPIO.LOW)

def forward():
    # Going backward (going down)
    GPIO.output(AIN1Pin, GPIO.LOW)
    GPIO.output(AIN2Pin, GPIO.HIGH)


def sequence():
    while True:
        forward()

def destroy():
    # Clean up the GPIO pins
    GPIO.cleanup()

if __name__ == '__main__':
    # Set up the GPIO pins
    setup()
    try:
        # Run the sequence
        sequence()
    except KeyboardInterrupt:
        # Clean up the GPIO pins on interrupt
        destroy()