Tornado-Redis-Chat
==================

A mutli-room chat application based on Tornado and Redis

This is an example of a mutli-room chat application based on the asynchronous
web framework [Tornado](http://www.tornadoweb.org/). It uses [Redis Pup/Sub](http://redis.io/topics/pubsub)
feature as a message queue to distribute chat messages to multiple instances in a mutli-process
setup. This way you can run this application in mutliple instances behind a load balancer
like [ninx](http://nginx.org/). It uses [brukva](https://github.com/evilkost/brukva) as asynchronous
Redis client. Client-Server communication is based on [websockets](http://www.tornadoweb.org/en/stable/websocket.html).

**Note**: Please note that this is just an example project for demonstration purpose only. It is little tested
and missing important features like authenticated websockets, input validation and so on. It is intended
to show how to build a scalable real-time web application with [Tornado](http://www.tornadoweb.org/).

## Requirements and Setup
First of all you need Redis:
```
sudo apt-get install redis-server
```
Next you need the following python packages:
```
sudo pip install tornado
sudo pip install git+https://github.com/evilkost/brukva.git
```
Finally clone this repository:
```
git clone https://github.com/nislag/chat-bot-tornado.git chat
cd chat
```

## Run Application
You can run the application on a specific port like that:
```Bash
python app.py --port=8888
```
Open `localhost:8888` in your browser and see the result!
