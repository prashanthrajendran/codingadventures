'''
file for caclulating the rtt for the given ip
'''

import SocketServer
import commands
import logging

COMMAND_FILE = "scamper -c 'ping -c 1' ips | grep 'time=' | awk -v OFS='\t' '{print substr($4, 0, length($4)-1),substr($7,6,length($7))}'"
COMMAND_IP = "scamper -c 'ping -c 1' -i {{ }} | grep 'time=' | awk -v OFS='\t' '{print substr($4, 0, length($4)-1),substr($7,6,length($7))}'"
COMMAND_PING = "ping -c 1 {{ }} | grep 'rtt' | cut -d '=' -f 2 | cut -d '/' -f 2"
PORT = 59587

'''
Handler for the socket server calculates rtt and returns
'''
class ProbeHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                ip = self.request.recv(1024).strip()
                rtt = commands.getoutput(COMMAND_PING.replace('{{ }}', ip))
                float(rtt)
                self.request.sendall(rtt)
            except Exception, ex:
                self.request.sendall('ping failed')
    
    def receive(self, s):
        recmsg = s.recv(4096)
        fullmsg = ""
        while recmsg:
            fullmsg = fullmsg + recmsg
            recmsg = s.recv(4096)
        return fullmsg.strip()
        
if __name__ == "__main__":
    server = SocketServer.TCPServer(('', PORT), ProbeHandler)
    server.serve_forever()
