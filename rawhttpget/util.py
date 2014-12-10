
'''
 function to check whether syn flag is set
 @param flag : flag in the tcp packet
 @returns : true if the syn flag is set, false otherwise.
'''
def is_syn(flag):
    return is_set(flag, 1)

'''
 function to check whether ack flag is set
 @param flag : flag in the tcp packet
 @returns : true if the ack flag is set, false otherwise.
'''
def is_ack(flag):
    return is_set(flag, 4)

'''
 function to check whether fin flag is set
 @param flag : flag in the tcp packet
 @returns : true if the fin flag is set, false otherwise.
'''
def is_fin(flag):
    return is_set(flag, 0)

'''
  function to check whether a particular bit is set in  number
  @param val : number for which a bit has been set has to be determined
  @param bit : indicates which bit has to be checked whether it is set or not

  @returns : if the given bit is set in val, false otherwise
'''
def is_set(val, bit):
    return (val & (1 << bit) == (1 << bit))


'''
 function to calculate the checksum (ip checksum)
 @params : data for which the check sum has to be calculated
 @returns : check sum for the given data
'''
def checksum(data):
  length = len(data)
  if (length & 1):
    length -= 1
    total = ord(data[length])
  else:
    total = 0
  while length > 0:
    length -= 2
    total += (ord(data[length + 1]) << 8) + ord(data[length])

  total = (total >> 16) + (total & 0xffff)
  total += (total >> 16)
  return total

