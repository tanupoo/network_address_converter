Network Address Converter
=========================

## Example

```
% ./nac 2001:0db8:85a3::8a2e:0370:7334 
20 01 0d b8 85 a3 00 00 00 00 8a 2e 03 70 73 34

% ./nac 2001:0db8:85a3::8a2e:0370:7334 -6
2001:0db8:85a3:0000:0000:8a2e:0370:7334

% ./nac 192.168.10.131 -bx
11000000.10101000.00001010.10000011
c0 a8 0a 83

% ./nac c0 a8 0a 83 -4
192.168.10.131

% ./nac 192.168.10.131/26 -4b
192.168.10.128
11000000.10101000.00001010.10000000
```

## Usage

```
usage: nac [-h] [-4] [-6] [-m] [-b] [-x] [-X] [-d] [-r] [-R] [-c]
           [-e PAIR_SIZE] [-D DLM] [-f FROM_TYPE] [-v]
           number [number ...]

converter of a network address like string.

positional arguments:
  number        any number-like string. you can use mask.

optional arguments:
  -h, --help    show this help message and exit
  -4            convert into IPv4 address. alias to option -d -e1 -D.
                (default: False)
  -6            convert into IPv6 address. alias to option -x -e2 -D:
                (default: False)
  -m            convert into hex string separated by ':' for each byte. alias
                to -x -e1 -D: (default: False)
  -b            convert into a bit string for each byte. with -e1 -D. as
                default (default: False)
  -x            convert into a hex string. with -e1 -D' ' as default (default:
                False)
  -X            convert into a continous hex string followed by '0x'.
                (default: False)
  -d            convert into decimal. (default: False)
  -r            convert into a string for IPv4 reverse lookup. (default:
                False)
  -R            convert into a string for IPv6 reverse lookup. (default:
                False)
  -c            specify to capitalize the output. (default: False)
  -e PAIR_SIZE  specify the number of pair of bytes. (default: None)
  -D DLM        specify delimiter. (default: None)
  -f FROM_TYPE  specify the type of the input string. by default, it will
                guess what. valid key is either: b,x,d,r (default: None)
  -v            enable verbose mode. (default: False)
```
