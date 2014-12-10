import socket
import os
import sys
import collections
from ip import ip_header, ip_information, ip_isvalidchecksum
from tcp import tcp_header, tcp_flags, tcp_information, tcp_init, tcp_isvalidport
from util import *
from random import randint
from multiprocessing import Process, Queue
from http import request, body
from urlparse import *


'''
  receives the url form command line
'''
try:
    web_url = sys.argv[1]
except Exception, e:
    print "Given Input is not in valid format"
    os._exit(1)


'''
 parsing the url to pick the file name and to calculate the destination ip
'''
try:
    o = urlparse(web_url)
    filename = o.path.split('/')[len(o.path.split('/'))-1]
    dest_ip = socket.gethostbyname(o.hostname)
except Exception, e:
    print "Not a valid url"
    os._exit(1)

if filename == "":
    filename = "index.html"

send_socket = None
receive_socket = None
pkt_id = randint(11, 20) # packet id
source_ip = socket.gethostbyname("%s.local" % socket.gethostname()) # local host ip address
pkt_seq = randint(2, 10) # sequence number of outgoing packet
ack_seq = 0 # acknowledgement number to be sent
prev_packet = collections.namedtuple('packet', 'flags ack data') #details of recent outgoing packet


'''
  function for initializing the sockets and creating/clearing the file
'''
def init():
    global send_socket
    global receive_socket
    try:
        receive_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        tcp_init()
        open(filename,'w').close()
        send_socket.connect((dest_ip, 0))
    except socket.error, msg:
        print str(msg)
        os._exit(1)


'''
 function for sending the message to the server

 @type flags : Integer
 @param flags : tcp flags that has to sent in the outgoing packet

 @type ack_seq : Integer
 @param ack_seq : acknowledgement number that has to sent in the outgoing packet

 @type message : String
 @param message : payload to be sent
'''
def send(flags, ack_seq, message):
    global pkt_seq, send_socket,pkt_seq, pkt_id, dest_ip, source_ip
    pkt_id += 1
    ip_head = ip_header(pkt_id, source_ip, dest_ip)
    tcp_head = tcp_header(pkt_seq, ack_seq,flags, source_ip, dest_ip, message)
    if message:
        packet = ip_head + tcp_head + message
    else:
        packet = ip_head + tcp_head
    send_socket.sendto(packet, (dest_ip, 0))


'''
 function to receive data packet from server. This function implements timeout of 3 minutes
 to receive packets form the server. If no packet is received from the server in 3 minutes
 then it terminates the execution

 @return : packet received form the server
'''
def receive_from_target():
    q = Queue()
    p = Process(target=receive_from_socket, args=(q,))
    p.start()
    # Wait for 3 minutes or until process finishes
    p.join(180)
    if p.is_alive():
        p.terminate()
        p.join()
        print "for past 3 minutes nothing is heard from the server"
        os._exit(1)
    else:
        return q.get()


'''
  function for receiving the ack from the server
  @type last_packet : prev_packet, a named tuple (refer the top of file for definition)
  @param last_packet : last outgoing packet to the server

'''
def receive_ack(last_packet):
    counter = 0
    while True:
        q = Queue()
        p = Process(target=receive_from_socket, args=(q,))
        p.start()
        p.join(60)
        if p.is_alive():
            counter += 1
            p.terminate()
            p.join()
            if counter == 3:
                print "for past 3 minutes nothing is heard from the server"
                os._exit(1)
            send(last_packet.flags, last_packet.ack, last_packet.data)
        else:
            rec_packet = q.get()
            raw_packet = rec_packet[0]
            ip_detail = ip_information(raw_packet)
            tcp_detail = tcp_information(raw_packet, ip_detail.header_len)
            if is_acceptable(tcp_detail.seq):
                return tcp_detail


'''
    function to receive packets from the server. It receives all the incoming packets and
    filters the packet based on the server ip and port address

    @returns : received packet from the server
'''
def receive_from_socket(q):
    while True:
        raw_packet = receive_socket.recvfrom(65565)
        packet = raw_packet[0]
        ip_detail = ip_information(packet)
        if not (str(ip_detail.source) == dest_ip): continue # validating ip address
        tcp_detail = tcp_information(packet, ip_detail.header_len)
        if not (tcp_isvalidport(tcp_detail)): continue # validating port no
        q.put(raw_packet)
        break


