# SMB/445/139 (TCP)

## Questions to ask yourself
  *  What SMB dialects are available and what OS is serving them?
      *  Refer to nmap scans version detection and script enum info
      *  `Google` and `searchsploit` all the things
  *  What SMB shares are available?
      *  Do filesystem locations of SMB shares overlap with another service?
      *  Directories/files of interest, can we read/write them?
  *  Is NetBIOS listening? Why? Are there endpoints with old/alt OSes somewhere?

## Things to remember
  *  [NetBIOS](https://datatracker.ietf.org/doc/html/rfc1001) is a legacy API providing [IPC](https://en.wikipedia.org/wiki/Inter-process_communication)
      *  Not a network transport: must be paired with a transport protocol
      *  Most commonly served as [NetBIOS over TCP/IP](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-2000-server/cc940063(v=technet.10))
  *  [SMB](https://learn.microsoft.com/en-us/windows/win32/fileio/microsoft-smb-protocol-and-cifs-protocol-overview) is primarily a file sharing protocol
      *  Often exposed via NetBIOS over TCP/IP for compatibility with old/alt operating systems
      *  Provides other services such as printer sharing and IPC via named pipes
  *  [HackTricks has a page](https://book.hacktricks.xyz/network-services-pentesting/pentesting-smb#smb-server-version) covering SMB version identification and more

## Useful tools
  *  [`nmap`](https://nmap.org/) for various NSE enum scripts
  *  [`enum4linux-ng`](https://github.com/cddmp/enum4linux-ng) for automated SMB enum
  *  [`nbtscan`](https://github.com/resurrecting-open-source-projects/nbtscan)/[`nmblookup`](https://www.samba.org/samba/docs/current/man-html/nmblookup.1.html) for gathering NetBIOS information
  *  [`netexec`](https://www.netexec.wiki/) for various enum/spraying credentials
  *  [`impacket-lookupsid`](https://github.com/fortra/impacket/blob/master/examples/lookupsid.py) for enumerating users via `lsarpc` named pipe
  *  [`exiftool`](https://exiftool.org/) for extracting metadata from any readable files

## Additional NSE enumeration
  *  `nmap` has plenty of SMB [recon/scanning scripts](https://nmap.org/search/?q=smb)
      *  Be careful with `unsafe=1`, it will crash vulnerable machines
      *  If a scan errors, use debug (`-d`) and run it again

```
nmap --script=smb-vuln* --script-args=unsafe=1 -T4 -vv 10.0.0.1
nmap --script=*samba* --script-args=unsafe=1 -T4 -vv 10.0.0.1
```

```
nmap --script="smb-enum* and not smb-enum-services" --script-args=unsafe=1 -T4 -vv 10.0.0.1
nmap --script=smb-enum-services --script-args=unsafe=1 -T4 -vv 10.0.0.1
nmap --script 'not brute and not dos and smb-*' -T4 -vv 10.0.0.1
```

## Automation
  *  `enum4linux-ng` for automatically collecting SMB service info
  *  Cover a lot of ground and make a lot of noise

```
enum4linux-ng 10.0.0.1
enum4linux-ng -u 'bob' -p 'password' 10.0.0.1
enum4linux-ng -w 'example.com' -u 'bob' -p 'password' 10.0.0.1
```

## Enumerate NetBIOS hostnames
  *  `nbtscan` and `nmblookup` for gathering NetBIOS hostnames
      *  NetBIOS is often enabled for backwards compatibility
      *  Gather neighbors of hosts with NetBIOS enabled

```
nbtscan 10.0.0.1
nbtscan -r 10.0.0.1
nmblookup -A 10.0.0.1
```

## Mapping SMB shares
  *  `smbmap`, `smbclient`, and `netexec` for listing SMB file shares
      *  Always try `guest`, `null`, and `anonymous` sessions
      *  Got creds from elsewhere? **TRY THEM ALL**
  *  **Do not** trust SMB share permissions output
      *  Always perform manual read/write checks

```
smbmap -H 10.0.0.1
smbmap -u 'anonymous' -H 10.0.0.1
smbmap -u 'bob' -p 'E52CAC67419A9A224A3B108F3FA6CB6D:8846F7EAEE8FB117AD06BDD830B7586C' -H 10.0.0.1
```

```
smbclient -U '' -L \\\\10.0.0.1
smbclient -U 'anonymous' -L \\\\10.0.0.1
```

```
netexec smb 10.0.0.1 -u 'bob' -p 'password' --shares
netexec smb 10.0.0.1 -d 'example.com' -u 'bob' -p 'password' --shares
netexec smb 10.0.0.1 -u 'bob' -H '8846F7EAEE8FB117AD06BDD830B7586C' --shares
```

## Manual R/W checks
  *  `smbclient` for reading/writing files in SMB shares
      *  Manually `get`/`put` files to verify permissions

```
smbclient -U 'anonymous' \\\\10.0.0.1\\share
smb: \> get example.txt
smb: \> put test.txt
```

## Enumerating users
  *  `impacket-lookupsid` for enumerating users via [`$IPC`](https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/inter-process-communication-share-null-session) share
      *  Performs enumeration using named pipe [`lsarpc`](https://github.com/fortra/impacket/blob/master/examples/lookupsid.py#L39)

```
impacket-lookupsid bob:password@10.0.0.1 -target-ip 10.0.0.1
impacket-lookupsid bob:password@exampleHostname -target-ip 10.0.0.1
```

## Download all files
  *  `smbmap` for automatically downloading files
  *  `smbclient` for manually downloading files
  *  Create a new directory for this to keep things clean

```
smbmap -u bob -p 'E52CAC67419A9A224A3B108F3FA6CB6D:8846F7EAEE8FB117AD06BDD830B7586C' -H 10.0.0.1 -s share -R -A '.*'
```

```
smbclient -U 'anonymous' \\\\10.0.0.1\\share
smb: \> RECURSE ON
smb: \> PROMPT OFF
smb: \> mget *
```

## Extract metadata from files
  *  `exiftool` for extracting metadata from readable files
  *  Metadata can contain a plethora of information!

```
exiftool example.xlsx
exiftool -a -u example.pdf
```
