import struct
f= open('Capture.PNG','rb')
data=f.read(30)
valid_png_header = b'\x89PNG\r\n\x1a\n'
if data[:8] == valid_png_header:
    width, height = struct.unpack('>LL', data[16:24])
    print('Valid PNG, width', width, 'height', height)
else:
    print('Not a valid PNG')    