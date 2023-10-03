import time
import smtplib

def send_alert(message):
    # Set up the SMTP server
    server = smtplib.SMTP('smtp.example.com')

    # Send the email
    server.sendmail(
        "time-ball@example.com",  # From address
        "admin@example.com",      # To address
        message                    # Message
    )

    # Disconnect from the server
    server.quit()


# Set up the log file
log_file = open("time_ball_log.txt", "r")

# Read the log file line by line
for line in log_file:
    # Split the line into action and time
    action, timestamp = line.strip().split(',')

    # Convert the timestamp to a time object
    log_time = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    # Get the current time
    current_time = time.localtime()

    # Check the action and time
    if action == "Started moving to middle" and not (current_time.tm_hour == log_time.tm_hour - 1 and current_time.tm_min >= 50):
        send_alert("Action 'Started moving to middle' did not occur at the expected time.")
    elif action == "Started moving to top" and not (current_time.tm_hour == log_time.tm_hour - 1 and current_time.tm_min >= 55):
        send_alert("Action 'Started moving to top' did not occur at the expected time.")
    elif action == "Dropped" and not (current_time.tm_hour == log_time.tm_hour and current_time.tm_min == 0):
        send_alert("Action 'Dropped' did not occur at the expected time.")

# Close the log file
log_file.close()

