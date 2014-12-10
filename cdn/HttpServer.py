'''
Handling of storage limit (10 MB in cache of ec2 server): 
page hits and contents of the page both are stored in hard drive. Hence, in case of ec2 servers
more than 10MB of contents can't be stored. What ever is being stored in the hard drive is loaded
to RAM for performance. As contents in hard drive in less than or equal to 10 MB the contents in
the RAM also cannot exceed 10 MB.
'''

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import argparse
import urllib2
import heapq
import errno
import os
from _heapq import heappop

ORIGIN_SERVER = ''
pagehits = []
pages = {}

'''
Handler for handling the incoming requests to HTTP Server
'''
class HttpHandler(BaseHTTPRequestHandler):
    
    '''
     receives the get request and returns the response
    '''
    def do_GET(self):
        f = self.file_name()
        if f in pages:
            html = pages[f]
            self.increase_page_hit(f)
            status = 200
        else:
            status,html = self.fetch_from_origin()
        self.send_response(status)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(html)
        return
    
    '''
     function for fetching the content from origin server and storing it in cache
     @return: response code and the content returned form the origin server
    '''
    def fetch_from_origin(self):
        try:
            response = urllib2.urlopen("".join(['http://',ORIGIN_SERVER, self.path]))
        except urllib2.URLError, e:
            return (e.code, '')
        file_name = self.file_name()
        html = response.read()
        try:
            self.put_in_cache(file_name, html)
        except IOError as ex:
            if ex.errno == errno.EDQUOT:
                self.handle_cachefull(html)
        return (response.code,html)
    
    '''
     function for increasing the page hit
     @param page_file: name of the content file for which hit count has to be increased 
    '''
    def increase_page_hit(self, page_file):
        i = [y[1] for y in pagehits].index(page_file)
        count_tuple = pagehits[i]
        pagehits[i] = pagehits[-1]
        pagehits.pop()
        heapq.heapify(pagehits)
        heapq.heappush(pagehits, (count_tuple[0] + 1, page_file))
        self.create_count_file(page_file, count_tuple[0] + 1)
    
    '''
    function for replacing the least frequently used page in the cache
    @param html: content that has to be stored in the cache 
    '''
    def handle_cachefull(self, html):
        file_name = self.file_name()
        while pagehits:
            lowest_hit = heappop(pagehits)
            self.remove_from_cache(lowest_hit[1])
            try:
                self.put_in_cache(file_name, html)
                break
            except IOError as ex:
                if ex.errno == errno.EDQUOT:
                    continue
                else:
                    break
    
    '''
    function for storing the content in the cache
    @param html: content that has to be stored in cache 
    '''
    def put_in_cache(self, page_file, html):
        with open(self.data_file(page_file), 'w') as f:
            f.write(html)
        self.create_count_file(page_file, 1)
        pages[page_file] = html
        heapq.heappush(pagehits, (1, page_file))
    
    '''
    function for removing the content form the cache
    @param file_name: name of the content file that has to be removed 
    '''
    def remove_from_cache(self, file_name):
        delete_file(self.data_file(file_name))
        delete_file(self.count_file(file_name))
        if file_name in pages:
            del pages[file_name]
    
    '''
    function for creating the file to store the page hit
    @param file_name: name of the content file for which page hits has to be stored
    @param count: page hit   
    '''
    def create_count_file(self, file_name, count):
        with open(self.count_file(file_name), 'w') as f:
            f.write(str(count))
    
    '''
    function for converting the path received form the request to file name to store its contents
    @return: file name for the path name
    '''
    def file_name(self):
        return self.path.replace("/","-")
    
    '''
    function for converting the content file name to file name which stores its respective page hits
    @param page_file: name of the content file that has to be converted to its corresponding file for
    storing page hits  
    @return: page hits file for the given content file
    '''
    def count_file(self, page_file):
        return "".join([ORIGIN_SERVER,'-',page_file,'.count'])
    
    '''
     function for adding the extension of .data to indicate the data file
     @param page_file: content file name for which .data extension has to be added
     @return: .data file for the given content file 
    '''
    def data_file(self, page_file):
        return "".join([ORIGIN_SERVER,'-',page_file,'.data'])
    
    '''
    function for logging messages in the sever. It doesn't do anything to override the
    default log behavior of the BaseHTTPRequestHandler
    '''
    def log_message(self, format, *args):
        return
    
'''
function for deleting a file
@param file_name: name of the file that has to be deleted 
'''
def delete_file(file_name):
    try:
        os.remove(file_name)
    except OSError:
        pass

'''
function to delete cleanup before starting the server.
Deletes those file form cache which are not fetched form the current origin server
'''
def cleanup():
    files = [f for f in os.listdir(".") 
             if not f.startswith(ORIGIN_SERVER) and (f.endswith('.count') or f.endswith('.data'))]
    for f in files:
        delete_file(f)
    
'''
function to retrieve the contents of a file
@param file_name: name of the file whose contents has to be retrieved
@return: content of the given file 
'''
def get_contents(file_name):
    with open(file_name, 'r') as content_file:
        content = content_file.read()
    return content

'''
function for loading the data to RAM form the cache
'''
def load_data():
    cleanup()
    files = [f for f in os.listdir(".")
             if f.endswith('.count') or f.endswith('.data')]
    for f in files:
        if f.endswith('.data'):
            name = f[len(ORIGIN_SERVER)+1:][:-5] 
            pages[name] = get_contents(f) 
        else:
            name = f[len(ORIGIN_SERVER)+1:][:-6] 
            heapq.heappush(pagehits, (int(get_contents(f)), name))

'''
 Entry point when launching the HTTP server
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--origin", type=str, required=True)
    parser.add_argument("-p", "--port", type=int, required=True)
    args = parser.parse_args()    
    ORIGIN_SERVER = args.origin
    load_data()
    HttpServer = HTTPServer(('', args.port), HttpHandler)
    HttpServer.serve_forever()