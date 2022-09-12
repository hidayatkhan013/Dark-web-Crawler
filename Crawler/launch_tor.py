import os
import subprocess
import time


def launchTor():
    # start Tor (wait 30 sec for Tor to load)
    sproc = subprocess.Popen(r'C:\Users\A46\Desktop\Tor Browser\Browser/firefox.exe')
    time.sleep(3)
    return sproc

def isTorRunning(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())





def restart_tor(process_name):
    os.system(f'"taskkill /IM {process_name} /F"')
    time.sleep(2)
    if not isTorRunning('tor.exe'):
        launchTor()


