import datetime



def encode_msg(data):
    # Implement a way to encode the different messages
    t = datetime.datetime.now()
    # Make payload bytestring with timestamp
    payload = b'%d:%d:%d:%d:%d:%d:%f' %(t.day, t.month, t.year, t.hour, t.minute, t.second, data)

    return payload
    

def decode_msg(payload):
    # Decode different packets
    day, month, year, hour, minute, sec, data = payload.split(':')
    return {'data' : data, 'day' : day, 'month' : month, 'year' : year, 'hour' : hour, 'min' : minute, 'sec' : sec}
