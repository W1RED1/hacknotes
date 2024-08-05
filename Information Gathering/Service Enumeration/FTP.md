# FTP/21 (TCP) 

## Questions to ask yourself
  *  What is the version number?  
      *  Refer to nmap scans version detection and script enum info
      *  `Google` and `searchsploit` all the things
  *  What are my permissions?
      *  Directories/files of interest, can we read/write them?
      *  Gaining creds means gaining permissions, check back in later
  *  Where does this FTP directory exist on the filesystem?
      *  Does it overlap with another service?
      *  `Google` names of interesting directories and files
  *  Any writable shares appear to be frequently opened?
      *  Consider setting a [trap to coerce authentication](https://www.ired.team/offensive-security/initial-access/t1187-forced-authentication)

## Things to remember
  *  Manual [FTP protocol commands](https://en.wikipedia.org/wiki/List_of_FTP_commands) requires manipulation of both [control and data channels](https://userpages.umbc.edu/~dgorin1/451/OSI7/dcomm/ftp.htm)
  *  Check all files for sensitive information

## Useful tools
  *  [`nmap`](https://nmap.org/) for various NSE enum scripts
  *  [`netcat`](http://www.stearns.org/nc/)/[`openssl`](https://www.openssl.org/docs/man1.0.2/man1/openssl-s_client.html) for banner grab/manual FTP interactions
  *  [`hydra`](https://github.com/vanhauser-thc/thc-hydra) for checking default/weak FTP credentials
  *  Standard [`ftp`](https://linux.die.net/man/1/ftp) client for most FTP interactions
  *  [`exiftool`](https://exiftool.org/) for extracting metadata from any readable files
  *  [`seclists`](https://github.com/danielmiessler/SecLists) for default credential wordlists

## Additional NSE enumeration
  *  `nmap` has plenty of [FTP recon scripts](https://nmap.org/search/?q=ftp)

```
nmap -sS -p21 -T4 --script "ftp-* and not ftp-brute" -sV -vv 10.0.0.1
```

## Banner grab
  *  `netcat` banner grab for quick service identification
  *  `openssl` for connecting to FTP over TLS ([FTPS](https://datatracker.ietf.org/doc/html/rfc4217))

```
nc -vn 10.0.0.1 21
openssl s_client -connect 10.0.0.1:21 -starttls ftp
```

## Anonymous login
  *  Check if anonymous login is enabled

```
anonymous : anonymous
anonymous : (blank)
ftp : ftp
```

```
ftp anonymous@10.0.0.1
```

## Default credentials
  *  `hydra` for quickly checking default/weak credentials
  *  `Google` ftpd version/version #

```
hydra -C /usr/share/seclists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt -vV ftp://10.0.0.1
```

## HELP and FEAT commands
  *  List supported FTP commands/features

```
ftp> HELP
ftp> FEAT
```

## Download all files from FTP session
  *  Recursively download all readable files

```
ftp> mget *
mget example.txt [anpqy?]? a
```

```
wget -m ftp://anonymous@10.0.0.1
```

## Extract metadata from files
  *  `exiftool` for extracting metadata from readable files
  *  Metadata can contain a plethora of information!

```
exiftool example.xlsx
exiftool -a -u example.pdf
```

## Upload file
  *  Consider FTP `active`/`passive` mode [differences](https://stackoverflow.com/questions/1699145/what-is-the-difference-between-active-and-passive-ftp)
      *  `passive` mode generally preferred

```
ftp> binary
ftp> put example.txt
```
