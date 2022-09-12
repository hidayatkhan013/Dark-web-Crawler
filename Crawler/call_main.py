from multiprocessing import Pool
import os
import time
from launch_tor import *
from subprocess import *
from P_queue import *




def start_simple_q(url):
    BASE_URL = url
    execute = str('python main.py ' + BASE_URL)
    os.system(f"start cmd /k {execute}")


def menu():
    print(" 1--- Launch Crawler with Queue")
    print(" 2--- Add link to priority")
    select=input("choose from above : ")
    return int(select)

def pool_thread():
    with open("onionlinks.txt", "r") as websites:
        content = websites.read().splitlines()
    start_time = time.time()
    with Pool(processes=4) as pool:
        for website in range(0, len(content)):
            pool.apply(start_simple_q, args=(content[website],))
    print("--- %s seconds ---" % (time.time() - start_time))
    

if __name__ == '__main__':
    if not isTorRunning('tor.exe'):
        launchTor()
    while True:
        select=menu()
        if select==1:
            pool_thread()
        elif select==2:
            p_queue()




