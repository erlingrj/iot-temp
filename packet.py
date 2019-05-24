import datetime



def encode_msg(data):
    # Implement a way to encode the different messages
    t = datetime.datetime.now()
    # Make payload bytestring with timestamp
    payload = b'Timestamp=%d-%d-%d-%d-%d-%d;Data=%f' %(t.day, t.month, t.year, t.hour, t.minute, t.second, data)

    return payload

def decode_msg(payload):
    # Decode different packets
    return dict(item.split('=') for item in payload.split(';'))
