# coding: utf8

import os
import sys
import random
import psutil
import time
import subprocess
import platform
import shutil
import threading
from tqdm import tqdm
from elevate import elevate
import webbrowser
import subprocess

# Installing Scoop
def install_scoop():
    os.system('powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"')
    print('[+] Added ExecutionPolicy for Installing External Scripts')
    os.system('powershell -Command "iwr -useb get.scoop.sh -outfile "install.ps1"')
    print('[+] Successfully Downloaded Installer Script for Scoop')
    os.system('powershell -Command ".\install.ps1"') 
    print('[+] Scoop Install Completed, For Refrence check https://scoop.sh/') 

# Installing Scoop Apps
def install_scoop_apps():
    os.system('powershell scoop bucket add extras')
    # Installing Foxit Reader using Scoop app
    os.system('powershell scoop install foxit-reader')
    # installing python via. Scoop App
    os.system('powershell scoop install python')
def install_dependencies():
    # installing python dependencies
    os.system('python -m pip install --upgrade pip')
    os.system('python -m pip install -r requirements.txt')
    print('[+] Setup Completed!')

if __name__ == '__main__':

    install_scoop()
    install_scoop_apps()
    install_dependencies()