'''
    function to validate the received packet's checksum

    @rtype : tcp_info (Refer tcp.py for its definition)
    @returns : information from tcp segment
'''
def receive():
    global dest_ip, source_ip
    while True:
        packet = receive_from_target()
        packet = packet[0]
        ip_detail = ip_information(packet)
        tcp_detail = tcp_information(packet, ip_detail.header_len)
        if not (ip_isvalidchecksum(packet[0:20])): continue # validating ip checksum
        return tcp_detail

'''
    function for three way handshake
'''
def three_way_handshake():
    global ack_seq, pkt_seq
    send(tcp_flags(syn=1),ack_seq,None)
    tcp_detail = receive()
    if is_syn(tcp_detail.flags) and is_ack(tcp_detail.flags):
        pkt_seq = tcp_detail.ack
        ack_seq = tcp_detail.seq + 1
        send(tcp_flags(ack=1), ack_seq, None)


'''
 function to download the data using the url given to the program
 while launching it
'''
def download():
    global pkt_seq, ack_seq
    first_packet = True
    send(tcp_flags(ack=1), ack_seq, request(o.path, o.hostname))
    tcp_detail = receive_ack(prev_packet(tcp_flags(ack=1), ack_seq, request(o.path, o.hostname)))#receive()
    if is_ack(tcp_detail.flags) and tcp_detail.seq == ack_seq:
        while True:
            tcp_detail = receive()
            if not is_acceptable(tcp_detail.seq):
                send(tcp_flags(ack=1), ack_seq, None)
                continue
            modify_seq(tcp_detail)

            # -------for connection tear down---------
            if is_ack(tcp_detail.flags) and is_fin(tcp_detail.flags):
                if tcp_detail.data_size == 0:
                    inc_ack(tcp_detail)
                else:
                    with open(filename, 'a') as f:
                        f.write(tcp_detail.data)
                    modify_ack(tcp_detail)
                send(tcp_flags(fin=1,ack=1),ack_seq, None)
                tcp_detail = receive_ack(prev_packet(tcp_flags(fin=1,ack=1),ack_seq, None))#receive()
                if is_ack(tcp_detail.flags) and is_fin(tcp_detail.flags) and \
                        is_acceptable(tcp_detail.seq):
                    inc_ack(tcp_detail)
                    modify_seq(tcp_detail)
                    send(tcp_flags(fin=1,ack=1),ack_seq,None)
                break
            # -------end of connection tear down---------

            # -------for file download---------
            else:
                modify_ack(tcp_detail)
                if first_packet:
                    first_packet = False
                    data_to_write = body(tcp_detail.data)
                else:
                    data_to_write = tcp_detail.data
                with open(filename, 'a') as f:
                    f.write(data_to_write)
                send(tcp_flags(ack=1),ack_seq, None)
            # -------end of file download---------


'''
 function to calculate the ack to be sent for the packet received.

 @type tcp_detail : tcp_info (a named tuple defined in tcp.py)
 @param : tcp packet received recently
'''

def modify_ack(tcp_detail):
    global ack_seq
    ack_seq += tcp_detail.data_size



'''
 function to calculate the sequence number of the outgoing packet

 @type tcp_detail : tcp_info (a named tuple defined in tcp.py)
 @param : tcp packet received recently
'''
def modify_seq(tcp_detail):
    global pkt_seq
    pkt_seq = tcp_detail.ack


'''
  function to increment the current ack (i.e)
  sequence of recently received tcp packet + 1
'''
def inc_ack(tcp_detail):
    global ack_seq
    ack_seq = tcp_detail.seq + 1


'''
    function to check whether the sequence of the received sequence number
    is same as the acknowledgement previously sent
'''
def is_acceptable(curr_seq):
    global ack_seq
    return curr_seq == ack_seq


'''
 entry point of program
'''
if __name__ == "__main__":
    init()
    three_way_handshake()
    download()