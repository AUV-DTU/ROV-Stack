import socket
import pygame
import time

# ---------------- Configuration ----------------
RADXA_IPv4 = "192.168.1.69"
PORT = 5005
NEUTRAL_DATA = "1500/1500/1500/1500/1500/1500/1500/1500/0/0"

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
    left_y = -joystick.get_axis(1)   # surge (forward/back)
    left_x = joystick.get_axis(0)    # yaw
    right_x = joystick.get_axis(2)   # sway
    right_y = -joystick.get_axis(3)  # heave

    # Triggers
    rt = (joystick.get_axis(5) + 1) / 2
    lt = (joystick.get_axis(4) + 1) / 2

    # Deadzone
    if abs(left_y) < DEADZONE: left_y = 0
    if abs(left_x) < DEADZONE: left_x = 0
    if abs(right_x) < DEADZONE: right_x = 0
    if abs(right_y) < DEADZONE: right_y = 0

    # Combine heave
    heave = right_y + (rt - lt)

    # Base PWM
    base = 1500
    scale = 300

    # -------- THRUSTER MIXING --------
    # Horizontal (FL, FR, BL, BR)
    FL = base + scale*(left_y + left_x)
    FR = base + scale*(left_y - left_x)
    BL = base + scale*(left_y + left_x)
    BR = base + scale*(left_y - left_x)

    # Vertical (heave)
    H1 = base + scale*heave
    H2 = base + scale*heave
    H3 = base + scale*heave
    H4 = base + scale*heave

    # Sway
    SW1 = base + scale*(right_x)
    SW2 = base - scale*(right_x)

    # Clamp
    def clamp(v): return int(max(1100, min(1900, v)))

    FL, FR, BL, BR = map(clamp, [FL, FR, BL, BR])
    H1, H2, H3, H4 = map(clamp, [H1, H2, H3, H4])
    SW1, SW2 = map(clamp, [SW1, SW2])

    # -------- SERVO --------
    servo = 0
    if joystick.get_button(3):  # Y button
        servo = 180

    # -------- LIGHT --------
    light = 1 if joystick.get_button(0) else 0  # A button

    # -------- FINAL FORMAT --------
    return (
        f"{H1}/{H2}/{FL}/{FR}/"
        f"{H3}/{H4}/{SW1}/{SW2}/"
        f"{servo}/{light}"
    )

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