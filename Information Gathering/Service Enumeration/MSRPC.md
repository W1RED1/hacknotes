# MSRPC/135 (TCP)

## Questions to ask yourself
  *  What is the OS version?  
      *  Refer to `nmap` scans version detection and script enum info
      *  Does `Google` or `searchsploit` have anything to say?
  *  What services are mapped via RPC?
      *  Are any of them exposed to the network?

## Things to remember
  *  [MSRPC](https://learn.microsoft.com/en-us/windows/win32/rpc/rpc-start-page) is old and runs under the hood of a lot of stuff

## Useful tools
  *  [`nmap`](https://nmap.org/) for various RPC NSE enum scripts
  *  [`impacket-rpcdump`](https://github.com/fortra/impacket/blob/master/examples/rpcdump.py) and [`impacket-rpcmap`](https://github.com/fortra/impacket/blob/master/examples/rpcmap.py) for gathering RPC interfaces/endpoints
  *  [`enum4linux-ng`](https://github.com/cddmp/enum4linux-ng) for automatic RPC enum
  *  [`rpcclient`](https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html) for manual RPC enum

## Additional NSE enumeration
  *  `nmap` has a few [MSRPC recon/scanning scripts](https://nmap.org/search/?q=msrpc)
      *  If a scan errors, debug (`-d`) and run it again

```
nmap --script=msrpc-enum -vv 10.0.0.1
```

## Enumerating RPC mappings
  *  Dump MSRPC interfaces and endpoints
      *  Confirming services such as `DCOM` can be useful for code exec
      *  Watch for interesting Windows services listed via RPC mapping

```
impacket-rpcdump @10.0.0.1 -target-ip 10.0.0.1
impacket-rpcdump guest@10.0.0.1 -target-ip 10.0.0.1
impacket-rpcmap ncacn_ip_tcp:10.0.0.1
impacket-rpcmap 'ncacn_ip_tcp:10.0.0.1[135]' -target-ip 10.0.0.1 -auth-rpc 'example.com/bob:pass123'
```

## Automatic RPC enumeration
  *  `enum4linux-ng` for automated RPC enumeration

```
git clone https://github.com/cddmp/enum4linux-ng && cd enum4linux-ng
./enum4linux-ng.py -A 10.0.0.1
./enum4linux-ng.py -u bob -p password -w example.com
./enum4linux-ng.py -u bob -H [NT HASH] --local-auth
```

## Manual RPC enumeration
  *  `rpcclient` for manual RPC enumeration
      *  Seeing `NT_STATUS_NOT_FOUND`? Update `smbclient`
      *  [Lots of system information to be had here!](https://www.hackingarticles.in/active-directory-enumeration-rpcclient/)
  *  Got creds from elsewhere? **TRY THEM ALL**

```
rpcclient -U '' -N 10.0.0.1
rpcclient -U 'anonymous' 10.0.0.1
rpcclient -U bob 10.0.0.1
rpcclient -U bob%[NT HASH] --pw-nt-hash 10.0.0.1
```

// Basic system info
```
rpcclient $> srvinfo
```

// Enumerate users and groups
```
rpcclient $> querydispinfo
rpcclient $> enumdomusers
rpcclient $> queryuser [RID]
rpcclient $> queryusergroups [RID]
rpcclient $> lookupnames [USERNAME]
rpcclient $> queryuseraliases [builtin|domain] [SID]
rpcclient $> enumdomgroups
rpcclient $> querygroup [RID]
rpcclient $> querygroupmem [RID]
rpcclient $> enumalsgroups [builtin|domain]
rpcclient $> queryaliasmem [builtin|domain] [RID]
```

// Enumerate domains
```
rpcclient $> enumdomains
rpcclient $> lsaquery
rpcclient $> querydominfo
rpcclient $> dsroledominfo
rpcclient $> dsenumdomtrusts
```

// Enumerate all SIDs
```
rpcclient $> lsaenumsid
rpcclient $> lookupsids [SID]
```

// Manipulate user accounts
```
rpcclient $> createdomuser [USERNAME]
rpcclient $> deletedomuser [USERNAME]
rpcclient $> lsaaddacctrights [SID] [RIGHTS...]
rpcclient $> lsaremoveacctrights [SID] [RIGHTS...]
rpcclient $> setuserinfo2 [USERNAME] 23 [PASSWORD]
```
