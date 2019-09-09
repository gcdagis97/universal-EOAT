import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Motor 1 is topmost on breadboard (screws on bottom)
Motor1StepPin = 27
Motor1DirPin = 22
Motor2StepPin = 17
Motor2DirPin = 4
Motor3StepPin = 5
Motor3DirPin = 19
Motor4StepPin = 26
Motor4DirPin = 13

# Set up encoder channels
Encoder1ChA = 23
Encoder1ChB = 24
#Encoder2ChA = 
#Encoder2ChB = 
#Encoder3ChA = 
#Encoder3ChB = 
#Encoder4ChA = 
#Encoder4ChB = 

GPIO.setwarnings(False)

# Motor GPIO
GPIO.setup(Motor1DirPin, GPIO.OUT)
GPIO.setup(Motor1StepPin, GPIO.OUT)
GPIO.setup(Motor2StepPin, GPIO.OUT)
GPIO.setup(Motor2DirPin, GPIO.OUT)
GPIO.setup(Motor3StepPin, GPIO.OUT)
GPIO.setup(Motor3DirPin, GPIO.OUT)
GPIO.setup(Motor4StepPin, GPIO.OUT)
GPIO.setup(Motor4DirPin, GPIO.OUT)

# Encoder GPIO
GPIO.setup(Encoder1ChA, GPIO.IN)
GPIO.setup(Encoder1ChB, GPIO.IN)
#GPIO.setup(Encoder2ChA, GPIO.IN)
#GPIO.setup(Encoder2ChB, GPIO.IN)
#GPIO.setup(Encoder3ChA, GPIO.IN)
#GPIO.setup(Encoder3ChB, GPIO.IN)
#GPIO.setup(Encoder4ChA, GPIO.IN)
#GPIO.setup(Encoder5ChB, GPIO.IN)

# Establish a running frequency and an optimal frequency
runningfreq = 5000
optimalfreq = 9000

# Set the step pins and starting frequencies for motors
stepper1 = GPIO.PWM(27, runningfreq)
stepper2 = GPIO.PWM(17, runningfreq)
stepper3 = GPIO.PWM(5, runningfreq)
stepper4 = GPIO.PWM(26, runningfreq)

# Duty cycle is 50%
stepper1.start(50)
stepper2.start(50)
stepper3.start(50)
stepper4.start(50)

# Clockwise = 1 (brackets towards the motors)
GPIO.output(Motor1DirPin, 0)
GPIO.output(Motor2DirPin, 0)
GPIO.output(Motor3DirPin, 0)
GPIO.output(Motor4DirPin, 0)

# Distance for bracket to move (inches)
distance = .05

# Step motor based on pitch & steps/rev
steps1 = distance*4000# Delay for .05 seconds
delay = .05

# Function to step specific motor
def stepmotor(stepsm, motornum, chA, chB):
    
    # Define initial values
    currentA = currentB = currentX = lastA = lastB = lastX = count = 0
    EncoderChA = chA
    EncoderChB = chB
    stepper = motornum
    
    # Account for encoder (300 cycles/rotation rather than 200)
    # Start motor
    steps = stepsm*1.5
    stepper.start(50)
    
    # Encoder steps
    while count < steps:
    
        # Get current pin values
        currentA = GPIO.input(EncoderChA)
        currentB = GPIO.input(EncoderChB)
        
        # A XOR B
        currentX = bool(currentA) ^ bool(currentB)

        # Rise edge B + falling edge X = add
        if (currentB*1 > lastB*1) and (currentX*1 < lastX*1):
            count += 1

        # Reset X
        lastX = currentX

    stepper.stop()

# Step motors
stepmotor(steps1, stepper1, Encoder1ChA, Encoder1ChB)
stepmotor(steps2, stepper2, Encoder2ChA, Encoder2ChB)
stepmotor(steps3, stepper3, Encoder3ChA, Encoder3ChB)
stepmotor(steps4, stepper4, Encoder4ChA, Encoder4ChB)