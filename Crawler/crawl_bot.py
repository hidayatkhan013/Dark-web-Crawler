from typing import Counter
from get_domains import *
from file_manage import *
from link_finder import link_crawler
import requests as urlopen
import tldextract
from launch_tor import *
from bs4 import BeautifulSoup
from store_DB import *
import time
from call_main import *
import sys 



#Importing Stem libraries
from stem import Signal
from stem.control import Controller
import socks, socket


session = urlopen.session()
session.proxies = {'http':  'socks5h://localhost:9150',
                'https': 'socks5h://localhost:9150'}
# r=session.get(link)
Counter=0

class Crawl_bot:

    folder_name, start_link, domain_name, queued_data, crawled_data = '', '', '', '', ''
    queue = set()
    data_crawled = set()

    def __init__(self, folder_name, start_link, domain_name):
        Crawl_bot.folder_name = folder_name
        Crawl_bot.start_link = start_link
        Crawl_bot.domain_name = domain_name
        Crawl_bot.queued_data = Crawl_bot.folder_name + '/queue.txt'
        Crawl_bot.crawled_data = Crawl_bot.folder_name + '/crawled.txt'
        self.initiate_directory()
        self.crawl_page('Spider starts here', Crawl_bot.start_link)

    @staticmethod
    def initiate_directory():                   # Define and create new directory on the first run
        create_project_folder(Crawl_bot.folder_name)
        create_data_files(Crawl_bot.folder_name, Crawl_bot.start_link)
        Crawl_bot.queue = convert_to_set(Crawl_bot.queued_data)
        Crawl_bot.data_crawled = convert_to_set(Crawl_bot.crawled_data)

    @staticmethod
    def crawl_page(thread_name, web_url):      # Fill queue and then update files, also updating user display
        print(web_url)
        if web_url not in Crawl_bot.data_crawled:
            print(thread_name + ' now crawl starts ' + web_url)
            print('Queue_url ' + str(len(Crawl_bot.queue)) + ' | Crawled_url  ' + str(len(Crawl_bot.data_crawled)))
            Crawl_bot.add_url_to_queue(Crawl_bot.collect_url(web_url))
            Crawl_bot.queue.remove(web_url)
            Crawl_bot.data_crawled.add(web_url)
            Crawl_bot.update_folder()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def collect_url(web_url):
        html_data_string = ''
        try:

            received_response = session.get(web_url)
            global Counter
            print()
            print (f"This took counter  [ {Counter} ]")
            print()
            Counter+=1
            if Counter==10:
                restart_tor("firefox.exe")
                Counter=0
                time.sleep(5)



                # print("######################################## time here :  ",b-start_time=="0:00:10","     ",b-start_time)
                
            if 'text/html' in received_response.headers['Content-Type']:
                html_data_string = received_response.encoding = 'utf-8'
                html_data_string = received_response.text
                soup = BeautifulSoup(html_data_string,'lxml').text
                insert_DB(web_url,soup)
            link_finder = link_crawler(Crawl_bot.start_link, web_url)
            link_finder.feed(html_data_string)
            counter = 0
            filename = ((tldextract.extract(web_url)).domain)+"{}.html"
            while os.path.isfile(Crawl_bot.folder_name + '/' + filename.format(counter)):
                counter += 1
            filename = filename.format(counter)

##############################################################################################################################################################################################
#######################################FOR SCRAPPING PURPOSES#################################################################################################################################

            f = open(Crawl_bot.folder_name + '/' + filename, 'w',encoding='utf-8')
            f.write(html_data_string)
            f.close()

###############################################################################################################################################################################################
###############################################################################################################################################################################################

        except Exception as e:
            print(str(e))
            return set()
        return link_finder.page_urls()


    @staticmethod
    def add_url_to_queue(links):          # Queue data saves to project files
        for url in links:
            if (url in Crawl_bot.queue) or (url in Crawl_bot.data_crawled):
                continue
            Crawl_bot.queue.add(url)


    @staticmethod
    def update_folder():                    # Update the project directory
        set_to_file(Crawl_bot.queue, Crawl_bot.queued_data)
        set_to_file(Crawl_bot.data_crawled, Crawl_bot.crawled_data)
