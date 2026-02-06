# os = Raspberry Pi
import lgpio
import threading
import time

# GPIO Pin Definitions
PWM_PIN = 18 # PWM pin for motor speed control
TRIG_PIN = 23 # Ultrasonic sensor TRIG pin
ECHO_PIN = 24 # Ultrasonic sensor ECHO pin
HALL_SENSOR_PINS = [5,6,13] # Hall sensor GPIO pins

# Variables
current_speed = 0 # Current motor speed
running = True # Main program control
obstacle_detected = False # Flag to indicate obstacle detection

# Open GPIO chip
chip = lgpio.gpiochip_open(0)

# Setup GPIO
lgpio.gpio_claim_output(chip, TRIG_PIN)
lgpio.gpio_claim_input(chip, ECHO_PIN)
lgpio.gpio_claim_output(chip, PWM_PIN)
for pin in HALL_SENSOR_PINS:
    lgpio.gpio_claim_input(chip, pin)

# Start PWM with 0% duty cycle and 6kHz frequency
lgpio.tx_pwm(chip, PWM_PIN, 6000, 0)

# Lock for thread safety
sensor_lock = threading.Lock()

def set_motor_speed(speed):
    """
    set motor speed.
    :param speed: Motor speed(0 to 100).
    """
    global current_speed
    if 0 <= speed <= 100:
        current_speed = speed
        lgpio.tx_pwm(chip, PWM_PIN, 6000, speed)
        print(f"Motor speed set to {speed}%")
    else:
        print("Invaild speed! Enter a value between 0 and 100.")

def get_distance():
    """
    Measure the distance using the Ultrasonic sensor.
    :return: Distance in centimeters.
    """
    with sensor_lock: # Ensure thread safety
        lgpio.gpio_write(chip, TRIG_PIN, 0)
        time.sleep(0.000002) # 2us delay
        lgpio.gpio_write(chip, TRIG_PIN, 1)
        time.sleep(0.00001) # 10us delay
        lgpio.gpio_write(chip, TRIG_PIN, 0)

        start_time = time.time()
        while lgpio.gpio_read(chip, ECHO_PIN) == 0:
            start_time = time.time()

        while lgpio.gpio_read(chip, ECHO_PIN) == 1:
            end_time = time.time()

        pulse_duration = end_time - start_time
        distance = (pulse_duration * 34300) / 2 # Convert to centimeters
        return distance
def input_thread():
    """
    Thread for handling user input to control motor speed.
    """
    global running, current_speed, obstacle_detected
    try:
        while running:
            speed = input("Enter motor speed (0 to 100) or 'q' to quit: ")
            if speed.lower() == 'q':
                running = False
            else:
                try:
                    speed_value = int(speed)
                    if obstacle_detected:
                        print("Obstacle detected! Cannot set speed. Wait until the obstacle is cleared.")
                    else:
                        set_motor_speed(speed_value)
                except ValueError:
                    print("Invaild input! Please enter a number. ")
    except KeyboardInterrupt:
        running = False
def distance_monitor():
    """
    Thread to monitor the distance and stop the motor if an obstacle is detected.
    """
    global running, obstacle_detected
    try:
        while running:
            distance = get_distance()
            if distance <= 100:
                if not obstacle_detected:
                    print(f"Distance: {distance:.2f}cm")
                    print("Obstacle detected! Stopping the motor.")
                    obstacle_detected = True
                    set_motor_speed(0)
            else:
                if obstacle_detected:
                    print("Obstacle cleared. You can set the speed again.")
                obstacle_detected = False
            time.sleep(0.1)
    except KeyboardInterrupt:
        running = False
try:
    # Start threads for input and distance monitoring
    input_thread_instance = threading.Thread(target=input_thread, daemon=True)
    distance_monitor_instance = threading.Thread(target=distance_monitor, daemon=True)

    input_thread_instance.start()
    distance_monitor_instance.start()

    #Main loop to keep program running
    while running:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program...")

finally:
    running = False
    # Stop PWM and release resources
    lgpio.tx_pwm(chip, PWM_PIN, 6000, 0) # Stop PWM
    lgpio.gpiochip_close(chip)
    print("Program finished.")