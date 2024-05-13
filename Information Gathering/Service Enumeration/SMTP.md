# SMTP/25 (TCP) 

## Questions to ask yourself
  *  What mail server software and version is running?
      *  Refer to nmap scans version detection and script enum info
      *  What do `Google` and `searchsploit` have to say about that?
  *  Is authentication required to send e-mail?
  *  What e-mail addresses are deliverable?
      *  Try e-mail interaction with user?
      *  Do you have creds? Try sending with those.
   
## Things to remember
  *  Sending e-mails as another user is risky
      *  Much safer to sit in the inbox and intercept messages

## Useful tools
  *  [`nmap`](https://nmap.org/) for various NSE enum scripts
  *  [`netcat`](http://www.stearns.org/nc/) for banner grab/manual SMTP interactions
  *  [`smtp-user-enum`](https://pentestmonkey.net/tools/user-enumeration/smtp-user-enum) for gathering users via certain [SMTP](https://datatracker.ietf.org/doc/html/rfc5321#section-3.5) [commands](https://datatracker.ietf.org/doc/html/rfc5321#section-3.3)
  *  [`seclists`](https://github.com/danielmiessler/SecLists) for username wordlists
  *  [`sendemail`](http://caspian.dotconf.net/menu/Software/SendEmail/) for... sending e-mails

## Additional NSE enumeration
  *  `nmap` has plenty of [SMTP recon/scanning scripts](https://nmap.org/search/?q=smtp)

```
nmap -sS -p25 -T4 --script smtp-* -vv 10.0.0.1
```

## Banner grab
  *  `netcat` banner grab for quick service identification

```
nc -vn 10.0.0.1 25
```

## Enumerating users
  *  `smtp-user-enum` for gathering users via `VRFY`, `EXPN`, and `RCPT TO` commands
      *  Refer to nmap script enum info for proper method to use
  *  Username wordlists at [`/usr/share/seclists/Usernames/`](https://github.com/danielmiessler/SecLists/tree/master/Usernames)
      *  Have a list of known users from elsewhere? **TRY THEM**

```
smtp-user-enum -M VRFY -U usernames.txt -t 10.0.0.1
smtp-user-enum -M VRFY -U usernames.txt -D example.com -t 10.0.0.1
```

## Sending e-mail
  *  `sendemail` for sending basic e-mails from CLI
      *  Consider a traditional e-mail client for crafting finer e-mails

```
sendemail -f attacker@attacker -t victim@victim -u 'This is the subject line!' -m 'This is the email body!' -s 10.0.0.1:25
```
