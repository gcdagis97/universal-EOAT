# PWM on Raspberry Pi
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/

# Working with A4988 Motor Driver
# https://howtomechatronics.com/tutorials/arduino/how-to-control-stepper-motor-with-a4988-driver-and-arduino/

# Project Utilizes Four NEMA 14 Bipolar Stepper Motors
# https://www.omc-stepperonline.com/download/14HS20-1504D-E22-300.pdf

# Motors are Driven Using A4988 Motor Drivers
# https://www.pololu.com/file/0J450/A4988.pdf

# Program is built to control the Multi-purpose Gripper End of Arm Tooling (EOAT) project for SUNY New Paltz Senior Design II

"""main.py :Main controller for EOAT """

# system exits
import sys
import os

# re.findall for file handling & line deletion
import re
import RPi.GPIO as GPIO
import time

# run parallel processes
import multiprocessing

__author__ = "George Dagis", "NAME OMITTED"
__copyright__ = "Copyright 2019, Sr. Design II EOAT"
__version__ = "1.0"
__email__ = "dagisg1@hawkmail.newpaltz.edu"
__status__ = "Prototype"

# Establish a running frequency and an optimal frequency
runningfreq = 5000

# NEMA 14 motor runs best at 9kHz but this is adjustable
# optimalfreq = 9000

# Refer to GPIO by GPIO#
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
Encoder2ChA = 18
Encoder2ChB = 25
Encoder3ChA = 12
Encoder3ChB = 20
Encoder4ChA = 16
Encoder4ChB = 21

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
GPIO.setup(Encoder2ChA, GPIO.IN)
GPIO.setup(Encoder2ChB, GPIO.IN)
GPIO.setup(Encoder3ChA, GPIO.IN)
GPIO.setup(Encoder3ChB, GPIO.IN)
GPIO.setup(Encoder4ChA, GPIO.IN)
GPIO.setup(Encoder4ChB, GPIO.IN)

# Set the step pins and starting frequencies for motors
stepper1 = GPIO.PWM(27, runningfreq)
stepper2 = GPIO.PWM(17, runningfreq)
stepper3 = GPIO.PWM(5, runningfreq)
stepper4 = GPIO.PWM(26, runningfreq)

# Main method
def main():

   # Main prompt for user
   print()
   print("SELECT A DESIRED FUNCTION: ")
   print("1. START AUTOMATION WITH AN EXISTING PART.")
   print("2. VIEW / EDIT PARTS LIST.")
   print("3. EXIT PROGRAM.\n")

   # Register input
   menuSel= int(input("SELECTION: "))

   # Start automation
   if menuSel == 1:
       startautomation()

   # View / edit parts list
   elif menuSel == 2:
       vieweditpartslist()
      
   # Exit Program
   elif menuSel == 3:
       print("PROGRAM EXITING\n")
       sys.exit()

   else:
       print("UNACCEPTABLE INPUT. PLEASE TRY AGAIN")
       main()

