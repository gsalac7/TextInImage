from PIL import Image
import sys
import binascii

# check the image format to see if JPEG
def is_JPEG(Image):
  if Image.format == 'JPEG':
    return True
  return False

# read from the file and open the picture
def setup(file, picture):
  pic = Image.open(picture)
  # convert to jpeg if not already
  if is_JPEG(pic) == False:
    picture = picture.split('.')
    print('File is not JPEG')
    print('Converting to JPEG...')
    # change to JPEG'
    pic_string = picture[0] + '.jpg'
    rgb_im = pic.convert('RGB')
    rgb_im.save(pic_string, 'JPEG')
    pic = Image.open(pic_string)
  f = open(file, 'r')
  source_code = f.read()
  f.close()
  return source_code, pic

# Helper functions to turn the string to binary
# pad the binary value until it is 8 bits
def pad_binary(binary):
  while len(binary) < 8:
    binary = '0' + binary
  return binary

# get the binary values of the string and pad until
# they are 8 bits. Return the string as a list of 8 
# bits
def str_to_bin(string):
  binaries = ' '.join(format(ord(x), 'b') for x in string)
  binaries = binaries.split()
  for i in range(len(binaries)):
    binaries[i] = pad_binary(binaries[i])
  binaries = ''.join(binaries)
  return list(binaries)

# Turn an integer to binary
def int_to_bin(integer):
  return bin(integer)[2:]

# turn binary back into an int
def bin_to_int(binary):
  return int(binary, 2)

# Function to put the actual data into the least significant bit
def input_value(rgb_bin, value):
  rgb_bin = list(rgb_bin)
  rgb_bin[-1] = value
  return rgb_bin

# The function to embed the length and the text
def embed(code, source_pic, output_pic):
  # get the number of bits
  msg_len = len(code) * 8
  print('The Length of the message is:', msg_len, 'bits')
  # get the width and height of the picture
  width, height = source_pic.size

  # convert the msg_len to binary format
  msg_len = int_to_bin(msg_len)
  msg_len = str(msg_len)
  
  # pad it to 32 bits
  while len(msg_len) < 32:
    msg_len = '0' + msg_len

  # input the length of the bits in the first 11 pixels starting
  # from the bottom right 
  msg_len = list(msg_len)
  for i in range(width - 1, width - 12, -1):
    if len(msg_len) == 0:
      break
    r,g,b = source_pic.getpixel((i, height-1))
    # Get the RGB values in binary
    r_bin = int_to_bin(r)
    g_bin = int_to_bin(g)
    b_bin = int_to_bin(b)
    
    # as long as there is still something to pop,
    # keep embedding the length
    if len(msg_len) != 0:
      r_bin = input_value(r_bin, msg_len.pop(0))
    if len(msg_len) != 0:
      g_bin = input_value(g_bin, msg_len.pop(0))
    if len(msg_len) != 0:
      b_bin = input_value(b_bin, msg_len.pop(0))   

    # convert the modified binaries into an integer
    r = bin_to_int(''.join(r_bin))
    g = bin_to_int(''.join(g_bin))
    b = bin_to_int(''.join(b_bin))

    # put the pixels in the proper spots
    source_pic.putpixel((i, height - 1), (r,g,b))

  # Starting from the bottom right, start getting the r,g,b values
  # of the pixels
  code = str_to_bin(code)
  code = list(code)
  finished = False
  for x in range(width - 12, -1, -1):
    # if the length of the code is finished, then stop the loop
    r,g,b = source_pic.getpixel((x, height - 1))

    # get the r,g,b values
    r_bin = int_to_bin(r)
    g_bin = int_to_bin(g)
    b_bin = int_to_bin(b)

    # modify the binary as long as there is still something to modify
    if len(code) != 0: 
      r_bin = input_value(r_bin, code.pop(0))
    else:
      finished = True
      break
    if len(code) != 0:
      g_bin = input_value(g_bin, code.pop(0))
    else:
      finished = True
      break
    if len(code) != 0:  
      b_bin = input_value(b_bin, code.pop(0))
    else:
      finished = True
      break

    # convert back to ints
    r = bin_to_int(''.join(r_bin))
    g = bin_to_int(''.join(g_bin))
    b = bin_to_int(''.join(b_bin))

    source_pic.putpixel((x,height - 1),(r,g,b))

  # Traverse the pixels starting from the bottom right
  if finished == False:
    for y in range(height - 2, -1, -1):
      for x in range(width - 1, -1, -1):
        # if the length of the code is finished, then stop the loop
        r,g,b = source_pic.getpixel((x,y))

        # get the r,g,b values
        r_bin = int_to_bin(r)
        g_bin = int_to_bin(g)
        b_bin = int_to_bin(b)

        # modify the binary as long as there is still something to modify
        if len(code) != 0: 
          r_bin = input_value(r_bin, code.pop(0))
        else:
          finished = True
          break
        if len(code) != 0:
          g_bin = input_value(g_bin, code.pop(0))
        else:
          finished = True
          break
        if len(code) != 0:  
          b_bin = input_value(b_bin, code.pop(0))
        else:
          finished = True
          break
        # convert back to ints
        r = bin_to_int(''.join(r_bin))
        g = bin_to_int(''.join(g_bin))
        b = bin_to_int(''.join(b_bin))

        source_pic.putpixel((x,y),(r,g,b)) 
      if finished == True:
        break

  source_pic.save(output_pic)
  print('Successfully embedded the text')  

