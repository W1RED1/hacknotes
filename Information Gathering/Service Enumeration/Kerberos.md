# Kerberos/88 (TCP/UDP)

## Questions to ask yourself
  *  Where is the KDC and is it routable?
  *  How many machines/users in the domain?
      *  Which are high-value targets?

## Useful tools
  *  [`nmap`](https://nmap.org/) for Kerberos NSE enum script
  *  [`kerbrute`](https://github.com/ropnop/kerbrute) for speedy enumeration of users
  *  [`seclists`](https://github.com/danielmiessler/SecLists) for username discovery wordlists

## Enumerating users
  *  `nmap` has an NSE script for [enumerating users via Kerberos](https://nmap.org/nsedoc/scripts/krb5-enum-users.html)
  *  `kerbrute` serves the same purpose plus threading!
  *  `seclists` for [user discovery wordlists](https://github.com/danielmiessler/SecLists/tree/master/Usernames/Names)

```
nmap -p 88 -T4 --script="krb5-enum-users" --script-args krb5-enum-users.realm='example.com' -vv 10.0.0.1
nmap -p 88 -T4 --script="krb5-enum-users" --script-args krb5-enum-users.realm='example.com',userdb=/path/to/usernames.txt -vv 10.0.0.1
```

```
kerbrute userenum --dc 10.0.0.1 -d example.com /path/to/usernames.txt
```
