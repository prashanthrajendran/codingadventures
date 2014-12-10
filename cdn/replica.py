'''
 file for choosing the best replica server 
'''

import json
import urllib
import random
import socket
from threading import Lock, Timer, Thread
from math import *
import traceback
import logging
import time
from Queue import Queue

optimal_replica = {}
replica_probe_port = 59587 
lock = Lock()
queue = Queue(100)
connections = {}

contents = [['ec2-54-174-6-90.compute-1.amazonaws.com', u'54.174.6.90', -77.488, 39.044],
        ['ec2-54-149-9-25.us-west-2.compute.amazonaws.com', u'54.149.9.25', -119.529, 45.779],
        ['ec2-54-67-86-61.us-west-1.compute.amazonaws.com', u'54.67.86.61', -122.42, 37.775],
        ['ec2-54-72-167-104.eu-west-1.compute.amazonaws.com', u'54.72.167.104', -6.249, 53.333],
        ['ec2-54-93-182-67.eu-central-1.compute.amazonaws.com', u'54.93.182.67', 8.683, 50.117],
        ['ec2-54-169-146-226.ap-southeast-1.compute.amazonaws.com', u'54.169.146.226', 103.856, 1.293],
        ['ec2-54-65-104-220.ap-northeast-1.compute.amazonaws.com', u'54.65.104.220', 139.69, 35.69],
        ['ec2-54-66-212-131.ap-southeast-2.compute.amazonaws.com', u'54.66.212.131', 151.206, -33.862],
        ['ec2-54-94-156-232.sa-east-1.compute.amazonaws.com', u'54.94.156.232', -55, -10]]


'''
To establish connection with all the replica servers and store it
'''
def init():
    global connections, replica_probe_port
    for replica in contents:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((replica[1], replica_probe_port))
        connections[replica[1]] = s

    
'''
 function for calculating distance between the given lat long points
 @param lon1: longitude 1
 @param  lat1: latitude 1
 @param lon2: longitude 2
 @param lat2: latitude 2
 @return:  distance between (lon1,lat1) and (lon2,lat2)   
 
 distance is calculated based on Haversine formula
 reference :
 http://en.wikipedia.org/wiki/Haversine_formula 
 http://rosettacode.org/wiki/Haversine_formula
'''
def distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    lon_distance = lon2 - lon1 
    lat_disatnce = lat2 - lat1 
    a = sin(lat_disatnce/2)**2 + cos(lat1) * cos(lat2) * sin(lon_distance/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

'''
 function for choosing the closest replica server for given ip
 @param ip: ip address of the client from which HTTP request is received
 @return: ip address of the replica server which is closest to the given ip address 
'''
def nearby_replica(ip):
    dns_map =dict()
    try:
        response = (urllib.urlopen("http://www.telize.com/geoip/"+ip).read())
        j = json.loads(response)
        for content in contents:
            dns_map[content[1]] = distance(j['longitude'],j['latitude'],content[2],content[3]) 
        return min(dns_map, key=dns_map.get)
    except Exception, e:
        return contents[random.randint(0,len(contents))][1]


'''
 To probe each replica server with the client ip and the get the rtt
'''
def probe_replica(client_ip, replica_ip, temp_rtt_holder, l_lock):
    s = connections[replica_ip] 
    s.sendall(client_ip)
    rtt = s.recv(1024)
    float(rtt)
    with l_lock:
        temp_rtt_holder.append((replica_ip,float(rtt)))
    
        
'''
 To probe all the replica servers by creating thread for each and finally choosing
 server with minimum rtt 
'''
def probe_replicas(client_ip):
    temp_rtt_holder = []
    threads = []
    l_lock = Lock()
    for replica in contents:
        t = Thread(target=probe_replica, args = (client_ip,replica[1],temp_rtt_holder, l_lock))
        t.start()
        threads.append(t)
    [x.join() for x in threads]
    min_rtt_ip = min(temp_rtt_holder, key = lambda t: t[1])[0]
    return min_rtt_ip

'''
Thread which will be responsible for choosing the replica for newly incoming client
'''
class ConsumerThread(Thread):
    def run(self):
        global queue
        while True:
            try:
                client_ip = queue.get(block=True, timeout=None)
                best_replica = probe_replicas(client_ip)
            except Exception, e:
                continue
            queue.task_done()
            with lock:
                optimal_replica[client_ip] = best_replica

'''
method invoked by dns to find the best replica server. If the client visits the dns for
first time then geographically closest server will be returned otherwise the best replica
for the client will be returned from the cache
'''
def shortest_rtt_replica(ip):
    global queue
    with lock:
        if not ip in optimal_replica:
            optimal_replica[ip] = nearby_replica(ip)
            queue.put(ip)
    return optimal_replica[ip]

init()
ConsumerThread().start()
