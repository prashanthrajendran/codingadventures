import socket
import collections
from struct import pack,unpack
from util import *

ip_info = collections.namedtuple('ip_info','source header_len')

'''
  function to form the ip header
  @param pkt_id : packet id
  @param source_ip : source ip address
  @param dest_ip : destination ip address

  @returns : the ip header formed using the given information
'''
def ip_header(pkt_id, source_ip, dest_ip):
    ip_ihl = 5
    ip_ver = 4
    ip_tos = 0
    ip_tot_len = 0
    ip_id = pkt_id
    ip_frag_off = 0
    ip_ttl = 255
    ip_proto = socket.IPPROTO_TCP
    ip_check = 0
    ip_saddr = socket.inet_aton(source_ip)
    ip_daddr = socket.inet_aton(dest_ip)
    ip_ihl_ver = (ip_ver << 4) + ip_ihl

    return pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl,
                ip_proto, ip_check, ip_saddr, ip_daddr)

'''
 function to extract the information from ip header
 @param packet : ip packet
 @returns : source ipaddress from the packet and header length
            of the packet as a tuple
'''
def ip_information(packet):

    ip_head = packet[0:20]
    iph = unpack('!BBHHHBBH4s4s', ip_head)

    version_ihl = iph[0]
    ihl = version_ihl & 0xF

    iph_length = ihl * 4
    s_addr = socket.inet_ntoa(iph[8])
    return ip_info(source=s_addr, header_len=iph_length)

'''
  function to check whether the ip checksum is correct
  (i.e) whether the ip packet is received without any loss of information

  @param header : ip header
  @returns : true if the ip checksum is valid
'''
def ip_isvalidchecksum(header):
  return (checksum(header) == 65535)