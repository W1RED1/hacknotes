# POP3/110 (TCP) 

## Questions to ask yourself
  *  What mail server software and version is running?
      *  Refer to nmap scans version detection and script enum info
      *  What do `Google` and `searchsploit` have to say about that?
  *  Is authentication required to check the mail?
  *  What users are able to login?
      *  Do you have creds? **TRY THEM ALL**
   
## Things to remember
  *  **ALWAYS CHECK THE MAIL**

## Useful tools
  *  [`nmap`](https://nmap.org/) for various NSE enum scripts
  *  [`netcat`](http://www.stearns.org/nc/)/[`telnet`](https://linux.die.net/man/1/telnet) for banner grab/manual POP3 interactions

## Additional NSE enumeration
  *  `nmap` has a few [POP3 recon scripts](https://nmap.org/search/?q=pop3)

```
nmap -p 110 --script="*pop3* and not pop3-brute" 10.0.0.1
```

## Banner grab
  *  `netcat` banner grab for quick service identification

```
nc -vn 10.0.0.1 110
```

## Retrieve e-mail from POP3 server
  *  `telnet` client for [manually reading POP3 messages](https://www.vircom.com/blog/quick-guide-of-pop3-command-line-to-type-in-telnet/)
  *  See [RFC 1939](https://www.ietf.org/rfc/rfc1939.txt) for POP3 command details

```
telnet 10.0.0.1 110
USER username
PASS password
STAT
LIST
RETR [MESSAGE NUMBER]
```
