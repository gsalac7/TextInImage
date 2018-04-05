from PIL import Image
import sys

# check the image format to see if JPEG
def is_JPEG(Image):
    if Image.format == 'JPEG':
        return True
    return False

# pad the binary value until it is 8 bits
def pad_binary(binary):
    while len(binary) < 8:
        binary = '0' + binary
    return binary

# read from the file and open the picture
def setup(file, picture):
    pic = Image.open(picture)
    if is_JPEG(picture) == False:
        print('File is not JPEG')
        print('Converting to JPEG...')
        # change to JPEG
        pic.save('testImage.jpg', 'JPEG')
    pic = Image.open('testImage.jpg')
    f = open(file, 'r')
    source_code = f.read()
    f.close()
    return source_code, pic

# get the binary values of the string
def str_to_bin(string):
    binaries = ' '.join(format(ord(x), 'b') for x in string)
    binaries = binaries.split()
    for i in range(len(binaries)):
        binaries[i] = pad_binary(binaries[i])
    binaries = ' '.join(binaries)
    return list(binaries)

# get the integer as a binary string
def int_to_bin(integer):
    return str(bin(integer))[2:]

# takes binary as a string of 1's and 0's and returns it as an int to
# encode into the picture
def bin_to_int(binary):
    return int(str(binary), 2)

# change the least significant bit
def input_value(rgb_bin, input_value):
    rgb_bin = list(rgb_bin)
    if input_value == '':
        rgb_bin.pop()
    else:
        rgb_bin[-1] = input_value # right most bit will be the input value
    return ''.join(rgb_bin) # return as a string

def rgb_bin_values(r,g,b):
    return int_to_bin(r), int_to_bin(g), int_to_bin(b)

def encode(code, pic, image):
    msg_len = len(code)
    print 'Size of the Messsage being encoded is: ' + str(msg_len)
    width, height = pic.size

    msg_len_bin = int_to_bin(msg_len)
    # pad the length of the message
    while len(msg_len_bin) < 33:
        msg_len_bin = '0' + msg_len_bin
    msg_len_bin = list(msg_len_bin)

    # use the first 11 pixels to contain the length of the message
    for x in range(width - 1, width - 12, -1):
        r,g,b = pic.getpixel((x, height - 1))

        r_bin, g_bin, b_bin = rgb_bin_values(r,g,b)

        if len(msg_len_bin) != 0:
            r_bin = input_value(r_bin, msg_len_bin.pop(0))
        if len(msg_len_bin) != 0:
            g_bin = input_value(g_bin, msg_len_bin.pop(0))
        if len(msg_len_bin) != 0:
            b_bin = input_value(b_bin, msg_len_bin.pop(0))

        r = bin_to_int(r_bin)
        g = bin_to_int(g_bin)
        b = bin_to_int(b_bin)

        pic.putpixel((x, height - 1), (r, g, b))
    pic.save(image)

    pic = Image.open(image)
    # code is now a string as binary
    code = str_to_bin(code)
    #print ''.join(code)
    index = 0
    # traverse the pixels starting from the bottom right
    while len(code) != 0:
        for y in range(height - 1, 0, -1):
            for x in range(width - 12, 0, -1):
                # get the rgb pixels as integers
                r, g, b = pic.getpixel((x,y))
                # get the rgb binary values
                r_bin, g_bin, b_bin = rgb_bin_values(r,g,b)

                r_bin = pad_binary(r_bin)
                g_bin = pad_binary(g_bin)
                b_bin = pad_binary(b_bin)

                if len(code) != 0:
                    value = code.pop(0)
                    if value == ' ': # if a space, pop the value again
                        value = code.pop(0)
                    r_bin = input_value(r_bin, value)
                if len(code) != 0:
                    value = code.pop(0)
                    if value == ' ':
                        value = code.pop(0)
                    g_bin = input_value(g_bin, value)
                if len(code) != 0:
                    value = code.pop(0)
                    if value == ' ':
                        value = code.pop(0)
                    b_bin = input_value(b_bin, value)

                r = bin_to_int(r_bin)
                g = bin_to_int(g_bin)
                b = bin_to_int(b_bin)

                pic.putpixel((x, y), (r, g, b))
    pic.save(image)
    print 'Successfully encoded message'

def decode(pic):
    # from bottom right, get the length,
    # then get the thing
    width, height = pic.size
    size = ''
    for x in range(width - 1, width - 12, -1):
        r, g, b = pic.getpixel((x, height - 1))

        r_bin, g_bin, b_bin = rgb_bin_values(r,g,b)

        r_value = r_bin[-1]
        g_value = g_bin[-1]
        b_value = b_bin[-1]

        size += r_value + g_value + b_value
    size = bin_to_int(size)
    print 'The Length of the decoded message is: ' + str(size)

    print 'Decoding message...'
    string_bin = ''
    for y in range(height - 1, 0, -1):
        for x in range(width - 12, 0, -1):
            # get the rgb pixels
            r,g,b = pic.getpixel((x,y))

            r_bin, g_bin, b_bin = rgb_bin_values(r,g,b)

            # get the string
            string_bin += r_bin[-1] + g_bin[-1] + b_bin[-1]

    # divide the string into groups of 8 bits
    string_bin = [string_bin[i: i+8] for i in range(0, len(string_bin), 8)]
    output = ''
    # Only go up to the length of the message
    for i in range(size):
        output += chr(int(string_bin[i], 2))

    print 'Successfully decoded message!'
    print output

def main():
    # get the mode either encoding or decoding
    mode = sys.argv[1]

    if mode == 'encode':
        text_file = sys.argv[2]
        image = sys.argv[3]
        put_image = sys.argv[4]

        message, image = setup(text_file, image)
        encode(message, image, put_image)
    elif mode == 'decode':
        image = sys.argv[2]
        pic = Image.open(image)
        decode(pic)

if __name__ == '__main__':
    main()
