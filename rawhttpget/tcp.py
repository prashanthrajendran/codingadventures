import socket
from struct import *
import collections
from util import checksum

# to store the information in the tcp layer
tcp_info = collections.namedtuple('tcp_info','check_sum destination data flags ack seq data_size')

window_size = 5840
port = 0

'''
  initialization function for tcp layer
'''
def tcp_init():
    global port
    port = getport()


'''
 function to calculate the flag value
 all the flags have default value as 0 in this function. Only those flags that has
 to be set needs to passed with value 1 to this function

 @rtype : Integer
 @returns : flag value that can be put inside the tcp packet
'''
def tcp_flags(fin=0,syn=0,rst=0,psh=0,ack=0,urg=0):
    return fin + (syn << 1) + (rst << 2) + (psh <<3) + (ack << 4) + (urg << 5)


'''
 function for forming the tcp header

 @param pkt_seq : sequence number of the packet
 @param ack_seq : ack number that has to be packaged in the header
 @param flags :  flag value to be packaged in the tcp header
 @param check_sum : check_sum of the header, If the checksum is not known
                    this parameter can be left without passing anything. When
                    checksum is not passed 0 will be represented in the checksum
                    field

 @returns : tcp header after packaging the given values
'''
def header(pkt_seq, ack_seq,flags,check_sum=None):
    global port
    # tcp header fields
    tcp_source = port   # source port
    tcp_dest = 80   # destination port
    tcp_doff = 5
    tcp_window = socket.htons(5840)#window size
    tcp_check = 0
    tcp_urg_ptr = 0

    tcp_offset_res = (tcp_doff << 4) + 0

    if not check_sum:
        header = pack('!HHLLBBHHH' , tcp_source, tcp_dest, pkt_seq, ack_seq, tcp_offset_res, flags,
                        tcp_window, tcp_check, tcp_urg_ptr)
    else:
        header = pack('!HHLLBBH' , tcp_source, tcp_dest, pkt_seq, ack_seq, tcp_offset_res, flags,
                      tcp_window) + pack('H',check_sum) + pack('!H', tcp_urg_ptr)

    return header



'''
 function for forming the tcp header

 @param pkt_seq : sequence number of the packet
 @param ack_seq : ack number that has to be packaged in the header
 @param flags :  flag value to be packaged in the tcp header
 @param check_sum : check_sum of the header, If the checksum is not known
                    this parameter can be left without passing anything

 @returns : tcp header after packaging the given values
'''

def tcp_header(pkt_seq, ack_seq,flags, source_ip, dest_ip, payload):
    tcp_check = pseudoheader_checksum(pkt_seq, ack_seq,flags, source_ip, dest_ip, payload)
    tcp_header = header(pkt_seq, ack_seq,flags,tcp_check)
    return tcp_header

'''
 function for retrieving the tcp information from the received packet

 @param packet : received packet
 @param iph_length :ip header length

 @rtype : tcp_info (Refer top of file for tuple definition)
 @returns : field from the tcp segment
'''
def tcp_information(packet, iph_length):

    tcp_header = packet[iph_length:iph_length+20]
    tcph = unpack('!HHLLBBHHH', tcp_header)

    source_port = tcph[0]
    dest_port = tcph[1]
    sequence = tcph[2]
    acknowledgement = tcph[3]
    doff_reserved = tcph[4]
    flags = tcph[5]
    sum = tcph[7]
    tcph_length = doff_reserved >> 4

    h_size = iph_length + tcph_length * 4
    data_size = len(packet) - h_size


    data = packet[h_size:]

    return tcp_info(check_sum= sum,
                    destination=dest_port,
                    data=data,
                    flags=flags,
                    ack=acknowledgement,
                    seq=sequence,
                    data_size=data_size)


'''
  function to calculate the checksum using pseudo header

  @param pkt_seq : sequence number of the packet
  @param ack_seq : sequence number to be sent in the packet
  @param flags : tcp flags to be sent
  @param source_ip : source ip address
  @param dest_ip : destination ip address
  @param payload : tcp payload
  @param tcp_header : tcp_header only if its already known, otherwise it can be left blank

  @returns : the checksum
'''
def pseudoheader_checksum(pkt_seq, ack_seq,flags, source_ip, dest_ip, payload,tcp_header=None):
    if not tcp_header:
        tcp_header = header(pkt_seq, ack_seq,flags)
    source_address = socket.inet_aton(source_ip)
    dest_address = socket.inet_aton(dest_ip)
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    if payload:
        payload_len = len(payload)
    else:
        payload_len = 0
    tcp_length = len(tcp_header) + payload_len
    psh = pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
    if payload:
        psh = psh + tcp_header + payload
    else:
        psh = psh + tcp_header
    return tcp_checksum(psh)


'''
 function to calculate the checksum
 @param data : ip header + tcp header + payload for which check sum has to be calculated
 @returns : calculated checksum
'''
def tcp_checksum(data):
    sum = checksum(data)
    result = (~ sum) & 0xffff
    return result

'''
 function to find the free port
 @returns : free port
'''
def getport():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('localhost', 0))
  addr, port = s.getsockname()
  s.close()
  return port

'''
  function to check whether the received packet's port
  is the intended port(i.e) port used by this code

  @returns : true if the port is intended port
'''
def tcp_isvalidport(tcp_detail):
    return tcp_detail.destination == port
