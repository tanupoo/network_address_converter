from network_address_converter import NetworkAddressConverter

nc = NetworkAddressConverter("2001:0db8:85a3::8a2e:0370:7334")
assert str(nc) == "[32, 1, 13, 184, 133, 163, 0, 0, 0, 0, 138, 46, 3, 112, 115, 52]"
assert nc.to_dec() == "42540766452641154071740215577757643572"
assert nc.to_dec(pair_size=1, dlm=".") == "32.1.13.184.133.163.0.0.0.0.138.46.3.112.115.52"
assert nc.to_hex() == "0x20010DB885A3000000008A2E03707334"
assert nc.to_hex(dlm="") == "0x20010DB885A3000000008A2E03707334"
assert nc.to_hex(pair_size=1, dlm=" ") == "20 01 0D B8 85 A3 00 00 00 00 8A 2E 03 70 73 34"
assert nc.to_hex(pair_size=2, dlm=":") == "2001:0DB8:85A3:0000:0000:8A2E:0370:7334"
assert nc.to_hex(pair_size=2, dlm=":", capitalize=False) == "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
assert nc.to_bin() == "00100000000000010000110110111000100001011010001100000000000000000000000000000000100010100010111000000011011100000111001100110100"
assert nc.to_bin(pair_size=1, dlm=".") == "00100000.00000001.00001101.10111000.10000101.10100011.00000000.00000000.00000000.00000000.10001010.00101110.00000011.01110000.01110011.00110100"
assert nc.to_rev(ipv4=True) == "52.115.112.3.46.138.0.0.0.0.163.133.184.13.1.32.in-addr.arpa."
assert nc.to_rev(ipv4=False) == "4.3.3.7.0.7.3.0.e.2.a.8.0.0.0.0.0.0.0.0.3.a.5.8.8.b.d.0.1.0.0.2.IP6.INT."

test_vector = [
"""
= 2001:0db8:85a3::8a2e:0370:7334
4 32.1.13.184.133.163.0.0.0.0.138.46.3.112.115.52
6 2001:0db8:85a3:0000:0000:8a2e:0370:7334
m 20:01:0d:b8:85:a3:00:00:00:00:8a:2e:03:70:73:34
b 00100000.00000001.00001101.10111000.10000101.10100011.00000000.00000000.00000000.00000000.10001010.00101110.00000011.01110000.01110011.00110100
x 20 01 0d b8 85 a3 00 00 00 00 8a 2e 03 70 73 34
X 0x20010db885a3000000008a2e03707334
d 42540766452641154071740215577757643572
r 52.115.112.3.46.138.0.0.0.0.163.133.184.13.1.32.in-addr.arpa.
R 4.3.3.7.0.7.3.0.e.2.a.8.0.0.0.0.0.0.0.0.3.a.5.8.8.b.d.0.1.0.0.2.IP6.INT.
"""
,
"""
= 192.168.0.25
4 192.168.0.25
6 c0a8:0019
m c0:a8:00:19
b 11000000.10101000.00000000.00011001
x c0 a8 00 19
X 0xc0a80019
d 3232235545
r 25.0.168.192.in-addr.arpa.
R 9.1.0.0.8.a.0.c.IP6.INT.
"""
,
"""
= 12:34:56:78:9a:bc
4 18.52.86.120.154.188
6 1234:5678:9abc
m 12:34:56:78:9a:bc
b 00010010.00110100.01010110.01111000.10011010.10111100
x 12 34 56 78 9a bc
X 0x123456789abc
d 20015998343868
r 188.154.120.86.52.18.in-addr.arpa.
R c.b.a.9.8.7.6.5.4.3.2.1.IP6.INT.
"""
,
"""
= 192.168.153.243/26
4 192.168.153.192
6 c0a8:99c0
m c0:a8:99:c0
b 11000000.10101000.10011001.11000000
x c0 a8 99 c0
X 0xc0a899c0
d 3232274880
r 192.153.168.192.in-addr.arpa.
R 0.c.9.9.8.a.0.c.IP6.INT.
"""
]

for tv_src in test_vector:
    """
    = 2001:0db8:85a3::8a2e:0370:7334
    4 32.1.13.184.133.163.138.46.3.112.115.52 
    6 2001:0db8:85a3:0000:0000:8a2e:0370:7334
    m 20:01:0d:b8:85:a3:00:00:00:00:8a:2e:03:70:73:34
    b 00100000.00000001.00001101.10111000.10000101.10100011.00000000.00000000.00000000.00000000.10001010.00101110.00000011.01110000.01110011.00110100
    x 20 01 0d b8 85 a3 00 00 00 00 8a 2e 03 70 73 34
    X 0x20010db885a3000000008a2e03707334
    d 42540766452641154071740215577757643572
    r 52.115.112.3.46.138.0.0.0.0.163.133.184.13.1.32.in-addr.arpa.
    R 4.3.3.7.0.7.3.0.e.2.a.8.0.0.0.0.0.0.0.0.3.a.5.8.8.b.d.0.1.0.0.2.IP6.INT.
    """
    tv = [kt.split(" ",1) for kt in tv_src.splitlines()[1:]]
    key0,in_str = tv[0]
    if key0 != "=":
        print("IGNORE:", tv)
        continue
    try:
        nc = NetworkAddressConverter(in_str)
        print(nc)
    except ValueError as e:
        print(e)
        continue
    #
    print("input: {} {}".format(key0, in_str))
    for k,answer in tv[1:]:
        ret = None
        if k == "4":
            ret = nc.to_dec(pair_size=1, dlm=".")
        elif k == "6":
            ret = nc.to_hex(pair_size=2, dlm=":", capitalize=False)
        elif k == "m":
            ret = nc.to_hex(pair_size=1, dlm=":", capitalize=False)
        elif k == "b":
            ret = nc.to_bin(pair_size=1, dlm=".")
        elif k == "x":
            ret = nc.to_hex(pair_size=1, dlm=" ", capitalize=False)
        elif k == "X":
            ret = nc.to_hex(capitalize=False)
        elif k == "d":
            ret = nc.to_dec()
        elif k == "r":
            ret = nc.to_rev(ipv4=True)
        elif k == "R":
            ret = nc.to_rev(ipv4=False)
        #
        print(f"{answer == ret}\t{answer} vs {ret}")
        if answer != ret:
            raise ValueError


