import RPi.GPIO as GPIO
import time
import datetime
import os, sys
import pygame
import socket
import netifaces

# Pin definitions.
#pwmPIN = 26 # hasn't assigned yet
AIN1Pin = 5
AIN2Pin = 6

Topsensor_pin = 16
Midsensor_pin = 20
Bottomsensor_pin = 21

#duty = 50
#frequency = 50

#timeouts
raise_halfway_timeout = 17
raise_top_timeout = 17
drop_timeout = 32

def setup():
    GPIO.setup(AIN1Pin, GPIO.OUT)
    GPIO.setup(AIN2Pin, GPIO.OUT)
    GPIO.setup(Topsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Midsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Bottomsensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    

# define a function to exit the program
def exit_program():
    GPIO.output(AIN1Pin, GPIO.LOW)
    GPIO.output(AIN2Pin, GPIO.LOW)
    sys.exit()

def forward_to_middle(now, screen, font):
    start_time_1 = time.time()
    #log_entry("Started moving to middle: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    Midsensor_status = GPIO.input(Midsensor_pin)
    while Midsensor_status == 1:
        # Update time
        date_string = now.strftime("%B %d, %Y")
        time_string = now.strftime("%I:%M:%S %p")
        time_left = "Moving to the middle!"

        # Going forwards (going up) to the middle.
        GPIO.output(AIN1Pin, GPIO.HIGH)
        GPIO.output(AIN2Pin, GPIO.LOW)

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw the date, time , and time left to noon
        date_text = font.render(date_string, True, (0, 0, 0))
        screen.blit(date_text, (10, 10))
        time_text = font.render(time_string, True, (0, 0, 0))
        screen.blit(time_text, (10, 40))
        noon_text = font.render(time_left, True, (0, 0, 0))
        screen.blit(noon_text, (10, 70))

        # Update the screen
        pygame.display.flip()
       
        # Update current time
        now = datetime.datetime.now()

        Midsensor_status = GPIO.input(Midsensor_pin)

       # Check if the elapsed time has surpassed the timeout.
       # Remove timeout to test functionality first
       # elapsed_time = time.time() - start_time_1
       # if elapsed_time > raise_halfway_timeout:
       #     print("Timeout reached. Shutting down.")
       #     # Call a function to shutdown the system.
       #     exit_program()


    print("Middle sensor reached!")
    #stop
    GPIO.output(AIN1Pin, GPIO.LOW)

    return now

def forward_to_top(now, screen, font):
    start_time_2 = time.time()
    #log_entry("Started moving to top: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    Topsensor_status = GPIO.input(Topsensor_pin)
    while Topsensor_status == 1:
        # Update time
        date_string = now.strftime("%B %d, %Y")
        time_string = now.strftime("%I:%M:%S %p")
        time_left = "Moving to the top!"        

        # Going forwards (going up) to the top.
        GPIO.output(AIN1Pin, GPIO.HIGH)
        GPIO.output(AIN2Pin, GPIO.LOW)

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw the date, time , and time left to noon
        date_text = font.render(date_string, True, (0, 0, 0))
        screen.blit(date_text, (10, 10))
        time_text = font.render(time_string, True, (0, 0, 0))
        screen.blit(time_text, (10, 40))
        noon_text = font.render(time_left, True, (0, 0, 0))
        screen.blit(noon_text, (10, 70))

        # Update the screen
        pygame.display.flip()
       
        # Update current time
        now = datetime.datetime.now()


        Topsensor_status = GPIO.input(Topsensor_pin)

        # Check if the elapsed time has surpassed the timeout.
        # Remove timeout to test functionality first
        #elapsed_time = time.time() - start_time_2
        #if elapsed_time > raise_top_timeout:
        #    print("Timeout reached. Shutting down.")
        #    # Call a function to shutdown the system.
        #    exit_program()

    print("Top sensor reached!")
    #stop
    GPIO.output(AIN1Pin, GPIO.LOW)

    return now

def backwards(now, screen, font):
    start_time_3 = time.time()
    #log_entry("Dropped: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    Bottomsensor_status = GPIO.input(Bottomsensor_pin)
    while Bottomsensor_status == 1:
        # Update time
        date_string = now.strftime("%B %d, %Y")
        time_string = now.strftime("%I:%M:%S %p")
        time_left = "Dropping back to the bottom!"        

        # Going backwards (going down).
        GPIO.output(AIN1Pin, GPIO.LOW)
        GPIO.output(AIN2Pin, GPIO.HIGH)

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw the date, time , and time left to noon
        date_text = font.render(date_string, True, (0, 0, 0))
        screen.blit(date_text, (10, 10))
        time_text = font.render(time_string, True, (0, 0, 0))
        screen.blit(time_text, (10, 40))
        noon_text = font.render(time_left, True, (0, 0, 0))
        screen.blit(noon_text, (10, 70))

        # Update the screen
        pygame.display.flip()
       
        # Update current time
        now = datetime.datetime.now()


        Bottomsensor_status = GPIO.input(Bottomsensor_pin)

        # Check if the elapsed time has surpassed the timeout.
        # Remove timeout to test functionality first
        #elapsed_time = time.time() - start_time_3
        #if elapsed_time > drop_timeout:
        #    print("Timeout reached. Shutting down.")
        #    # Call a function to shutdown the system.
        #    exit_program()

    print("Bottom sensor reached!")
    # stop
    GPIO.output(AIN2Pin, GPIO.LOW)

    return now

#def sequence(running):
#    GPIO.output(AIN1Pin, GPIO.LOW)
#    GPIO.output(AIN2Pin, GPIO.LOW)
#    # Flags
#    raised_to_middle = False
#    raised_to_top = False
#    dropped = False
#
#    # Set up the log file.
#    #try:
#    #    log_file = open("time_ball_log.txt", "a")
#    #except:
#    #    print("Unable to open log file")
#    #    return
#
#
#    while running:
#        current_time = datetime.datetime.now().time()
#
#        # 1 minutes in each cycle, raise the ball to the middle of the post.
#        if current_time.minute - system_start_time.minute == 1 and current_time.second == system_start_time.second and not raised_to_middle:
#            print("Triggering forward_to_middle()")
#            forward_to_middle()
#            raised_to_middle = True
#
#        # 2 minutes in each cycle, raise the ball to the top of the post.
#        if current_time.minute - system_start_time.minute == 2 and current_time.second == system_start_time.second and not raised_to_top:
#            print("Triggering forward_to_top()")
#            forward_to_top()
#            raised_to_top = True
#
#        # 3 minutes in each cycle, drop the ball from the top to the bottom.
#        if current_time.minute - system_start_time.minute == 3 and current_time.second == system_start_time.second and not dropped:
#            print("Triggering backwards()")
#            backwards()
#            dropped = True
#
#        # Check if all the actions have been completed
#        if raised_to_middle and raised_to_top and dropped:            
#            break
#
#        time.sleep(1)  # Wait for 1


#if __name__ == '__main__':
#    setup()
#    running = True
#    #system_start_time = datetime.datetime.now()
#
#    while running:
#        try:
#            sequence(running)
#        except KeyboardInterrupt:
#            GPIO.cleanup()

#pygame.quit()
#sys.exit()
