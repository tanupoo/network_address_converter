#!/usr/bin/env python

import re
from ipaddress import ip_network, ip_address

class NetworkAddressConverter:
    def __init__(self, input_str, verbose=False):
        """
        convert input_str into ...
        set it into self.num.
        """
        self.verbose = verbose
        if input_str.find("/") > -1:
            str_num, mask = input_str.split("/")
        else:
            str_num = input_str
            mask = -1
        self.patterns = [
            # an ipv4 PTR
            ( "^([0-9\.]+)\.IN-ADDR\.ARPA\.$", self.cv_from_ip4ptr ),
            # an ipv6 PTR
            ( "^([0-9a-f\.]+)\.IP6\.INT\.$", self.cv_from_ip6ptr ),
            # represented by a bit (01) string separated by [\.:] for each byte.
            ( "^[01]{8}([\.:][01]{8})*$", self.cv_from_bit ),
            # represented by a continuous hex string.
            ( "^0x[0-9a-f]+$", self.cv_from_hex ),
            # represented by less than or equal to 6 hex strings
            # separated by a colon ":" for each byte.
            # including a mac address.
            # must be evaluated before the regex for ipv6 address.
            ( "^[0-9a-f]{2}(:[0-9a-f]{2}){,5}$", self.cv_from_mac ),
            # a decimal string.
            ( "^[0-9]+$", self.cv_from_dec ),
            # represented by a dicimal setring separated by "." for each byte.
            # as same as IPv4 address.
            ( "^[0-9\.]+\.([0-9\.]+)*$", self.cv_from_ip4 ),
            # represented by a hex string separated by a colon ":".
            # including an IPv6 address.
            # must be evaluated after the regex for a mac address form.
            ( "^[0-9a-f:]+$", self.cv_from_ip6 ),
        ]

        # guessing
        for patt,cb in self.patterns:
            r = re.match(patt, str_num, re.IGNORECASE)
            if r is not None:
                self.num = cb(str_num, mask)
                break
        else:
            raise ValueError("unknown form of string.")

    def __str__(self):
        return str(self.num)

    def to_bit8(self, num):
        """
        return a string of an 8-bit form.
        """
        return bin(num)[2:].rjust(8,"0")

    def to_dec(self, pair_size=None, dlm=None):
        """
        convert self.num into a string of a number or a set of decimal numbers.
        return it.
            pair_size  dlm
            =========  ====
            None       Any    a number.
            !None      None   ValueError.
            1          !None  numbers separated by dlm.
            Other      !None  ValueError.
        """
        if pair_size is None:
            return str(int.from_bytes(bytes(self.num), "big"))
        elif dlm is None:
            raise ValueError("dlm is None, but pair_size is specified.")
        elif pair_size == 1:
            return dlm.join([f"{i}" for i in self.num])
        else:
            raise ValueError("pair_size must be 1 or None.")

    def to_hex(self, pair_size=None, dlm=None, capitalize=True):
        """
        convert self.num into a hex string or a set of hex strings.
            pair_size  dlm
            =========  ====
            None       Any    0x + hex strings.
            !None      !None  hex separated by dlm.
            !None      None   ValueError
        """
        if capitalize:
            fmt = lambda i: f"{i:02X}"
        else:
            fmt = lambda i: f"{i:02x}"
        #
        if pair_size is None:
            return "0x{}".format("".join([fmt(i) for i in self.num]))
        elif pair_size is not None and dlm is not None:
            a = []
            for i in range(0,len(self.num),pair_size):
                a.append("".join([fmt(i) for i in self.num[i:i+pair_size]]))
            return dlm.join(a)
        else:
            raise ValueError("dlm is None, but pair_size is specified.")

    def to_bin(self, pair_size=None, dlm=None):
        """
        convert self.num into a bin string or a set of bin strings.
            pair_size  dlm
            =========  ====
            None       Any   continous bit strings. 
            !None      None  ValueError
            !None      !None bit strings separated by dlm.
        """
        if pair_size is None:
            return "".join([self.to_bit8(i) for i in self.num])
        elif dlm is None:
            raise ValueError("dlm is None, but pair_size is specified.")
        else:
            a = []
            for i in range(0,len(self.num),pair_size):
                a.append("".join([self.to_bit8(i)
                                  for i in self.num[i:i+pair_size]]))
            return dlm.join(a)

    def to_rev(self, ipv4=True, capitalize=False):
        if ipv4:
            if capitalize:
                raise ValueError("ERROR: capitalize is True, but for IPv4.")
            return "{}.in-addr.arpa.".format(
                    ".".join([f"{i}" for i in self.num[::-1]]))
        else:
            return "{}.IP6.INT.".format(".".join(
                    [i for i in self.to_hex(capitalize=capitalize)[2:][::-1]]))

    def int_to_x(self, num):
        a = []
        while num > 0:
            a.append(num & 0xff)
            num >>= 8
        return a[::-1]

    def cv_from_ip4ptr(self, str_num, mask):
        if mask != -1:
            raise ValueError("mask is not allowed for this conversion.")
        num = [int(i)
            for i in str_num.replace(".in-addr.arpa.","").split(".")[::-1]]
        if self.verbose:
            print("ip4ptr:", str_num)
            print("num:", num)
        return num

    def cv_from_ip6ptr(self, str_num, mask):
        if mask != -1:
            raise ValueError("mask is not allowed for this conversion.")
        """
        num = self.int_to_x(
                int("".join(str_num.replace(".IP6.INT.","").split(".")[::-1]),16)
                )
        """
        a = str_num.replace(".IP6.INT.","").split(".")[::-1]
        num = [int("".join(a[i:i+2]),16) for i in range(0,len(a),2)]
        if self.verbose:
            print("ip6ptr:", str_num)
            print("num:", num)
        return num

    def cv_from_bit(self, str_num, mask):
        if mask != -1:
            raise ValueError("mask is not allowed for this conversion.")
        num = [int(i, 2) for i in re.sub("[\.: ]", " ", str_num).split()]
        if self.verbose:
            print("bit:", str_num)
            print("num:", num)
        return num

    def cv_from_hex(self, str_num, mask):
        if mask != -1:
            raise ValueError("mask is not allowed for this conversion.")
        num = self.int_to_x(int(str_num, 16))
        if self.verbose:
            print("hex:", str_num)
            print("num:", num)
        return num

    def cv_from_mac(self, str_num, mask):
        if mask != -1:
            raise ValueError("mask is not allowed for this conversion.")
        num = [int(i,16) for i in str_num.split(":")]
        if self.verbose:
            print("mac:", str_num)
            print("num:", num)
        return num

    def cv_from_dec(self, str_num, mask):
        if mask != -1:
            raise ValueError("mask is not allowed for this conversion.")
        num = self.int_to_x(int(str_num))
        if self.verbose:
            print("dec:", str_num)
            print("num:", num)
        return num

    def cv_from_ip4(self, str_num, mask):
        if mask != -1:
            a = ip_network(f"{str_num}/{mask}", strict=False)
            num = [ i for i in a.network_address.packed ]
        else:
            a = ip_address(f"{str_num}")
            num = [ i for i in a.packed ]
            #num = [int(i) for i in str_num.split(".")]
        if self.verbose:
            print("ip4:", str_num)
            print("num:", num)
        return num

    def cv_from_ip6(self, str_num, mask):
        if mask != -1:
            a = ip_network(f"{str_num}/{mask}", strict=False)
            num = [ i for i in a.network_address.packed ]
        else:
            a = ip_address(f"{str_num}")
            num = [ i for i in a.packed ]
            #num = self.int_to_x(int("".join(str_num.split(":")), 16))
        if self.verbose:
            print("ip6:", str_num)
            print("num:", num)
        return num

