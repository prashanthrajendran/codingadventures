import socket   #for sockets
import re # for regular expression
from bs4 import BeautifulSoup # for parsing html
import os # for exit
import sys # for command line arguments

host = 'cs5700f14.ccs.neu.edu' # server name containing fakebook
port = 80 #  default HTTP port
cookie = {} # dictionary to store cookie

'''
 function for creating the TCP socket used to send HTTP Requests and read Responses
 @rtype: socket
 @return: socket after establishing connection on port 80 with the server having fakebook
'''
def getSocket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = socket.gethostbyname( host )
        s.connect((ip , port))
        return s
    except socket.error:
        print 'Failed to create socket'
        os._exit(1)
    except socket.gaierror:
        print 'Hostname could not be resolved. Exiting'
        os._exit(1)


'''
function which sends the given message (HTTP Requests) to server and gets the Response back

@type message: String
@param message: HTTP Requests that has to be sent to the server

@rtype: String
@return: HTTP Response from the server for the given Request
'''
def sendToServer(message):
    s = getSocket()
    try :
        #Send the whole string
        s.sendall(message)
    except socket.error:
        #Send failed
        print 'Send failed'
        os._exit(1)
    recmsg = s.recv(4096)
    fullmsg = ""
    while recmsg:
        fullmsg = fullmsg + recmsg
        recmsg = s.recv(4096)
    return fullmsg


'''
 function for extracting the header from the HTTP Response
 
 @type message: String
 @param message: HTTP Response from the server
 
 @rtype: String
 @return: Header of the given HTTP Response
'''
def header(message):
    return message.split("\n\n",1)[0]


'''
 function for extracting the body from the HTTP Response
 
 @type message: String
 @param message: HTTP Response from the server
 
 @rtype: String
 @return: Body of the given HTTP Response
'''
def body(message):
    return message.split('\r\n\r\n',1)[-1]


'''
 function for fetching the home page of the given user after login
 
 @type username: String
 @param username: NEU Id of the user
 
 @type password: String
 @param username: password for the given user
 
 @rtype: String
 @return: Home page of the given user in HTML format after login     
'''
def homePage(username, password):
    message = "\n".join(["GET /accounts/login/?next=/fakebook/ HTTP/1.0","Host:cs5700f14.ccs.neu.edu","\n"])
    recievedMsg = sendToServer(message)
    response = header(recievedMsg)
    cookie['csrftoken'] =  re.search('csrftoken=(.+?);',response).group(1)
    cookie['sessionid'] = re.search('sessionid=(.+?);',response).group(1)
    headmsg = "\n".join(["POST /accounts/login/?next=/fakebook/ HTTP/1.0",
                        "Host:cs5700f14.ccs.neu.edu",
                        "Content-Length:109",
                        "Content-Type:application/x-www-form-urlencoded",
                        "".join(["Cookie:csrftoken=",cookie['csrftoken'],"; sessionid=",cookie['sessionid']]),
                        "\n"])           
    bodymsg = "".join(["username=",username,"&password=",password,"&csrfmiddlewaretoken=",cookie['csrftoken'],"&next=%2Ffakebook%2F"])
    message = "".join([headmsg,bodymsg,"\n"])
    response = sendToServer(message)
    headmsg = header(sendToServer(message))
    if "Forgot password?" in body(response):
        print 'Invalid user name or password'
        os._exit(1)
    cookie['sessionid'] = re.search('sessionid=(.+?);',response).group(1)
    url = re.search('Location:(.+)',headmsg).group(1).strip()
    return fetchPage(url)
    

'''
function for removing the domain/server name from the given url

@type url: String
@param url: url

@rtype: String
@return: url after removing the domain/server name   
'''
def excludedomain(url):
    return re.search('cs5700f14.ccs.neu.edu(.+)',url).group(1).strip()


