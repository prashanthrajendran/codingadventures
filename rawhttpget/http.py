import os


'''
function to form the get request

@param path : path that has to be packages in get request
@param hostname : server name to which the get request has to be sent
'''
def request(path, hostname):
    if path == "" or not path:
        path="/"
    return "\n".join(["GET "+path+" HTTP/1.0",
                      "Host:"+hostname,
                      "\n"])

'''
  function to check whether the response got from server is 200 OK

  @param resposne : HTTP response form the server
  @returns : true if the response is 200 OK, false otherwise.
'''
def isvalidresponse(response):
    headmsg = header(response)
    statusCode = headmsg.split("\n",1)[0].split(" ")[1]
    return (statusCode == "200")

'''
  function to extract the body form the http response
  @param message : HTTP response from the server
  @returns : body form th HTTP response. If the status code of the
             header is something other than 200 ok then program will
             terminate
'''
def body(message):
    if isvalidresponse(message):
        return message.split('\r\n\r\n',1)[-1]
    else:
        print "A status code other than 200 OK has been received"
        os._exit(1)

'''
  function to extract the header form the http response
  @param message : HTTP response form the server
  @returns : Header form the given HTTP response
'''
def header(message):
    return message.split('\r\n\r\n',1)[0]
