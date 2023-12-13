import struct
from io import BytesIO

HEADER_SIZE = 9744  # for both Esum and List data, in bytes
EVENT_SIZE = 8  # Size of each esum or list event in bytes
nsPerBin = 5 * 2**16 / 2**24  # nano second per bin

# Define Esum event
class Event:
    def __init__(self, t=0, frame=0, mode=0, x=0, z=0, e=0, ring=0):
        self.raw = (
            (t << 40)                 # timestamp:  24 bit
            | ((frame & 0x0F) << 36)  # frame number: 4 bit
            | ((mode & 0x0F) << 32)   # data type: 4 bit 
            | ((x & 0x03FF) << 22)    # x (tangential) address: 10 bit
            | ((z & 0x003F) << 16)    # z (axial) address: 6 bit
            | ((e & 0x1FFF) << 3)     # energy: 13 bit
            | (ring & 0x07)           # ring number: 3 bit
        )

    def t(self):
        return (self.raw >> 40) & 0xFFFFFF

    def frame(self):
        return (self.raw >> 36) & 0x0F

    def mode(self):
        return (self.raw >> 32) & 0x0F

    def x(self):
        return (self.raw >> 22) & 0x03FF

    def z(self):
        return (self.raw >> 16) & 0x003F

    def e(self):
        return (self.raw >> 3) & 0x1FFF

    def ring(self):
        return self.raw & 0x07

    def isData(self):  # mode = 2
        return (self.raw & 0x0000000F00000000) == 0x0000000200000000

    def isFrameStart(self):  # mode = 15
        return (self.raw & 0x0000000F00000000) == 0x0000000F00000000

    def isFrameEnd(self):  # mode = 14
        return (self.raw & 0x0000000F00000000) == 0x0000000E00000000

    def decode(self, data):
        self.raw = struct.unpack('<Q', data)[0]
    
    def encode(self):
        return struct.pack('<Q', self.raw)

    @classmethod
    def decode_multiple(cls, data):  # return both decoded events and the number of events decoded
        events = []
        buffer = BytesIO(data)
        num_events_read = 0  # Initialize the counter
        while True:
            event_data = buffer.read(EVENT_SIZE)
            if not event_data:
                break
            event = cls()
            event.decode(event_data)
            events.append(event)
            num_events_read += 1  # Increment the counter for each event
        return events, num_events_read

    @classmethod
    def encode_multiple(cls, events):
        buffer = BytesIO()
        for event in events:
            buffer.write(event.encode())
        return buffer.getvalue()
