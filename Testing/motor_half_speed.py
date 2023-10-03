import RPi.GPIO as GPIO


# Pin definitions
pwmPin_1 = 6
pwmPin_2 = 5

GPIO.setwarnings(False)

# Duty cycle and frequency
duty = 50
frequency = 50

def setup():
    # Set up GPIO
    GPIO.setmode(GPIO.BCM)

    # Set up the pins
    GPIO.setup(pwmPin_1, GPIO.OUT)
    GPIO.setup(pwmPin_2, GPIO.OUT)

    # Set up the PWM channel
    global pwm_1
    global pwm_2
    pwm_1 = GPIO.PWM(pwmPin_1, frequency)
    pwm_2 = GPIO.PWM(pwmPin_2, frequency)
def backwards():
    # Going forwards (going up)

    pwm_1.start(duty)
    pwm_2.start(0)
def forward():
    # Going backwards (going down)
    pwm_2.start(duty)
    pwm_1.start(0)
def sequence():
    while True:
        #forward()
        backwards()

def destroy():
    # Clean up the GPIO pins
    GPIO.cleanup()
    # Stop the motor
    pwm_1.stop()
    pwm_2.stop()

if __name__ == '__main__':
    # Set up the GPIO pins
    setup()
    try:
        # Run the sequence
        sequence()
    except KeyboardInterrupt:
        # Clean up the GPIO pins on interrupt
        destroy()
