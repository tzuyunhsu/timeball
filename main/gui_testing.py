import pygame
import datetime
import socket
import RPi.GPIO as GPIO
import netifaces
import os, sys

def update_time():
    # Get the current date and time
    now = datetime.datetime.now()
    date_string = now.strftime("%B %d, %Y")
    time_string = now.strftime("%I:%M:%S %p")

    # Calculate the time left to noon
    noon = datetime.time(12, 0, 0)
    if now.time() < noon:
        diff = datetime.datetime.combine(now, noon) - now
        hours, remainder = divmod(diff.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_left = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    else:
        time_left = "Noon has passed"

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
os.putenv('SDL_FBDEV', '/dev/fb1')
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
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    update_time()
    pygame.time.wait(1000)
    pygame.display.update()

pygame.quit()
sys.exit()
