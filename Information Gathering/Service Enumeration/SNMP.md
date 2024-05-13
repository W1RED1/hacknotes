# SNMP/161/162 (UDP/TCP)

## Questions to ask yourself
  *  What version of SNMP is being served?
  *  What communities are serving data?

## Things to remember
  *  Only community based SNMP flavors are covered here
      *  SNMPv3 and some configurations of SNMPv2 [do not rely on community strings](https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol#Authentication)
  *  Different data in different communities
  *  SNMP versions [1, 2, and 2c transmit in cleartext](https://www.rapid7.com/blog/post/2016/01/27/simple-network-management-protocol-snmp-best-practices/)

## Useful tools
  *  [`nmap`](https://nmap.org/) for various NSE enum scripts
  *  [`onesixtyone`](https://github.com/trailofbits/onesixtyone) for bruteforcing community strings
  *  [`seclists`](https://github.com/danielmiessler/SecLists) for community string wordlists
  *  [`snmpbulkwalk`](http://www.net-snmp.org/docs/man/snmpbulkwalk.html), [`snmpwalk`](http://www.net-snmp.org/docs/man/snmpwalk.html), and [`snmp-check`](https://www.nothink.org/codes/snmpcheck/index.php) for gathering data from MIB

## Additional NSE enumeration
  *  `nmap` has tons of [SNMP recon scripts](https://nmap.org/search/?q=snmp)

```
nmap -sU -p161 --script "not brute and snmp-*" -T4 -vv 10.0.0.1
nmap -sU -p161 --script "snmp-brute" -T4 -vv 10.0.0.1
```

## Bruteforce community strings
  *  `onesixtyone` for finding more valid community strings

```
onesixtyone -c /path/to/wordlist 10.0.0.1
```

## Community string wordlists
  *  Entire contents of [`/usr/share/seclists/Discovery/SNMP/`](https://github.com/danielmiessler/SecLists/tree/master/Discovery/SNMP)
      *  Consider using a directory wordlist as well

```
/usr/share/seclists/Discovery/SNMP/common-snmp-community-strings-onesixtyone.txt
/usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt
/usr/share/seclists/Discovery/SNMP/snmp-onesixtyone.txt
/usr/share/seclists/Discovery/SNMP/snmp.txt
```

## Dumping [MIB](https://datatracker.ietf.org/doc/html/rfc3418) data
  *  `snmpbulkwalk`, `snmpwalk`, `snmp-check` for extracting data from MIB database
      *  Increase timeout length if needed
      *  Specify MIB values to perform specific enumerations

```
snmpbulkwalk -c public -v2c 10.0.0.1 .
snmpwalk -c public -v1 -t 10 10.0.0.1
snmpwalk -c public -v1 -t 10 10.0.0.1 1.3.6.1.4.1.77.1.2.25
snmp-check -c public -v 1 -t 10 10.0.0.1
```

## MIB [paths of interest](https://book.hacktricks.xyz/network-services-pentesting/pentesting-snmp#snmp-parameters-for-microsoft-windows)
  *  MIB values associated with interesting info

```
1.3.6.1.2.1.25.1.6.0	System Processes
1.3.6.1.2.1.25.4.2.1.2	Running Programs
1.3.6.1.2.1.25.4.2.1.4	Processes Path
1.3.6.1.2.1.25.2.3.1.4	Storage Units
1.3.6.1.2.1.25.6.3.1.2	Software Name
1.3.6.1.4.1.77.1.2.25	User Accounts
1.3.6.1.2.1.6.13.1.3	TCP Local Ports
```
