# MSSQL/1433 (TCP)

## Questions to ask yourself  
  *  What services rely on the MSSQL databases?
      *  Could modification of a DB lead to further access?
  *  Is the MSSQL service exposed outside localhost? Why?

## Useful tools
  *  [`nmap`](https://nmap.org/) for various NSE enum scripts
  *  [`impacket-mssqlclient`](https://github.com/fortra/impacket/blob/master/examples/mssqlclient.py) for connecting to MSSQL from linux
  *  [`hydra`](https://github.com/vanhauser-thc/thc-hydra) for checking default/weak MSSQL credentials
  *  [`seclists`](https://github.com/danielmiessler/SecLists) for default credential wordlists

## Additional NSE enumeration
  *  `nmap` has plenty of [MSSQL recon/scanning scripts](https://nmap.org/search/?q=mssql)
     * Re-run if credentials are obtained
  * These NSE scripts are broken in `nmap` version (7.93)
      *  To use these, first download and extract `nmap-7.92.tgz`
      *  Pass `--datadir` so nmap knows where to find the scripts

```
wget https://nmap.org/dist/nmap-7.92.tgz
tar -xvf nmap-7.92.tgz
```

```
nmap -p 1433 -T4 -vv --datadir="/path/to/extracted/nmap-7.92/" --script="ms-sql-* and not brute" 10.0.0.1
nmap -p 1433 -T4 -vv --datadir="/path/to/extracted/nmap-7.92/" --script="ms-sql-* and not brute" --script-args=mssql.username='sa',mssql.password='password' 10.0.0.1
```

## Connecting to MSSQL
  *  `impacket-mssqlclient` for remotely interacting with MSSQL
  *  **Port forwarding needed** if MSSQL is listening internally
      *  No Windows CLI MSSQL client currently available

```
impacket-mssqlclient 'sa':'password'@10.0.0.1
impacket-mssqlclient exampleDomain.local/bob:password@10.0.0.1 -windows-auth
```

## Default credentials
  *  `hydra` for quickly checking default/weak credentials
  *  `Google` DBMS/DBMS version to find default cred lists 

```
sa : sa
sa : (blank)
sa : RPSsql12345
```

```
hydra -C /usr/share/seclists/Passwords/Default-Credentials/mssql-betterdefaultpasslist.txt -vV mssql://10.0.0.1
```

## Searching for credentials
  *  Consider where credentials may be stored within the DBMS
  *  Check directories of services that may use a DB
      *  e.g. [web roots](https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ms474356(v=office.14)) often contain creds in config files
      *  e.g. backend files such as `.asp`, `.jsp`, `.php`
  *  [Log files](https://learn.microsoft.com/en-us/sql/tools/configuration-manager/viewing-the-sql-server-error-log?view=sql-server-ver16) can possibly contain credentials

## Config files
  *  Review [MSSQL config files](https://learn.microsoft.com/en-us/sql/sql-server/install/file-locations-for-default-and-named-instances-of-sql-server?view=sql-server-ver16) for anything interesting
  *  `Google` DBMS/DBMS version and OS for specific locations

## Command execution
  *  [Ole Automation Procedures](https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/ole-automation-procedures-server-configuration-option?view=sql-server-ver16) can be used to [write files to the filesystem](https://book.hacktricks.xyz/network-services-pentesting/pentesting-mssql-microsoft-sql-server#write-files)
  *  [`xp_cmdshell`](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/xp-cmdshell-transact-sql?view=sql-server-ver16) for executing commands on the underlying OS
      *  Hunt for privilege escalation vectors **within** MSSQL
      *  Have `sa` credentials? Gain RCE with `impacket-mssqlclient`
