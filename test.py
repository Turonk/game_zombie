#!/bin/python3
import os
import time
import shutil
import subprocess
from optparse import OptionParser
from sys import argv
from os.path import abspath, dirname

parser = OptionParser()

parser.add_option('-d', '--debug', dest='debug',
                  action='store_true', default=False,
                  help="make debug")

options, args = parser.parse_args()

if options.debug:
    print('Ddebug flag is set')
else:
    print('Debug flag is not set')

print('Script is launched from dir:', dirname(abspath(argv[0])))

if args:
    print('The rest args:', args)


deployPath="/home/pi/writefolder/heliox_lcd_deploy"
maincycle = True
a = 0
b = 0
i_usb = 0
print('Script running...')

def shutdown():
    print(">>> Shutdown....")
    subprocess.call(["shutdown", "-f", "-s", "-t", "0"])

def reboot():
    print(">>> Reboot....")
    subprocess.call(["shutdown", "-f", "-r", "-t", "0"])

def kill_programm():
    print(">>>Kill heliox programm...")
    os.system('killall -9 one')

def start_programm():
    print(">>> Start heliox programm...")
    os.system(deployPath + "/heliox_lcd/one &")

def build_programm():
    print(">>> Build heliox programm...")
    os.system("cd /home/pi/writefolder/heliox_lcd_deploy/heliox_lcd; qmake one.pro -spec linux-g++; make")

def clear():
    print(">>> Clean...")
    os.system("cd /home/pi/writefolder/heliox_lcd_deploy/heliox_lcd; make clean")


while maincycle:
    for root, dirs, files in os.walk("/home/pi/writefolder/usb"):
        if i_usb < 2:
            usb = root
            i_usb += 1

    if not options.debug:
        time.sleep(2)
        if os.access(usb + "/heliox_debug", os.F_OK) == True:
            time.sleep(2)
            kill_programm()
            os.system("python /home/pi/writefolder/heliox_lcd_deploy/terminal_heliox.py")
            time.sleep(1)
            quit()

    if b == 2:
        file_brake = "/home/pi/writefolder/heliox_data/brake"
        if not os.access(file_brake, os.F_OK) == True:
            file = open(file_brake, 'w')
            file.close()
        time.sleep(1)
        alarm_start = "/home/pi/writefolder/heliox_data/alarm_start"
        if os.access(file_brake, os.F_OK) == True:
            time.sleep(2)
            kill_programm()
            file = open(alarm_start, 'w')
            file.close()
            start_programm()
        b = 0

    if os.access(deployPath+"/settime.sh", os.F_OK) == True:
        time.sleep(2)
        print(">>>Set time...")
        os.system('chmod 777', deployPath+'/settime.sh')
        os.system(deployPath+'/settime.sh')
        os.remove(deployPath+"/settime.sh")

    if a == 0:
        if os.access(usb + "/one_deploy", os.F_OK) == True:
            time.sleep(2)
            kill_programm()
            print(">>> Delete file ONE...")
            os.remove(deployPath+"/heliox_lcd/one")
            print(">>> Copy file...")
            shutil.copy(usb + '/one_deploy', '/home/pi/writefolder/heliox_lcd_deploy/heliox_lcd/one', follow_symlinks=True)
            a = 1
            start_programm()

    if os.access(deployPath + "/start", os.F_OK) == True:
        time.sleep(2)
        os.remove(deployPath+"/start")
        start_programm()

    if os.access(deployPath + "/stop", os.F_OK) == True:
        time.sleep(2)
        os.remove(deployPath+"/stop")
        kill_programm()

    if os.access(deployPath + "/build", os.F_OK) == True:
        time.sleep(2)
        os.remove(deployPath + "/build")
        kill_programm()
        build_programm()

    if os.access(deployPath + "/buildRun", os.F_OK) == True:
        time.sleep(2)
        os.remove(deployPath + "/buildRun")
        kill_programm()
        build_programm()
        start_programm()

    if os.access(deployPath + "/cleanBuild", os.F_OK) == True:
        time.sleep(2)
        os.remove(deployPath + "/cleanBuild")
        kill_programm()
        clear()
        build_programm()

    if os.access(deployPath + "/cleanBuildRun", os.F_OK) == True:
        time.sleep(2)
        os.remove(deployPath + "/cleanBuildRun")
        kill_programm()
        clear()
        build_programm()
        start_programm()

    if os.access(deployPath + "/shutdown", os.F_OK) == True:
        time.sleep(2)
        os.remove(deployPath+"/shutdown")
        shutdown()

    if os.access(deployPath + "/reboot", os.F_OK) == True:
        time.sleep(2)
        os.remove(deployPath+"/reboot")
        reboot()

    if os.access(deployPath + "/remove", os.F_OK) == True:
        time.sleep(2)
        os.remove(deployPath + "/remove")
        kill_programm()
        print(">>> Heliox dir remove...")
        shutil.rmtree(deployPath+"/heliox_lcd")

    b += 1
    time.sleep(1)









