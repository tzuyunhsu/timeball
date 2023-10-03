import RPi.GPIO as GPIO
import time
import sys

# Pin definitions.
AIN1Pin = 6
AIN2Pin = 5

Topsensor_pin = 16
Midsensor_pin = 20
Bottomsensor_pin = 21


# Set the times in seconds
raise_halfway_time = 10
raise_top_time = 40
drop_time = 80
restart_time = 120

#The time measurements:
#12.3
#12.9
#25.6

#timeouts
raise_halfway_timeout = 13
raise_top_timeout = 13.6
drop_timeout = 26.3


# define a function to exit the program
def exit_program():
    GPIO.output(AIN1Pin, GPIO.LOW)
    GPIO.output(AIN2Pin, GPIO.LOW)
    sys.exit()

def setup():
    # Setup GPIO.
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(AIN1Pin, GPIO.OUT)
    GPIO.setup(AIN2Pin, GPIO.OUT)
    GPIO.setup(Topsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Midsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Bottomsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def forward_to_middle():
    start_time_1 = time.time()

    Midsensor_status = GPIO.input(Midsensor_pin)
    while Midsensor_status == 1:
        # Going forwards (going up) to the middle.
        GPIO.output(AIN1Pin, GPIO.HIGH)
        GPIO.output(AIN2Pin, GPIO.LOW)

        Midsensor_status = GPIO.input(Midsensor_pin)

        # Check if the elapsed time has surpassed the timeout.
        elapsed_time = time.time() - start_time_1
        if elapsed_time > raise_halfway_timeout:
            print("Timeout reached. Shutting down.")
            # Call a function to shutdown the system.
            exit_program()

    #stop
    GPIO.output(AIN1Pin, GPIO.LOW)

def forward_to_top():
    start_time_2 = time.time()
    Topsensor_status = GPIO.input(Topsensor_pin)
    while Topsensor_status == 1:
        # Going forwards (going up) to the top.
        GPIO.output(AIN1Pin, GPIO.HIGH)
        GPIO.output(AIN2Pin, GPIO.LOW)


        Topsensor_status = GPIO.input(Topsensor_pin)

        # Check if the elapsed time has surpassed the timeout.
        elapsed_time = time.time() - start_time_2
        if elapsed_time > raise_top_timeout:
            print("Timeout reached. Shutting down.")
            # Call a function to shutdown the system.
            exit_program()

    #stop
    GPIO.output(AIN1Pin, GPIO.LOW)

def backwards():
    start_time_3 = time.time()
    Bottomsensor_status = GPIO.input(Bottomsensor_pin)
    while Bottomsensor_status == 1:
        # Going backwards (going down).
        GPIO.output(AIN1Pin, GPIO.LOW)
        GPIO.output(AIN2Pin, GPIO.HIGH)

        Bottomsensor_status = GPIO.input(Bottomsensor_pin)

        # Check if the elapsed time has surpassed the timeout.
        elapsed_time = time.time() - start_time_3
        if elapsed_time > drop_timeout:
            print("Timeout reached. Shutting down.")
            # Call a function to shutdown the system.
            exit_program()

    GPIO.output(AIN2Pin, GPIO.LOW)

def sequence():
    GPIO.output(AIN1Pin, GPIO.LOW)
    GPIO.output(AIN2Pin, GPIO.LOW)
    #Flags
    raised_to_middle = False
    raised_to_top = False
    dropped = False
    restarted = False


    # Assume that the ball starts at the bottom position.
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        print("Elapsed Time:", elapsed_time)
        #print("Raised to Middle:", raised_to_middle)
        #print("Raised to Top:", raised_to_top)
        #print("Dropped:", dropped)
        #print("Restarted:", restarted)
        #print(elapsed_time)
        if elapsed_time >= raise_halfway_time and not raised_to_middle:  # Raise ball to halfway
            print("Triggering forward_to_middle()")
            forward_to_middle()
            raised_to_middle = True

        if elapsed_time  >= raise_top_time and not raised_to_top:
            print("Triggering forward_to_top()")

            forward_to_top()
            raised_to_top = True

        if elapsed_time >= drop_time and not dropped:
            print("Triggering backwards()")
            backwards()
            dropped = True

        if elapsed_time >= restart_time and not restarted:   # Restart the sequence
            print("Triggering restart")
            start_time = time.time()
            raised_to_middle = False
            raised_to_top = False
            dropped = False
            restarted = True


if __name__ == '__main__':
    setup()
    try:
        sequence()
    except KeyboardInterrupt:
        GPIO.cleanup()