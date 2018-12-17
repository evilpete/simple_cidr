#!/usr/bin/env python

import socket
import struct

# Peter Shipley
# peter.shipley@gmail.com
# Sun Dec 16 20:11:53 PST 2018


ip_debug = 0


#
# Simple CIDR
#
# Small and fast IPv4 network address tool
#
# 75% faster then netaddr,
#
# for cases where netaddr is too slow and you do not need the kitchen sink
#
# to use,
#   from simple_cidr import *
# -or-
#   just copy the functions you need into your code...
#

def ip2int(addr):
    # takes asciiip addr and  returns a 32bit int
    if isinstance(addr, int):
        return addr
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def int2ip(addr):
    # takes 32bit int and returns a formated IP addr
    return socket.inet_ntoa(struct.pack("!I", addr))

def cidr2int(cdr):
    # takes a cidr in addr/bit formate and returns a cidr tuple
    # eg : cidr2int('10.1.10.1/24')
    if ip_debug:
        print "\ncidr2int", cdr
    a = cdr.split('/')
    r = ipmask2int(a[0], a[1])
    return r

def ipmask2int(ip, mk):
    # takes a ip_addr string and network bit and returns a cidr tuple
    # eg:  ipmask2int('10.1.10.1', 24)
    _ip = ip2int(ip)
    _mk = 32 - int(mk)
    m = (0xFFFFFFFF << _mk) & 0xFFFFFFFF
    r = _ip & m
    if ip_debug:
        print "\nipmask2int", ip, mk
        print 'net\t{0:032b} {0} {1}'.format(_ip, ip)
        print 'mk\t{0:032b} {0} {1} {2}'.format(m, _mk, mk)
        print 'r \t{0:032b} {0}'.format(r)
    adr = int2ip(r)
    return (r, m, adr + '/' + mk)

def cidr3netmask(cidr):
    return int2ip(cidr[1])

def ip_in_cidr(ip, cidr):
    # takes a ip address and cidr tuple and returns true if IP is in cidr block
    if ip_debug:
        print "\nip_in_cidr", ip, cidr
    if isinstance(ip, basestring):
        _ip = ip2int(ip)
    else:
        _ip = ip
    if isinstance(cidr, basestring):
        _cidr = cidr2int(cidr)
    else:
        _cidr = cidr

    if ip_debug:
        print 'ip\t{0:032b} {0} {1}'.format(_ip, ip)
        print 'mk\t{0:032b} {0} {1} {2}'.format(_cidr[1], _cidr[1], cidr)
        print 'net\t{0:032b} {0} {1} {2}'.format(_cidr[0], _cidr[0], cidr)
        # print 'ip {} in {} : {}'.format(ip, cidr, r)

    return _ip_in_cidr(_ip, _cidr)

def _ip_in_cidr(i_ip, i_cidr):
    # ipm = _ip & _cidr[1]
    r = i_cidr[0] == (i_ip & i_cidr[1])
    return r

def ip_in_cidr_list(ip, cidr_list):
    # return Ture if int_ip addr in in array of cidr tuples
    for _cidr in cidr_list:
        if _cidr[0] == (ip & _cidr[1]):
            return True
    return False


#print(int2ip(0xc0a80164)) # 192.168.1.100

def subnet_cidr(b_cidr, bits):
    # take a cidr tuple and a int for subnet size
    # yields a list or subblocks
    i_bits = 32 - int(bits)
    netblk_sz = (0x00000001 << i_bits) & 0xFFFFFFFF
    subnet_i = b_cidr[0]
    while b_cidr[0] == (subnet_i & b_cidr[1]):
        yield "{}/{}".format(int2ip(subnet_i), bits)
        subnet_i += netblk_sz