# Starts automation on tool
def startautomation():
   print("SELECT PATTERN TO WORK ON: ")
   printpartslistwithnumbers()
   print()

   # Get the desired part and convert input from str to type 'int' (will be compared later)
   print("INPUT THE CORRESPONDING LINE NUMBER (Ex '3')")
   print("YOU MAY ALSO QUIT WITH '0'")
   parttoworkon = int(input("SELECTION: "))
   print()

   # Returns number of parts in PartsList.txt (make sure declaration is valid)
   num_lines = sum(1 for line in open('PartsList.txt'))

   # Quit
   if parttoworkon == 0:
       print("QUITTING PROCESS. RETURNING TO MAIN MENU")
       main()

   # Ensure a part on that line in the file exists
   # Automation continue
   elif parttoworkon > 0 and parttoworkon <= num_lines:

       # Decrement one, otherwise while loop will get the part after the desired line
       parttoworkon = parttoworkon - 1

       # Prints all integers on separate lines
       with open('PartsList.txt') as f:

           # keep track of lines skipped
           linecounter = 0

           # skip lines until desired line is the current line
           while linecounter != parttoworkon:

               # read (skip) line
               f.readline()

               # increment counter
               linecounter = linecounter+1

           # first line is now a str
           s = f.readline()
           print("ARE YOU SURE YOU'D LIKE TO START AUTOMATION ON THE FOLLOWING PART? (Y/N)",s)
           confirmautomation = input("SELECTION: ")

           if confirmautomation == 'Y' or confirmautomation == 'y':

               # extract all integers from string and put into a list
               coordinates = (re.findall(r'\d+', s))
               f.close

               # Assign values to cup position variable
               # Cast to int for comparison
               # x, y2
               Cup_A_X = int(coordinates[0])
               Cup_A_Y = int(coordinates[1])

               # 0, y1
               Cup_B_X = int(coordinates[2])
               Cup_B_Y = int(coordinates[3])

               # x, 0
               Cup_C_X = int(coordinates[4])
               Cup_C_Y = int(coordinates[5])

               # Always 0,0
               Cup_D_X = int(coordinates[6])
               Cup_D_Y = int(coordinates[7])

               # A: x, y1
               # B: 0, y2
               # C: x, 0
               # D: 0, 0

               #x = Cup_A_X
               #y1 = Cup_A_Y
               #y2 = Cup_B_Y
              
               # Step each motor based different number of steps
               # Steppers 1 and 2 always doing the same thing
               steps1 = Cup_A_X
               steps2 = Cup_C_X
               steps3 = Cup_B_Y
               steps4 = Cup_A_Y

               # Convert from inches to steps (20 threads/inch * 200 steps/rev * 1.5 encoder cycles/motor cycle
               steps1 = steps1*6000
               steps2 = steps2*6000
               steps3 = steps3*6000
               steps4 = steps4*6000

               # Ensure that x/y1/y2 are within bounds

               if (Cup_A_X == Cup_C_X) and (Cup_A_X >= 0) and (Cup_A_X <= 14000) and (
                       Cup_A_Y >= 0 and Cup_A_Y <= 20000) and (Cup_B_Y >= 0 and Cup_B_Y <= 20000):
                  
                   print("AUTOMATION WILL NOW BEGIN")
              
                   # Step motors towards part
                   GPIO.output(Motor1DirPin, 0)
                   GPIO.output(Motor2DirPin, 0)
                   GPIO.output(Motor3DirPin, 0)
                   GPIO.output(Motor4DirPin, 0)

                   # Step motors
                   proc1 = multiprocessing.Process(target=stepmotor, args=(steps1,stepper1,Encoder1ChA,Encoder1ChB))
                   proc2 = multiprocessing.Process(target=stepmotor, args=(steps2,stepper2,Encoder2ChA,Encoder2ChB))
                   proc3 = multiprocessing.Process(target=stepmotor, args=(steps3,stepper3,Encoder3ChA,Encoder3ChB))
                   proc4 = multiprocessing.Process(target=stepmotor, args=(steps4,stepper4,Encoder4ChA,Encoder4ChB))

                   proc1.start()
                   proc2.start()
                   proc3.start()
                   proc4.start()

                   proc1.join()
                   proc2.join()
                   proc3.join()
                   proc4.join()
                  
                   # Reverse direction; step motors away from part
                   GPIO.output(Motor1DirPin, 1)
                   GPIO.output(Motor2DirPin, 1)
                   GPIO.output(Motor3DirPin, 1)
                   GPIO.output(Motor4DirPin, 1)

                   # Step motors
                   procr1 = multiprocessing.Process(target=stepmotor, args=(steps1,stepper1,Encoder1ChA,Encoder1ChB))
                   procr2 = multiprocessing.Process(target=stepmotor, args=(steps2,stepper2,Encoder2ChA,Encoder2ChB))
                   procr3 = multiprocessing.Process(target=stepmotor, args=(steps3,stepper3,Encoder3ChA,Encoder3ChB))
                   procr4 = multiprocessing.Process(target=stepmotor, args=(steps4,stepper4,Encoder4ChA,Encoder4ChB))


                   procr1.start()
                   procr2.start()
                   procr3.start()
                   procr4.start()

                   procr1.join()
                   procr2.join()
                   procr3.join()
                   procr4.join()

                   # Exit program
                   os._exit(1)
                  
               # Coordinates not valid
               else:
                   print("UNACCEPTABLE PART COORDINATES. PLEASE INSPECT THE PART AND MAKE SURE THEY FOLLOW THE FOLLOWING RULES:")
                   print("CUP A X COORDINATE = CUP C X COORDINATE, >= 0 AND <= 14000")
                   print("CUP A Y COORDINATE >= 0 AND <= 20000")
                   print("CUP B Y COORDINATE >= 0 AND <= 20000")
                   print("RETURNING TO MAIN MENU")
                   main()

   # Part number out of bounds (specified a number greater than the number of parts in the file)
   elif parttoworkon < 0 or parttoworkon > num_lines:
       print("ERROR: PART NUMBER OUT OF BOUNDS. RETURNING TO MAIN MENU")
       main()

   # Unacceptable input
   else:
       print("UNACCEPTABLE INPUT. RETURNING TO MAIN MENU")
       main()