'''
 function for checking whether the given url is public domain
 (i.e) any url apart from cs5700f14.ccs.neu.edu
 
 @type url: string
 @param url: url
 
 @rtype: Boolean
 @return: True if the given url is not a public domain url. False otherwise
'''
def isNotPublicDomain(url):
    return url.startswith('/') or host in url


'''
 function for forming GETRequest using the given url
 
 @type url: String
 @param url: value for url field of GETRequest
 
 @rtype: String
 @return: GETRequest formed using the given url field
'''
def GETRequest(url):
    url = excludedomain(url)
    message = " ".join(["GET", url, "HTTP/1.0"])
    message = "\n".join([message, 
                         "Host:cs5700f14.ccs.neu.edu",
                         "".join(["Cookie:csrftoken=",cookie['csrftoken'],"; sessionid=",cookie['sessionid']]),
                         "\n"])
    return message


'''
function to form the full url from relative url (i.e) appending domain name.

@type url: String
@param url: relative url

@rtype: String
@return: absolute url (i.e) domain name appended to the given relative url    
'''
def domain(url):
    if not "mailto:choffnes@ccs.neu.edu" in url:
        return "".join(["http://",host,url])
    else: return None


'''
 function to fetch the html content of the given url
 
 @type url: String
 @param url: : url from which the html content has to be fetched
 
 @rtype : String
 @return: html content of the given url 
'''    
def fetchPage(url):
    response = sendToServer(GETRequest(url))
    headmsg = header(response)
    statusCode = headmsg.split("\n",1)[0].split(" ")[1]
    if statusCode == "500" or statusCode == "403" or statusCode == "404":
        return None
    elif statusCode == "301" or statusCode == "302":
        return fetchPage(re.search('Location:(.+)',header).group(1).strip())
    elif statusCode == "200":
        return body(response)
    else:
        print 'Server returned unexpected status code'
        os._exit(1)

'''
 function for fetching the links (i.e) value of href attribute of hyper link tag
 
 @type html: String
 @param html: html content of a page
 
 @rtype: List of String
 @return: list containing all the hyper links extracted form the given html   
'''
def links(html):
    lstOfLinks = []
    soup = BeautifulSoup(html)
    links = soup.find_all('a')    
    for tag in links:
        link = tag.get('href',None)
        if link != None:
            lstOfLinks.append(link)
    return lstOfLinks


'''
 function for extracting the flags from html content
 
 @type html: String
 @param html: html content of the page
 
 @rtype: List of String
 @return: List containing flags extracted from the given html.
          If no flags are there then empty list will be returned  
'''
def flags(html):
    flags = []
    soup = BeautifulSoup(html)
    elements = soup.findAll('h2',{'class':'secret_flag','style':'color:red'})
    if elements:
        for ele in elements:
            flag = ((ele.contents[0]).split(':')[1]).strip()
            print flag
            flags.append(flag)
    return flags


'''
 function for crawling the fakebook(using BFS) and printing the flags.
 It terminate the program once it collects five flags form
 the fakebook
 
 @type nuid: String
 @param nuid: id of the user
 
 @type password: String
 @param password: password of the user
'''
def crawl(nuid,password):
    crawledLinks = set()
    linksToCrawl = []
    html = homePage(nuid,password)
    crawledLinks.add('/fakebook/')
    linksToCrawl.extend(links(html))
    listOfFlags = []
    while True:
        link = linksToCrawl.pop(0)
        if link not in crawledLinks:
            crawledLinks.add(link)
            if isNotPublicDomain(link):
                fullurl = domain(link)
                if fullurl:
                    html = fetchPage(fullurl)
                    if html:
                        listOfFlags.extend(flags(html))
                        if len(listOfFlags) == 5:
                            os._exit(1) 
                        linksToCrawl.extend(links(html))


'''
Entry point of program
'''
if __name__ == "__main__":
    try:
        if not len(sys.argv) == 3:
            print 'Input format is invalid'
        else:
            crawl(sys.argv[1],sys.argv[2])
    except:
        print 'Some unexpected error occurred'