if __name__ == '__main__':

    print "ip2int :"
    addr1 = '172.21.8.4'
    addr1_i = ip2int(addr1)
    addr1_is = int2ip(addr1_i)
    print "\taddr1\t{0} == {1} == {2:032b} {2:d}".format(addr1, addr1_is, addr1_i)
    if addr1 == addr1_is:
        print "\tPass"
    else:
        print "\tFail"

    # mynetI  = ip2int(mynet)
    # print "mynet\t{0:032b} {0:d} {1}".format(mynetI, int2ip(mynetI))

    addr2 = '172.21.9.19'
    addr2_i = ip2int(addr2)
    addr2_is = int2ip(addr2_i)
    print "\taddr2\t{0} == {1} == {2:032b} {2:d}".format(addr2, addr2_is, addr2_i)
    if addr2 == addr2_is:
        print "\tPass"
    else:
        print "\tFail"

    print "\n"

    print "cidr2int :"
    cidr1 = '172.21.9.0/23'
    cidr1_i = cidr2int(cidr1)
    cidr1_test = (2887059456, 4294966784, '172.21.8.0/23')
    print "\tcidr1 =", cidr1, cidr1_i, int2ip(cidr1_i[0]), int2ip(cidr1_i[1])
    # print "\tcidr1\t{0:032b} {0:d} {1} {2}".format(cidr1_i[0], cidr1_i[1], int2ip(cidr1_i[0])), cidr1
    if cidr1_i == cidr1_test:
        print "\tPass"
    else:
        print "\tFail"

    cidr2 = '172.21.8.0/24'
    cidr2_i = cidr2int('172.21.8.0/24')
    cidr2_test = (2887059456, 4294967040, '172.21.8.0/24')
    print "\tcidr2 =", cidr2, cidr2_i, int2ip(cidr2_i[0]), int2ip(cidr2_i[1])
    # print "\tcidr2\t{0:032b} {0:d} {1} {2}".format(cidr2_i[0], cidr2_i[1], int2ip(cidr2_i[0])), cidr2
    if cidr2_i == cidr2_test:
        print "\tPass"
    else:
        print "\tFail"

    print "\n---\n"

    print "_ip_in_cidr :"
    #x = addr1_i & cidr1_i[0]
    #print "\ta1 & cidr1\t{0:032b} {0:d}".format(x)

    a1c1 = _ip_in_cidr(addr1_i, cidr1_i)
    print "\taddr1 in cidr1 True  ==", a1c1, addr1, cidr1

    a2c1 = _ip_in_cidr(addr2_i, cidr1_i)
    print "\taddr2 in cidr1 True  ==", a2c1, addr2, cidr1

    a2c2 = _ip_in_cidr(addr2_i, cidr2_i)
    print "\taddr2 in cidr2 False ==", a2c2, addr2, cidr2

    print "\n"

    print "ip_in_cidr :"

    a2c1 = ip_in_cidr(addr2, cidr1)
    print "\taddr2 in cidr1 True  ==", a2c1, addr2, cidr1
    assert a2c1

    a2c2 = ip_in_cidr(addr2, cidr2)
    print "\taddr2 in cidr2 False ==", a2c2, addr2, cidr2
    assert not a2c2

    a1c1 = ip_in_cidr(addr1_i, cidr1_i)
    print "\taddr1 in cidr1 True  ==", a1c1, addr1, cidr1
    assert a1c1

    a1c2 = ip_in_cidr(addr1_i, cidr2_i)
    print "\taddr1 in cidr2 True  ==", a1c2, addr1, cidr2
    assert a2c1


    print "\n---\n"

    ip_start = '91.189.88.0'
    ip_end = '91.189.95.255'

    _ip_start = ip2int(ip_start)

    cidr24 = "10.1.10.0/24"
    # cidr27 = "10.1.10.0/27"

    cidr24_i = cidr2int(cidr24)
    # cidr27_i = cidr2int(cidr27)

    # print "cidr24_i", cidr24_i

    print "subnet_cidr :"
    print "\tcidr24 :", cidr24_i
    print "\tsubnet :", 27

    # for s in subnet_cidr(cidr24_i, 27):
    #     print "\t{}".format(s)

    subnet_list = list(subnet_cidr(cidr24_i, 27))
    print "\tsubnets : ", subnet_list

    test_list = [
        '10.1.10.0/27', '10.1.10.32/27', '10.1.10.64/27', '10.1.10.96/27',
        '10.1.10.128/27', '10.1.10.160/27', '10.1.10.192/27', '10.1.10.224/27'
    ]

    if subnet_list == test_list:
        print "\tPass"
    else:
        print "\tFail"
