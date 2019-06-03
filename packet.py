import datetime



def encode_msg(data, src):
    # Implement a way to encode the different messages
    t = datetime.datetime.now()
    t = t.replace(microsecond=0)
    # Make payload bytestring with timestamp
    payload = 'Timestamp={};Data={};Src={}'.format(t.isoformat(), data, src)
    # Encode as bytestring
    return payload.encode('utf-8')

def decode_msg(payload):
    # Decode different packets
    return dict(item.split('=') for item in payload.split(';'))