# function to decode the text from the picture
def decode(embedded_picture):
  msg_len = ''
  width, height = embedded_picture.size
  
  # Get the size of the message
  for x in range(width - 1,  width - 12, -1):
    r,g,b = embedded_picture.getpixel((x, height - 1))
    
    r_bin = int_to_bin(r)
    g_bin = int_to_bin(g)
    b_bin = int_to_bin(b)

    msg_len += r_bin[-1]
    msg_len += g_bin[-1] 
    # only get the last bit if the msg_len is not 32 bits
    if len(msg_len) != 32:
      msg_len += b_bin[-1]
  msg_len = bin_to_int(msg_len)
  print('Length of the decoded message is:', msg_len, 'bits')
  
  # now get the actual data
  source_code = ''
  finished = False
  for x in range(width - 12, -1, -1):
    r,g,b = embedded_picture.getpixel((x, height - 1))
    r_bin = int_to_bin(r)
    g_bin = int_to_bin(g)
    b_bin = int_to_bin(b)

    # keep iterating as long as there we are less than the msg_len
    if len(source_code) != msg_len:
      source_code += r_bin[-1]
    else:
      finished = True
      break
    if len(source_code) != msg_len:  
      source_code += g_bin[-1]
    else:
      finished = True
      break
    if len(source_code) != msg_len:
      source_code += b_bin[-1]
    else:
      finished = True
      break

  if finished == False:
    # traverse through the pixels starting after the 11th pixel
    for y in range(height - 2, -1, -1):
      for x in range(width - 1, -1, -1):
        r,g,b = embedded_picture.getpixel((x, y))
        r_bin = int_to_bin(r)
        g_bin = int_to_bin(g)
        b_bin = int_to_bin(b)

        # keep iterating as long as there we are less than the msg_len
        # get the last bit and append it to the source_code
        if len(source_code) != msg_len:
          source_code += r_bin[-1]
        else:
          finished = True
          break
        if len(source_code) != msg_len:  
          source_code += g_bin[-1]
        else:
          finished = True
          break
        if len(source_code) != msg_len:
          source_code += b_bin[-1]
        else:
          finished = True
          break
      if finished == True:
        break
  
  # turn the source_code into a list of 8 bits per element
  source_code = [source_code[i: i+8] for i in range(0, len(source_code), 8)]

  code = ''
  # just convert the source_code binaries to characters and print
  for char in source_code:
    char_int = bin_to_int(char)
    code += chr(char_int)
  print('Successfully Decoded Message:')
  print(code)

def main():
  mode = sys.argv[1]

  if mode == 'encode':
    text_file = sys.argv[2]
    image = sys.argv[3]
    put_image = sys.argv[4]

    message, image = setup(text_file, image)
    embed(message, image, put_image)
  elif mode == 'decode':
    image = sys.argv[2]
    pic = Image.open(image)
    decode(pic)
  
if __name__=='__main__':
  main()