# Hub to view / edit parts list file
def vieweditpartslist():

   # Print PartsList
   printpartslist()
  
   # Print menu
   print("SELECT A DESIRED FUNCTION: ")
   print("0. GO BACK TO MAIN MENU")
   print("1. ADD NEW PART")
   print("2. REMOVE AN EXISTING PART")
   print()
  
   # Register input
   editSel = int(input("SELECTION: "))
   print()
  
   # Go back
   if editSel == 0:
       main()
  
   # Add a new part
   if editSel == 1:
       addpart()
      
   # Remove an existing part
   elif editSel == 2:
       removepart()

   # Unnacceptable input
   else:
       print("UNACCEPTABLE INPUT. GOING BACK TO MAIN MENU")
       main()

# Add a new part
def addpart():
   # Confirm with user
   print("ARE YOU SURE YOU WANT TO ADD A NEW PART? (Y/N): ")
  
   # Register input
   confirmAdd = input("SELECTION: ")
   print()
  
   # Confirmation
   if confirmAdd == 'Y' or confirmAdd == 'y':
       print("ADDING A NEW PART\n")

       f = open("PartsList.txt", "a")

       # Get name of part
       NewPartName = input("ENTER A NAME FOR THE NEW PART: ")

       # Get cup positions
       # CupA: x, y2
       NewPartCupA_X = int(input("ENTER X COORDINATE OF CUP A: "))
       NewPartCupA_Y = int(input("ENTER Y COORDINATE OF CUP A: "))

       # CupB: 0, y1
       #NewPartCupB_X = input("ENTER X COORDINATE OF CUP B: ")
       NewPartCupB_X = 0
       NewPartCupB_Y = int(input("ENTER Y COORDINATE OF CUP B: "))

       # CupC: x, 0
       NewPartCupC_X = int(input("ENTER X COORDINATE OF CUP C: "))
       NewPartCupC_Y = 0
       #NewPartCupC_Y = input("ENTER Y COORDINATE OF CUP C: ")

       # CupD: 0, 0
       #NewPartCupD_X = input("ENTER X COORDINATE OF CUP D: ")
       #NewPartCupD_Y = input("ENTER Y COORDINATE OF CUP D: ")
       NewPartCupD_X = 0
       NewPartCupD_Y = 0
       print()

       # Ensure that x/y1/y2 are within bounds
       if (NewPartCupA_X == NewPartCupC_X) and (NewPartCupA_X >= 0) and (NewPartCupA_X <= 14000) and (NewPartCupA_Y >= 0 and NewPartCupA_Y <= 20000) and (NewPartCupB_Y >= 0 and NewPartCupB_Y <= 20000):

           # Confirm with user
           print("PLEASE REVIEW THE INFORMATION BELOW:")
           print()
           print("PART NAME: '",NewPartName,"'")
           print("CUP A X COORDINATE:", NewPartCupA_X)
           print("CUP A Y COORDINATE:", NewPartCupA_Y)
           print("CUP B X COORDINATE:", NewPartCupB_X)
           print("CUP B Y COORDINATE:", NewPartCupB_Y)
           print("CUP C X COORDINATE:", NewPartCupC_X)
           print("CUP C Y COORDINATE:", NewPartCupC_Y)
           print("CUP D X COORDINATE:", NewPartCupD_X)
           print("CUP D Y COORDINATE:", NewPartCupD_Y)
           addpartconfirmation = input("ARE YOU SURE THIS INFORMATION IS CORRECT? (Y/N): ")

           # Confirmation
           if addpartconfirmation == 'Y' or addpartconfirmation == 'y':

               # Concatenation of inputs
               NewPartFinal = NewPartName + " " + str(NewPartCupA_X) + " " + str(NewPartCupA_Y) + " " + str(NewPartCupB_X) + " " \
                              + str(NewPartCupB_Y) + " " + str(NewPartCupC_X) + " " + str(NewPartCupC_Y) + " " + str(NewPartCupD_X) + " " + str(NewPartCupD_Y)

               # Make sure that it also starts a new line
               f.write("%s\n" % NewPartFinal)

               # Inform user a new part has been added
               print("'",NewPartName,"' HAS NOW BEEN ADDED TO PARTS LIST FILE")

               # Ask user if they want to add another part
               addanotherpart = input("WOULD YOU LIKE TO ADD ANOTHER PART? (Y/N): ")

               # Yes, add another part
               if addanotherpart == 'Y' or addanotherpart == 'y':
                   addpart()

               # Do not add another part
               elif addanotherpart == 'N' or addanotherpart == 'n':
                   f.close()
                   print("PROCESS CANCELLED. RETURNING TO MAIN MENU")
                   main()

               # Else, unrecognized input
               else:
                   f.close()
                   print("UNACCEPTABLE INPUT. RETURNING TO MAIN MENU")
                   main()

           # Go back to main menu
           elif addpartconfirmation == 'N' or addpartconfirmation == 'n':
               f.close()
               addpartcontinue = input("PROCESS CANCELLED. WOULD YOU LIKE TO TRY ADDING A NEW PART AGAIN? (Y/N): ")

               # Confirmation
               if addpartcontinue == 'Y' or addpartcontinue == 'y':
                   addpart()

               elif addpartcontinue == 'N' or addpartcontinue == 'n':
                   print("PROCESS CANCELLED. EXITING TO MAIN MENU")
                   main()

               # Exit
               else:
                   print("UNACCEPTABLE INPUT. GOING BACK TO MAIN MENU")
                   main()

           # Exit
           else:
               f.close()
               print("UNACCEPTABLE INPUT. RETURNING TO MAIN MENU")
               main()

       # Coordinates not valid
       else:
           print("UNACCEPTABLE INPUT. PLEASE REVIEW YOUR INPUTS AND MAKE SURE THEY FOLLOW THE FOLLOWING RULES:")
           print("CUP A X COORDINATE = CUP C X COORDINATE, >= 0 AND <= 14000")
           print("CUP A Y COORDINATE >= 0 AND <= 20000")
           print("CUP B Y COORDINATE >= 0 AND <= 20000")
           print("RETURNING TO MAIN MENU")
           main()

   # Go back to main menu
   elif confirmAdd == 'N' or confirmAdd == 'n':
       print("PROCESS CANCELLED")
       main()
      
   # Exit
   else:
       print("UNACCEPTABLE INPUT. RETURNING TO MAIN MENU")
       main()

