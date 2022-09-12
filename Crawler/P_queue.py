from queue import PriorityQueue
import os
import requests as rq
import tldextract
from bs4 import BeautifulSoup
from store_DB import *

session1 = rq.session()
session1.proxies = {'http':  'socks5h://localhost:9150',
                'https': 'socks5h://localhost:9150'}


def get_session(link):
    sess = session1.get(link)
    return sess


def p_queue():
    q = PriorityQueue()
    if not os.path.exists('Priority'):
        os.makedirs('Priority')
    Input=int(input("How many URLs do want to add : "))
    for i in range(0,Input):
        p_url=input("enter URL : ")
        p_prior=input("enter Priority : ")
        q.put((p_prior,p_url))
    while not q.empty():
        url=q.get()
        r=get_session(url[1])
        html_data_string = r.encoding = 'utf-8'
        html_data_string = r.text
        soup = BeautifulSoup(html_data_string,'lxml').text
        insert_DB(((tldextract.extract(url[1])).domain),soup)
        f = open("Priority/"+((tldextract.extract(url[1])).domain)+'.html', 'w',encoding='utf-8')
        f.write(html_data_string)
        f.close()
        print(url[1]," Save succesfully")



