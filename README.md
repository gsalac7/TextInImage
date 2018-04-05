# Text In Image

## Author: Gabe Salac

### Description:
This program is going to embed a secret message into the pixels of an image. It will take a JPEG image and output the secret text into a PNG image.

### Architecture:

Written in Python using Pillow Library

- encode() takes the text, input image, and output image and encodes the text into the output image. The message length is taken and encoded into the first 11 pixels. Every binary value of the message characters are extracted and padded with 0's until it is 8 bits long. Then it is embedded into the least significant bit of each RGB value.

- decode() takes an image and decodes the message. The message length is taken from the first 11 pixels. The binary values of the message are taken as one long continuous string, and then divided into a list of 8 bits each. The 8 bits are then translated into its binary ASCII value and printed out.


### To Execute:

Encoding:
```
 python TextInImage.py encode <message-text-file> <image-to-encode> <output-image-with-filetype>
```
example:
```
 python TextInImage.py encode source.txt testImage.jpg outputImage.png
```
Decoding:
```
 python TextInImage.py decode <secret-image>
```
example:
```
python TextInImage.py decode outputImage.png
```