def removepart():
   printpartslist()
   print()
   print("PLEASE SPECIFY PART TO DELETE (Ex. 'Blue Bottlecap Openers')")
   print("YOU MAY ALSO QUIT WITH 'N'")
   removeSel = input("SELECTION: ")
   print()

   if removeSel == 'N' or removeSel == 'n':
       print("QUITTING PROCESS. RETURNING TO MAIN MENU")
       main()

   else:
       fn = "PartsList.txt"
       f = open(fn)
       output = []
       for line in f:
          if not removeSel in line:
             output.append(line)
       f.close()

       f = open(fn, 'w')
       f.writelines(output)
       f.close
       print("'",removeSel,"' HAS BEEN DELETED FROM PARTS LIST (IF IT EXISTS)")

       # Ask user if they want to remove another part
       removeanotherpart = input("WOULD YOU LIKE TO REMOVE ANOTHER PART? (Y/N): ")

       # Yes, remove another part
       if removeanotherpart == 'Y' or removeanotherpart == 'y':
           removepart()

       # Do not remove another part
       elif removeanotherpart == 'N' or removeanotherpart == 'n':
           f.close()
           print("PROCESS CANCELLED. RETURNING TO MAIN MENU")
           main()

       # Else, unrecognized input
       else:
           f.close()
           print("UNACCEPTABLE INPUT. RETURNING TO MAIN MENU")
           main()

# Prints parts list file in alphabetical order
def printpartslist():
   print("CURRENTLY EXISTING PARTS: ")
   print()
   f = open("PartsList.txt", "r")
   PartsList = f.readlines()
   PartsList.sort()
   for x in PartsList:
       print(x)

# Print parts list with line numbers
def printpartslistwithnumbers():
   with open('PartsList.txt') as f:
       for i, line in enumerate(f):

           # Print part on line 1
           while line:

               # Increment to count from 1 rather than 0
               i=i+1;

               # Convert i to string for concatenation
               linenumber = str(i)

               # Concatenate
               numberedline = linenumber + ". " + line
               print(numberedline)
               break

       # No more lines in file
       else:
           print("*FINISHED READING FILE*")
           line = None

# Function to step specific motor
def stepmotor(stepsm, stepper, EncoderChA, EncoderChB):
  
   # Duty cycle is 50%
   stepper1.start(50)
  
   # Define initial values
   currentA = currentB = currentX = lastA = lastB = lastX = count = 0
  
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

if __name__ == '__main__':
   main()
