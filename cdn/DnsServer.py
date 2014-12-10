import SocketServer
import argparse
import struct
import socket
from replica import shortest_rtt_replica

CDN_NAME='' #stores the cdn specific name for which the ip has to be translated


'''
  To understand the values hard coded in the implementation. please refer
  http://www.ccs.neu.edu/home/amislove/teaching/cs4700/fall09/handouts/project1-primer.pdf 
'''

'''
 Handler for UDP server which handles the DNS requests and sends a response
'''
class DnsHandler(SocketServer.BaseRequestHandler):
    
    '''
     function which the receives the incoming the DNS requests and 
     send a response
    '''
    def handle(self):
        packet = self.request[0].strip()
        socket = self.request[1]
        pkt_id = self.dns_packet_id(packet)
        host = self.host_name(packet)
        if host == CDN_NAME:
            replica_ip = shortest_rtt_replica(self.client_address[0])
            response = self.header_for_response(pkt_id) + self.form_question(host) + self.answer_for_response(replica_ip)
        else:
            response = packet
        socket.sendto(response, self.client_address)
    
    '''
    function for extracting the packet id from dns packet
    @param packet: Dns packet received from the client
    @return: packet id of the given dns packet
    '''
    def dns_packet_id(self, packet):
        return int(struct.unpack('!H',packet[:2])[0])
    
    '''
    function for extracting the host name from dns packet
    @param packet: Dns packet received from the client
    @return: host name of the given dns packet
    '''
    def host_name(self, packet):
        packet = packet[12:]
        length = ord(packet[0])
        start = 1
        hostname = []
        while not length == 0:
            hostname.append(packet[start:start+length])
            start += length + 1
            length = ord(packet[start-1])
        return ".".join(hostname)
    
    '''
    function for constructing the dns header for response
    @param param: packet id of the received dns packet
    @return: header for the response
    '''
    def header_for_response(self, packet_id):
        flags = 33152
        one = 1
        nothing = 0  
        return struct.pack('!HHHHHH', packet_id,flags, one, one, nothing, nothing)
    
    '''
    function for constructing the answer part of the response
    @param ip: ip address mapping for the host name in the request
    @return: answer section of dns response  
    '''
    def answer_for_response(self, ip):
        ttl = 100
        return struct.pack('!HHHLH4s', 49164, 1, 1,
                          ttl, 4, socket.inet_aton(ip))
    
    '''
    function for constructing the question part of response packet
    @param domain: host name received in the dns request packet
    @return: question section of dns response
    '''
    def form_question(self, domain):
        parts = domain.split('.')
        qname = []
        for part in parts:
            qname.append(chr(len(part)))
            qname.append(part)
        qname.append(chr(0))
        return ''.join(qname) + struct.pack('!HH',1,1)
    
'''
  Entry point after launching DNS server
'''        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--cdnname", type=str, required=True)
    parser.add_argument("-p", "--port", type=int, required=True)
    args = parser.parse_args()
    port = args.port
    CDN_NAME = args.cdnname 
    server = SocketServer.UDPServer(('', port), DnsHandler)
    server.serve_forever()