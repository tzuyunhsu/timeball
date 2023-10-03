import pygame
import datetime
import socket
import RPi.GPIO as GPIO
import netifaces
import os, sys
from countdown_gui import *

raised_to_middle = False
raised_to_top = False
dropped = False

def update_time():
    # Get the current date and time
    now = datetime.datetime.now()
    date_string = now.strftime("%B %d, %Y")
    time_string = now.strftime("%I:%M:%S %p")
    
    global system_start_time
    global raised_to_middle
    global raised_to_top
    global dropped

    # Calculate the time left to the next motion
    diff = (now - system_start_time).total_seconds()
    # Waiting to move to the middle (1 minute)
    if diff < 60:
        #diff = datetime.datetime.combine(now, system_start_time) - now
        #hours, remainder = divmod(diff.total_seconds(), 3600)
        minutes, seconds = divmod((60 - diff), 60)
        time_left = f"{int(minutes):02d}:{int(seconds):02d} to move to the middle!"

    # Forward to the middle
    if diff >= 60 and not raised_to_middle:
        #time_left = "Moving to the middle!"
        now = forward_to_middle(now, screen ,font)
        time_string = now.strftime("%I:%M:%S %p")
        raised_to_middle = True

    # Waiting to move to the top (2 minutes)
    if raised_to_middle and diff < 120 :
        #diff = datetime.datetime.combine(now, system_start_time) - now
        #hours, remainder = divmod(diff.total_seconds(), 3600)
        minutes, seconds = divmod((120 - diff), 60)
        time_left = f"{int(minutes):02d}:{int(seconds):02d} to move to the top!"
    
    # Forward to the top
    if diff >= 120 and not raised_to_top:
        time_left = "Moving to the top!"
        now = forward_to_top(now, screen, font)
        time_string = now.strftime("%I:%M:%S %p")
        raised_to_top = True
    
    # Waiting to drop the ball to the bottom (3 minutes)
    if raised_to_middle and raised_to_top and diff < 180:
        #diff = datetime.datetime.combine(now, system_start_time) - now
        #hours, remainder = divmod(diff.total_seconds(), 3600)
        minutes, seconds = divmod((180 - diff), 60)
        time_left = f"{int(minutes):02d}:{int(seconds):02d} to drop to the bottom!"

    # Drop to the bottom
    if diff >= 180 and not dropped:
        time_left = "Dropping to the bottom!"
        now = backwards(now, screen, font)
        time_string = now.strftime("%I:%M:%S %p")
        dropped = True

    # Check if all actions completed
    if raised_to_middle and raised_to_top and dropped:
        time_left = "The cycle is complete!"

        # Enable multiple cycles (Up to 15 min)
        if (now - time_limit_start).total_seconds() < 900:
            system_start_time = now
            raised_to_middle = False
            raised_to_top = False
            dropped = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the date, time, and time left to noon
    date_text = font.render(date_string, True, (0, 0, 0))
    screen.blit(date_text, (10, 10))
    time_text = font.render(time_string, True, (0, 0, 0))
    screen.blit(time_text, (10, 40))
    noon_text = font.render(time_left, True, (0, 0, 0))
    screen.blit(noon_text, (10, 70))

    # Update the screen
    pygame.display.flip()


def get_ip():
    global ip_address,ip_displayed
    ip_address = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
    ip_displayed = True
    ip_text = font.render(ip_address, True, (0, 0, 0))
    screen.blit(ip_text, (10, 100))
    pygame.display.flip()

def button_callback(channel):
    get_ip()

def quit_callback(channel):
    global running
    running = False

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0') #/fb1 if connected with monitor and piTFT; /fb0 if only piTFT
pygame.init()

# Create the screen
screen = pygame.display.set_mode((320, 240))
pygame.display.set_caption("Current Date and Time")

# Create the font
font = pygame.font.Font(None, 30)

# Configuring the button
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(17, GPIO.FALLING, callback=button_callback, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=quit_callback, bouncetime=300)

# Main loop
running = True
system_start_time = datetime.datetime.now()
time_limit_start = system_start_time
setup()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    update_time()
    pygame.time.wait(1000)
    pygame.display.update()

pygame.quit()
sys.exit()
