# simple_cidr


A simple lightweight IPv4 CIDR address toolbox

written: Peter Shipley


Small and fast IPv4 network address tool (75% faster then netaddr)

For cases where netaddr is too slow and you do not need the kitchen sink

To use:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ```from simple_cidr import *```

-or-

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; just copy the functions you need into your code...



Example code
------------


```python
from simple_cidr import ip2int, cidr2int, ip_in_cidr, _ip_in_cidr

local_cidr = "10.1.10.0/21"
test_ip_list = [
    '1.183.157.52', '59.152.13.85', '132.255.253.243', '1.54.12.112',
    '91.93.164.13', '23.94.184.55', '52.2.45.42', '10.1.13.244',
    '31.163.95.153', '10.1.11.1', '103.60.220.87', '10.1.10.55'
]

my_cidr = cidr2int(local_cidr)

for ip in test_ip_list:
    if ip_in_cidr(ip, my_cidr):
        print ip, "\tis local"
    else:
        print ip, "\tis non-local"

```
