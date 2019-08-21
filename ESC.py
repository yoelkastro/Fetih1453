# This program will let you test your ESC and brushless motor.
# Make sure your battery is not connected if you are going to calibrate it at first.
# Since you are testing your motor, I hope you don't have your propeller attached to it otherwise you are in trouble my friend...?
# This program is made by AGT @instructable.com. DO NOT REPUBLISH THIS PROGRAM... actually the program itself is harmful                                             pssst Its not, its safe.

import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library
import Adafruit_PCA9685
import keyboard
import thread

def pressEnter(): #Function that presses the enter key
    while True:
        keyboard.press("enter")
        time.sleep(0.01)
        keyboard.release("enter")
        time.sleep(0.01)

ESC=4  #Connect the ESC in this GPIO pin 

pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC, 0)

pwm = Adafruit_PCA9685.PCA9685(address=0x49)

servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
dumen_ang = 370
arm_ver = 0  # 0 -> 450
arm_hor = 0

max_value = 2000 #change this if your ESC's max value is different or leave it be
min_value = 700  #change this if your ESC's min value is different or leave it be
print "For first time launch, select calibrate"
print "Type the exact word for the function you want"
print "calibrate OR manual OR control OR arm OR stop"

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

def manual_drive(): #You will use this function to program your ESC if required
    print "You have selected manual option so give a value between 0 and you max value"    
    while True:
        inp = raw_input()
        if inp == "stop":
            stop()
            break
	elif inp == "control":
		control()
		break
	elif inp == "arm":
		arm()
		break	
        else:
            pi.set_servo_pulsewidth(ESC,inp)
                
def calibrate():   #This is the auto calibration procedure of a normal ESC
    pi.set_servo_pulsewidth(ESC, 0)
    print("Disconnect the battery and press Enter")
    inp = raw_input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = raw_input()
        if inp == '':            
            pi.set_servo_pulsewidth(ESC, min_value)
            print "Wierd eh! Special tone"
            time.sleep(7)
            print "Wait for it ...."
            time.sleep (5)
            print "Im working on it, DONT WORRY JUST WAIT....."
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print "Arming ESC now..."
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print "See.... uhhhhh"
            control() # You can change this to any other function you want
            
def control():
    global dumen_ang
    global arm_ver
    global arm_hor
    print "I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'"
    time.sleep(1)
    speed = 1500    # change your speed if you want to.... it should be between 700 - 2000
    print "Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed"
    thread.start_new_thread(pressEnter, ())
    while True:
        pi.set_servo_pulsewidth(ESC, speed)
        inp = raw_input()
        
        if inp == "a":
            speed -= 100    # decrementing the speed of ESC like hell
            print "speed = %d" % speed
        elif inp == "q":    
            speed += 100    # incrementing the speed of ESC like hell
            print "speed = %d" % speed

        elif inp == "w" and servo_ang < 500:
            dumen_ang += 40
        elif inp == "s" and servo_ang > 200: 
            dumen_ang -= 40

        elif inp == "w" and arm_ver < 450:    
            arm_ver += 10
        elif inp == "s" and arm_ver > 0:    
            arm_ver -= 10

        elif inp == "w" and arm_hor < 450:
            dumen_ang += 10
        elif inp == "s" and arm_hor > 0:    
            dumen_ang -= 10
       
        elif inp == "stop":
            stop()          #going for the stop function
            break	
        elif inp != "":
            print "WHAT DID I SAID!! Make good input please thank you"

        pwm.set_pwm(15, 0, dumen_ang)  # Dümen

        pwm.set_pwm(14, 0, arm_ver + 150)
        pwm.set_pwm(13, 0, 600 - arm_ver)

        pwm.set_pwm(12, 0, arm_hor + 150)
        pwm.set_pwm(11, 0, 600 - arm_hor)
            
def arm(): #This is the arming procedure of an ESC 
    print "Connect the battery and press Enter"
    inp = raw_input()    
    if inp == '':
        pi.set_servo_pulsewidth(ESC, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, min_value)
        time.sleep(1)
        control() 
        
def stop(): #This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()



#This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.
time.sleep(5)
arm()