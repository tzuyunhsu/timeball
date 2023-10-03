import RPi.GPIO as GPIO
import time
import sys
import pygame

pygame.init()

# Set the width and height of the screen (optional).
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))


# Pin definitions.
pwmPin = 26
AIN1Pin = 5
AIN2Pin = 6

Topsensor_pin = 16
Midsensor_pin = 20
Bottomsensor_pin = 21

# Set the times in seconds
raise_halfway_time = 10
raise_top_time = 20
drop_time = 30
restart_time = 40

#timeouts
raise_halfway_timeout = 20
raise_top_timeout = 20
drop_timeout = 20




# Two buttons of the TFTScreen can act as Hall Effect Sensors
duty = 50
frequency = 50


def display_text(text):
    font = pygame.font.Font(None, 36)  # Choose a font and size.
    text_surface = font.render(text, True, (255, 255, 255))  # Create a surface for the text.
    screen.fill((0, 0, 0))  # Clear the screen.
    text_rect = text_surface.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()  # Update the screen.


# define a function to exit the program
def exit_program():
    sys.exit()

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

def forward_to_middle():
    display_text("Moving ball to middle...")
    start_time_1 = time.time()

    Midsensor_status = GPIO.input(Midsensor_pin)
    while Midsensor_status == 1:
        # Going forwards (going up) to the middle.
        GPIO.output(AIN1Pin, GPIO.HIGH)
        GPIO.output(AIN2Pin, GPIO.LOW)
        pwm.start(duty)

        Midsensor_status = GPIO.input(Midsensor_pin)

        # Check if the elapsed time has surpassed the timeout.
        elapsed_time = time.time() - start_time_1
        if elapsed_time > raise_halfway_timeout:
            print("Timeout reached. Shutting down.")
            # Call a function to shutdown the system.
            exit_program()
    pwm.ChangeDutyCycle(0)  # The ball is already at the middle.

def forward_to_top():
    display_text("Moving ball to top...")
    start_time_2 = time.time()
    Topsensor_status = GPIO.input(Topsensor_pin)
    while Topsensor_status == 1:
        # Going forwards (going up) to the top.
        GPIO.output(AIN1Pin, GPIO.HIGH)
        GPIO.output(AIN2Pin, GPIO.LOW)
        pwm.start(duty)

        Topsensor_status = GPIO.input(Topsensor_pin)

    # Check if the elapsed time has surpassed the timeout.
    elapsed_time = time.time() - start_time_2
    if elapsed_time > drop_timeout:
        print("Timeout reached. Shutting down.")
        # Call a function to shutdown the system.
        exit_program()

    pwm.ChangeDutyCycle(0)  # The ball is already on top.

def backwards():
    display_text("Moving ball down...")
    start_time_3 = time.time()
    Bottomsensor_status = GPIO.input(Bottomsensor_pin)
    while Bottomsensor_status == 1:
        # Going backwards (going down).
        GPIO.output(AIN1Pin, GPIO.LOW)
        GPIO.output(AIN2Pin, GPIO.HIGH)
        pwm.start(duty)

        Bottomsensor_status = GPIO.input(Bottomsensor_pin)

    # Check if the elapsed time has surpassed the timeout.
    elapsed_time = time.time() - start_time_3
    if elapsed_time > raise_halfway_timeout:
        print("Timeout reached. Shutting down.")
        # Call a function to shutdown the system.
        exit_program()

    pwm.ChangeDutyCycle(0)

def sequence():
    display_text("Waiting for 5 minutes till noon")
    start_time = time.time()
    #Flags
    raised_to_middle = False
    raised_to_top = False
    dropped = False
    restarted = False

    # Assume that the ball starts at the bottom position.
    while True:
        elapsed_time = time.time() - start_time
        time_left_noon = raise_top_time - elapsed_time
        time_left_2 = drop_time - elapsed_time
        time_left_3 = restart_time - elapsed_time

        time_left_noon = round(time_left_noon, 2)
        time_left_2 = round(time_left_2, 2)
        time_left_3 = round(time_left_3, 2)

        print(elapsed_time)
        if elapsed_time >= raise_halfway_time and not raised_to_middle:  # Raise ball to halfway
            forward_to_middle()
            raised_to_middle = True

        elif elapsed_time  < raise_top_time and raised_to_middle:
            display_text(f"Waiting for noon. Time left: {time_left_noon}")

        elif elapsed_time  >= raise_top_time and not raised_to_top:
            forward_to_top()
            raised_to_top = True

        elif elapsed_time < drop_time and raised_to_top:
            display_text(f"Top. Time left: {time_left_2}")



        elif elapsed_time >= drop_time and not dropped:
            backwards()
            dropped = True

        elif elapsed_time < restart_time and dropped:
            display_text("Bottom")

        elif elapsed_time >= restart_time and not restarted:   # Restart the sequence
            start_time = time.time()
            raised_to_middle = False
            raised_to_top = False
            dropped = False
            restarted = True


def destroy():
    pwm.stop()

if __name__ == '__main__':
    setup()
    try:
        sequence()
    except KeyboardInterrupt:
        destroy()
        GPIO.cleanup()
    pygame.quit()  # Clean up pygame resources.
