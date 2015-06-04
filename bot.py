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



class Bot(object):

    def __init__(self, master):
        self.master = master
        
        self.message = {
            '_id': '',
            'from': '',
            'body': '',
        }        
    
    
    def sum_func(self):
        sum_n = 0
        for i in self.command[1:]:
            sum_n += int(i)
    
        self.send_bot(sum_n)
    
    def mean_func(self):
        sum_n = 0
        m = 0
        for i in self.command[1:]:
            sum_n += int(i)
            m += 1
    
        self.send_bot(sum_n/m)
    
    def news_func(self):
        news = feedparser.parse('http://news.ycombinator.com/rss')
    
        for i in range(2, 12):
            self.send_bot(news.entries[i].title)
    
    
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
    
        r = duckduckgo.query(str(self.message["body"])[5:])
        for i in range(0,10):
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
