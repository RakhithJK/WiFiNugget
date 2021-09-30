def pack(unpacked_data):
    """
    Compresses image data using a very simple algoritm.
    Returns a list with repeating values converted into
    [value, count] lists, and with a [version, count] header
    in front of all that.
    Version 1 of the algorithm.

    For instance, compressing this bytearray:
    \x00\x00\x00\x01\x03\x0f\x1f
    will return this list:
    [1, 7, [0, 3], 1, 3, 15, 31]
    So, this compression works best for large bytearrays that have a lot of
    repeating pixels - i.e. monochrome display images ;-P

    This function is best run on 'your PC' side. Hasn't been tested on MicroPython yet.
    """
    packed_data = [1, len(unpacked_data)] # compression version and length of data we're compressing
    for value in unpacked_data:
        last_value = packed_data[-1]
        # if we have already packed at least one value (len>2),
        # let's check if the value is the same, if so, we should add to that value
        if len(packed_data) > 2 and value == last_value or (isinstance(last_value, list) and value == last_value[0]):
            if value == last_value:
                # last value is an integer and we need to turn it into a list
                packed_data[-1] = [value, 2]
            else:
                # last value is a list already, just adding 1 to the count
                packed_data[-1][1] += 1
        else:
            # new value, adding it to the list
            packed_data.append(value)
    return packed_data

def unpack(packed_data):
    """
    Decompresses image data using a very simple algorithm described in 'pack'.
    Returns a bytearray.

    This function is to be run on the MicroPython side. Hasn't been tested on MicroPython yet, however.
    """
    i = 0 # index for the unpacked bytearray element that we're currently on
    # checking the compression format version, for future compatibility in case this algo changes significantly
    if packed_data[0] != 1:
        print("Don't know how to decompress this image, format version:", packed_data[0])
        return None
    # pre-creating a bytearray of the length we need, initially filled with zeroes
    # to avoid creating too many useless objects and wasting memory as we unpack
    unpacked_data = bytearray(packed_data[1])
    for element in packed_data[2:]: # need to skip two elements - version and length
        if isinstance(element, int): # just an int, simply putting it into the bytearray
            unpacked_data[i] = element
            i += 1
        else:
            value, count = element
            if value == 0: # small optimization
                # skipping zero-filling since bytearrays are pre-filled with zeroes
                i += count
            else:
                for _ in range(count):
                    unpacked_data[i] = value
                    i += 1
    return unpacked_data

a = bytearray(
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x03\x0f\x1f\x7f\xff\xfe\xf8\xf0\xc0\x80\x00\x00\x00\x00\x80\xc0\xf0\xfc\xfe\xff\x3f\x1f'
    b'\x07\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x03\x0f\x1f\x7f\xff\xfe\xf8\xf0\xc0\x80\x00'
    b'\x00\x00\x00\x80\xc0\xf0\xfc\xfe\xff\x3f\x1f\x07\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x07\x1f\xbf\xff\xfe\xf8\xf8\xfe\xff\x1f\x0f\x07\x01\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x07\x1f\xbf\xff\xfe\xf8\xf8\xfe\xff'
    b'\x1f\x0f\x07\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x80\xe0\xf0\xfc\xfe\x7f\x1f\x0f\x03\x07\x1f\x7f\xff\xfe\xf8\xf0\xc0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\xe0\xf0\xfc\xfe\x7f\x1f\x0f\x03\x07\x1f\x7f\xff\xfe\xf8\xf0'
    b'\xc0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x38\x3c'
    b'\x3f\x3f\x3f\x0f\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x03\x0f\x1f\x3f\x3f\x3e\x3c\x30\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x70\xf8\xf8\xf8\xf8\xf8\xf8\xf8\x70\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x20\x38\x3c\x3f\x3f\x3f\x0f\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x03\x0f\x1f\x3f\x3f\x3e\x3c'
    b'\x30\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18'
    b'\x78\xf0\xc0\x80\x00\x00\x00\x00\x00\x01\x03\xff\x03\x01\x00\x00\x00\x00\x00\x80\xc0\xf0\x78\x18\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x03'
    b'\x07\x06\x0e\x0c\x0c\x0c\x0c\x0f\x0c\x08\x0c\x0c\x06\x06\x03\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

b = bytearray(
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\xe0\xe0'
    b'\x70\x38\x3c\x1c\x1c\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x1c\x1c\x38\x78\xf0\xe0\xc0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\xe0\xf0\x78\x3c\x1c\x0e\x0e\x0e\x07\x07'
    b'\x07\x07\x07\x07\x07\x06\x0e\x0e\x1c\x3c\x38\xf0\xe0\xc0\x80\x00\x00\x00\x00\x00\x00\x00\xf0\xfc\xff\x07\x01\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x20\xf8\xf8\xfc\xfc\xf8\x70\x00\x00\x01\x03\x1f\xfe\xf8\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xfc\xff\x07\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x78'
    b'\xfc\xfc\xfc\xfc\x78\x00\x00\x00\x01\x07\xff\xfe\xf0\x00\x00\x00\x00\x00\x0f\x7f\xff\xe0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x01\x01\x01\x00\x00\x00\x00\x00\xc0\xf0\xff\x3f\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x70\xf8\xf8\xf8\xf8\xf8\xf8\xf8\x70\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x1f\x7f\xf0\xc0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x80\xc0\xf0\xff\x3f\x07\x00\x00\x00\x00\x00\x00\x00\x01\x03\x07\x0f\x1e\x3c\x38\x30\x70\x70\x60\x60\xe0\xe0\xe0\x60'
    b'\x70\x70\x70\x38\x38\x1c\x0e\x0f\x07\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18'
    b'\x78\xf0\xc0\x80\x00\x00\x00\x00\x00\x01\x03\xff\x03\x01\x00\x00\x00\x00\x00\x80\xc0\xf0\x78\x18\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x03\x07\x0f\x1e\x1c\x38\x38\x38\x70\x70\x70\x70\x70\x70\x70\x30\x38\x38\x1c\x1e\x0e\x07'
    b'\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x03'
    b'\x07\x06\x0e\x0c\x0c\x0c\x0c\x0f\x0c\x08\x0c\x0c\x06\x06\x03\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

def test():
    ap = pack(a)
    au = unpack(ap)
    assert(a == au)

    bp = pack(b)
    bu = unpack(bp)
    assert(b == bu)
    print("tests pass")
    print("ap =", ap) # demo of the packed data

test()
