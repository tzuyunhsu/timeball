import datetime
import os
import socket
import sys
import time

import netifaces
import pygame
import RPi.GPIO as GPIO
from pygame.locals import *


def draw_time_page():
    update_background()
    draw_button("admin")
    update_time()


def draw_admin_login_page():
    screen.fill((94, 156, 166))
    draw_button("home")
    draw_login()


def draw_admin_control_page():
    screen.fill((94, 156, 166))
    draw_button("home")
    draw_control()


def update_background():
    global current_img_index, start
    current = time.time() - start
    if current > 6:
        # update the background with the next image file
        start = time.time()
        current = 0
        current_img_index = (current_img_index-1) % len(background_files)
    # Clear the screen & load image
    screen.fill((255, 255, 255))
    background = pygame.image.load(
        os.path.join(background_folder, background_files[current_img_index])).convert()
    background = pygame.transform.scale(background, (320, 240))
    screen.blit(background, (0, 0))


def draw_button(button_text):
    global font
    # Drawing the Button
    button_width, button_height = 80, 40
    button_color = (255, 255, 255)
    button_position = (220, 190)
    button_rect = pygame.Rect(button_position, (button_width, button_height))
    pygame.draw.rect(screen, button_color, button_rect)

    # Writing the Button Text
    text_surf = font.render(button_text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)


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

    # Draw the date, time, and time left to noon
    date_text = font.render(date_string, True, (0, 0, 0))
    screen.blit(date_text, (10, 10))
    time_text = font.render(time_string, True, (0, 0, 0))
    screen.blit(time_text, (10, 40))
    noon_text = font.render(time_left, True, (0, 0, 0))
    screen.blit(noon_text, (10, 70))

    # Update the screen
    pygame.display.flip()


def draw_login():
    global pwd_input
    text_str = "Enter Password:"
    text = font.render(text_str, True, (0, 0, 0))
    screen.blit(text, (80, 80))
    pwd_text = font.render(pwd_input, True, (0, 0, 0))
    pwd_rect = pwd_text.get_rect(center=(160, 120))
    screen.blit(pwd_text, pwd_rect)
    pygame.display.flip()


def draw_control():
    line1 = "Admin Control Page!"
    line1_text = font.render(line1, True, (0, 0, 0))
    screen.blit(line1_text, (10, 10))
    line2 = "- Press button #1 to move up"
    line2_text = font.render(line2, True, (0, 0, 0))
    screen.blit(line2_text, (10, 40))
    line3 = "- Press button #2 to move down"
    line3_text = font.render(line3, True, (0, 0, 0))
    screen.blit(line3_text, (10, 70))
    line4 = "- Press button #3 to stop"
    line4_text = font.render(line4, True, (0, 0, 0))
    screen.blit(line4_text, (10, 100))
    line4 = "- Press button #4 to shutdown"
    line4_text = font.render(line4, True, (0, 0, 0))
    screen.blit(line4_text, (10, 130))


def get_ip():
    global ip_address, ip_displayed
    ip_address = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
    ip_displayed = True
    ip_text = font.render(ip_address, True, (0, 0, 0))
    screen.blit(ip_text, (10, 100))
    pygame.display.flip()


def handle_event(event):
    global current_page, pwd_input
    # Handling Page Navigation and Button Clicks
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if current_page == HOME_PAGE:
            if pos[0] > 220 and pos[1] > 190:
                current_page = ADMIN_LOGIN_PAGE
        elif current_page == ADMIN_LOGIN_PAGE:
            if pos[0] > 220 and pos[1] > 190:
                current_page = HOME_PAGE
                pwd_input = ""
        elif current_page == ADMIN_CONTROL_PAGE:
            if pos[0] > 220 and pos[1] > 190:
                current_page = HOME_PAGE
        
def check_pwd():
    # Verifies if the user input is the correct password
    global current_page, pwd_input
    print(pwd_input)
    if len(pwd_input) == 4:
        if pwd_input == password:
            print("password correct!")
            current_page = ADMIN_CONTROL_PAGE
        else:
            print("Password incorrect!")
        pwd_input = ""

def gpio17_callback(channel):
    global current_page, pwd_input
    if current_page == ADMIN_CONTROL_PAGE:
        print("Moving Up!")
    elif current_page == ADMIN_LOGIN_PAGE:
        pwd_input += "1"
        check_pwd()


def gpio22_callback(channel):
    global current_page, pwd_input
    if current_page == ADMIN_CONTROL_PAGE:
        print("Moving Down!")
    elif current_page == ADMIN_LOGIN_PAGE:
        pwd_input += "2"
        check_pwd()


def gpio23_callback(channel):
    global current_page, pwd_input
    if current_page == ADMIN_CONTROL_PAGE:
        print("Stop!")
    elif current_page == ADMIN_LOGIN_PAGE:
        pwd_input += "3"
        check_pwd()


def gpio27_callback(channel):
    global running
    running = False


os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv("SDL_MOUSEDRV", "TSLIB")
os.putenv("SDL_MOUSEDEV", "/dev/input/touchscreen")
pygame.init()

# Create the screen
screen = pygame.display.set_mode((320, 240))
pygame.display.set_caption("Current Date and Time")

# Create the font
font = pygame.font.Font(None, 30)

# Access Images
background_folder = "background_img" #need to update pwd from home
background_files = [f for f in os.listdir(background_folder)]
current_img_index = 0
current_background = os.path.join(
    background_folder, background_files[current_img_index])
start = time.time()

# Pages
HOME_PAGE = 0
ADMIN_LOGIN_PAGE = 1
ADMIN_CONTROL_PAGE = 2

# Password Settings
password = "3221"
pwd_input = ""

# Configuring the button
GPIO.setmode(GPIO.BCM)
buttons = [17, 22, 23, 27]
for b in buttons:
    GPIO.setup(b, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(
    17, GPIO.FALLING, callback=gpio17_callback, bouncetime=300)
GPIO.add_event_detect(
    22, GPIO.FALLING, callback=gpio22_callback, bouncetime=300)
GPIO.add_event_detect(
    23, GPIO.FALLING, callback=gpio23_callback, bouncetime=300)
GPIO.add_event_detect(
    27, GPIO.FALLING, callback=gpio27_callback, bouncetime=300)

# Main loop
running = True
current_page = HOME_PAGE

while running:
    if current_page == HOME_PAGE:
        screen.fill((255, 255, 255))
        draw_time_page()
        pygame.time.wait(1000)
    elif current_page == ADMIN_LOGIN_PAGE:
        screen.fill((255, 255, 255))
        draw_admin_login_page()
    elif current_page == ADMIN_CONTROL_PAGE:
        screen.fill((255, 255, 255))
        draw_admin_control_page()

    for event in pygame.event.get():
        handle_event(event)

    pygame.display.update()

pygame.quit()
sys.exit()
