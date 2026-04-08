import socket
import pygame
import time

# ---------------- Configuration ----------------
RADXA_IPv4 = "192.168.1.69"
PORT = 5005
NEUTRAL_DATA = "1500/1500/1500/1500/1500/1500/0"

# ---------------- Setup UDP ----------------
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.01)

# ---------------- Setup Controller ----------------
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller detected!")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print("Controller connected:", joystick.get_name())

# Deadzone to avoid drift
DEADZONE = 0.2

def get_thruster_data():
    pygame.event.pump()

    # Axes
    left_y = -joystick.get_axis(1)  # Forward/back
    left_x = joystick.get_axis(0)   # Left/right

    # Apply deadzone
    if abs(left_y) < DEADZONE:
        left_y = 0
    if abs(left_x) < DEADZONE:
        left_x = 0

    # Mapping logic
    if left_y > 0.5:
        return "1500/1500/1500/1500/1580/1580/0"  # Forward (W)
    elif left_y < -0.5:
        return "1600/1500/1500/1500/1420/1420/0"  # Backward (S)
    elif left_x < -0.5:
        return "1650/1650/1650/1650/1500/1500/0"  # Left (Q)
    elif left_x > 0.5:
        return "1350/1350/1350/1350/1500/1500/0"  # Right (E)
    else:
        return NEUTRAL_DATA

print("Xbox controller mode started. Ctrl+C to stop.")

try:
    while True:
        thruster_data = get_thruster_data()

        sock.sendto(thruster_data.encode(), (RADXA_IPv4, PORT))

        print("Sending:", thruster_data)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    sock.close()
    pygame.quit()