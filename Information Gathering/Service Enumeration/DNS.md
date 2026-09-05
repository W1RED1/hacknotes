# DNS/53 (TCP/UDP)

## Questions to ask yourself
  *  What is the nameserver software and version number?
  *  Does there appear to be a naming convention?
      *  Consider modifying a wordlist to match

## Things to remember
  *  Research CVEs for any nameserver software components
  *  Different zone files exist for different domains, including [subdomains](https://datatracker.ietf.org/doc/html/rfc1034#section-3.1)
  *  Nameservers in the DNS chain may have interesting records
      *  Don't jump to a single nameserver for everything

## Useful tools
  *  [`dig`](https://linux.die.net/man/1/dig) and [`host`](https://linux.die.net/man/1/host) for obtaining DNS records
  *  [`dnsrecon`](https://github.com/darkoperator/dnsrecon), [`dnsenum`](https://github.com/SparrowOchon/dnsenum2), and [`nmap`](https://nmap.org/docs.html) for various DNS enumeration capabilities
  *  [`gobuster`](https://github.com/OJ/gobuster) for threaded DNS bruteforcing
  *  [`seclists`](https://github.com/danielmiessler/SecLists) for various subdomain wordlists

## [Zone transfer](https://en.wikipedia.org/wiki/DNS_zone_transfer) ([AXFR](https://datatracker.ietf.org/doc/html/rfc5936))
  *  `dnsrecon` and `dig` for performing zone transfers
      *  Try all available nameservers
      *  Try to replicate zone files for all known subdomains

```
dig ns example.com
dig ns example.com @example.public.nameserver
```

```
dnsrecon -t axfr -d example.com
dnsrecon -t axfr -d example.com -n nameserver.example.com
```

```
dig axfr @nameserver.example.com
dig axfr example.com @nameserver.example.com
```

## Obtaining DNS records
  *  `dnsrecon` and `dnsenum` to automatically request DNS records
  *  `host` and `dig` to manually request DNS records
  *  Query public DNS sources for target nameservers
  *  There are many [types of DNS records](https://datatracker.ietf.org/doc/html/rfc1035#section-3.2):
      *  `NS` records point to authoritative nameservers for a domain
      *  `A`/`AAAA` records get IPv4/IPv6 from hostname
      *  `CNAME` records create aliases for other records
      *  `MX` records point to mail servers
      *  `PTR` records point to other records based on associated IP (used in reverse lookups)
      *  `TXT` records can contain arbitrary data

```
dnsrecon -d example.com
dnsrecon -d example.com -n example.public.nameserver
dnsenum example.com
dnsenum example.com --dnsserver example.public.nameserver
```

```
host example.com example.public.nameserver
host www.example.com example.public.nameserver
host -t mx example.com example.public.nameserver
```

```
dig -f scope.txt @example.public.nameserver +noall +answer
dig cname example.com @example.public.nameserver
dig mx example.com @example.public.nameserver
```

## Forward-lookup bruteforce
  *  `gobuster` for finding more subdomains
  *  Generated a custom wordlist? Keep it
      *  Recycle it for any VHOST bruteforcing
      *  **DO NOT** assume DNS entries exist for all VHOSTs

```
gobuster dns --domain 'example.com' --resolver 'example.public.nameserver:53' -c -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -t 35
```

## Subdomain wordlists
  *  Various `seclists` files for subdomain discovery
  *  More at [`/usr/share/seclists/Discovery/DNS/`](https://github.com/danielmiessler/SecLists/tree/master/Discovery/DNS)

```
/usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt
/usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt
/usr/share/seclists/Discovery/DNS/namelist.txt
/usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt
```

## Reverse-lookup scanning
  *  `dnsrecon` and `nmap` for performing reverse lookup scans
      *  Discover potential live hosts via reverse lookup of each IP in a given space

```
dnsrecon -r 10.0.0.1/24
dnsrecon -r 10.0.0.1/24 -n nameserver.example.com
dnsrecon -d example.com -r 10.0.0.1/24 -n nameserver.example.com
```

```
nmap -sL 10.0.0.1/24
nmap -sL -iL scope.txt
```

## Nameserver self-resolution
  *  Manually resolve the name of the nameserver itself

```
nslookup
> server 10.0.0.1
> 10.0.0.1
```
