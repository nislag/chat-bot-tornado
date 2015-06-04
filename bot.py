# coding=UTF-8

# General modules.
import os, os.path
import logging
import sys
from threading import Timer
import string
import random

import feedparser
import urllib
import urllib2
import requests
from lxml import html
import duckduckgo

num_req = 10
shift = 2

class Bot(object):

    def __init__(self, master):
        self.master = master
        
        self.message = {
            '_id': '',
            'from': '',
            'body': '',
        }        
    
        
    def sum_list(self, list_n):
        sum_n = 0;
        for i in list_n:
            sum_n += int(i)            
        return sum_n
    
    
    def sum_func(self):
  
        self.send_bot(self.sum_list(self.command[1:]))
    
    def mean_func(self):
        
        list_n = self.command[1:]
        m = len(list_n)
        res = self.sum_list(list_n)/m
    
        self.send_bot(res)
    
    def news_func(self):
        news = feedparser.parse('http://news.ycombinator.com/rss')
    
        for i in range(num_req):
            self.send_bot(news.entries[i + shift].title)
    
    
    #def duck_func(self, message):
        #url = "http://duckduckgo.com/html"
        #data = urllib.urlencode({'q': 'Python'})
        #results = urllib2.urlopen(url, data)       
    
        ##find = 'http://duckduckgo.com/?q='+self.command[1]
        ##for i in self.command[2:]:
        ##    find += '+'+i
    
        ##find +='&ia=about'    
    
        ##found = feedparser.parse(find)
    
        ##for i in range(2, 11):
        #message["body"] = str(results.read(10))
        #message["from"] = 'Bot'
        #self.send_massage(message)
    
    
    #def duck_func(self, message):
        #url = 'http://duckduckgo.com/html/'
        #params = {
            #'q': 'Python',
            #'s': '0',
        #}
    
        #res = requests.post(url, data=params)
        #doc = html.fromstring(res.text)
    
        #results = [a.get('href') for a in doc.cssselect('#links .links_main a')]
        ##for result in results:
        #message["body"] = results[1]
        #message["from"] = 'Bot'
        #self.send_massage(message)
    
    
    
    
    def duck_func(self):
    
        r = duckduckgo.query(str(self.message["body"])[6:])
        for i in range(num_req):
            self.send_bot(r.related[i].text)
            
            
    def send_bot(self, body,  n_user = 'Bot'):
        self.message["body"] = body
        self.message["from"] = n_user
        self.master.send_massage(self.message)        
    
    def makeBot(self, message):
    
        #split command by spaces    
    
        self.command = message["body"].lower().split(' ')
        self.message = message
    
        try:
            self.com_dict[self.command[0]](self)
        except KeyError:
            self.master.write_message({'error': 1, 'textStatus': 'Error: wrong command'})
    
        return
    
    com_dict = {'!sum': sum_func, '!mean': mean_func, '!news': news_func, '!duck': duck_func}
