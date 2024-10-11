# Port Scanning

## Useful tools
  *  [`nmap`](https://nmap.org/docs.html) includes many [scan types](https://nmap.org/book/scan-methods.html) and [evasion](https://nmap.org/book/man-bypass-firewalls-ids.html) [features](https://nmap.org/book/subvert-ids.html)
  *  Consider probing with packet crafting tools like [`hping3`](https://www.kali.org/tools/hping3/) or [`scapy`](https://scapy.net/)
      *  Determine effective scan types and potential evasion techniques **before** scanning

## Manual probing
  *  Send crafted packets to determine useable scan types
      *  See `nmap` scan types and [`hping3`](https://linux.die.net/man/8/hping3)/[`scapy`](https://scapy.readthedocs.io/en/latest/usage.html#simple-one-liners) manuals

```
hping3 10.0.0.1 -c 1 -p 22 -S
hping3 10.0.0.1 -c 1 -p 22 -F
```

```
>>> ans, unans = sr(IP(dst="10.0.0.1")/TCP(dport=22,flags="S"))
>>> ans, unans = sr(IP(dst="10.0.0.1")/TCP(dport=22,flags="F"))
```

## Pivot scanning
  *  Default `proxychains` [configuration has a lengthy timeout](https://github.com/haad/proxychains/blob/master/src/proxychains.conf#L53)
      *  Make it faster by reconfiguring the timeouts
      *  Poorly configured timeouts will lead to false negatives
      *  Most other solutions are faster for when speed is priority
  *  Upload a port scanner to the beachhead and scan from there
      *  For this purpose, [`portscan.go`](https://github.com/SpacemanHenry/hacknotes/blob/main/Information%20Gathering/Port%20Scanning/portscan.go) and [`portscan.py`](https://github.com/SpacemanHenry/hacknotes/blob/main/Information%20Gathering/Port%20Scanning/portscan.py) were written
      *  [`netcat`](https://www.cyberciti.biz/faq/linux-port-scanning/)/[`bash`](https://github.com/Sq00ky/Bash-Port-Scanner) can also perform port scans

```
GOOS=linux GOARCH=amd64 go build -o portscan portscan.go
GOOS=linux GOARCH=386 go build -o portscan portscan.go
GOOS=windows GOARCH=amd64 go build -o portscan.exe portscan.go
GOOS=windows GOARCH=386 go build -o portscan.exe portscan.go
./portscan 10.0.0.1 1 65535 5 500
```

```
nc -nvz 10.0.0.1 1-65535 2>/dev/null
for port in $(seq 1 65535); do 2> /dev/null > /dev/tcp/10.0.0.1/$port && echo "Port $port: open"; done
```

## TCP scanning
  *  Scan twice to catch false negatives
  *  Consider omitting service/OS identification to speed up scans
      *  Perform fingerprinting once open ports are identified

```
nmap -sS --top-ports 100 -T4 -A -vv 10.0.0.1
nmap -sS -p- -T4 -A -vv 10.0.0.1
```

## [UDP scanning](https://nmap.org/book/scan-methods-udp-scan.html)
  *  UDP services are unresponsive to incorrect data
      *  `nmap` UDP results of `open|filtered` often followed with `no-response`
      *  UDP service identification often relies on sending the expected data structure

```
nmap -sU -p- -T4 -sC -sV -vv 10.0.0.1
nmap -sU -p- -T4 -sC -sV --version-intensity 0 -vv 10.0.0.1 
nmap -sU -p53,161,162 -T4 -sC -sV -vv 10.0.0.1
```
