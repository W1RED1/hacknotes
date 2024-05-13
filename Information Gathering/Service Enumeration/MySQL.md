# MySQL/3306 (TCP)  

## Questions to ask yourself  
  *  What services rely on the MySQL databases?
      *  Could modification of a DB lead to further access?
  *  Is the MySQL service exposed outside localhost? Why?

## Useful tools
  *  [`nmap`](https://nmap.org/) for various NSE enum scripts
  *  [`mysql`](https://dev.mysql.com/doc/refman/8.3/en/mysql.html) CLI client for most MySQL interactions
  *  [`hydra`](https://github.com/vanhauser-thc/thc-hydra) for checking default/weak MySQL credentials
  *  [`seclists`](https://github.com/danielmiessler/SecLists) for default credential wordlists

## Additional NSE enumeration
  *  `nmap` has plenty of [MySQL recon/scanning scripts](https://nmap.org/search/?q=mysql)
      * Re-run if credentials are obtained  

```
nmap -p3306 -sV -sC -T4 -vv --script=mysql* 10.0.0.1
nmap -p3306 -sV -sC -T4 -vv --script=mysql-enum --script-args userdb=/path/to/names.txt 10.0.0.1
```

```
nmap -p3306 -sV -sC -T4 -vv --script=mysql-audit,mysql-databases,mysql-dump-hashes,mysql-empty-password,mysql-enum,mysql-info,mysql-query,mysql-users,mysql-variables,mysql-vuln-cve2012-2122 10.0.0.1
```

```
nmap -p3306 -sV -sC -T4 -vv --script="mysql* and not (mysql-brute or mysql-enum or mysql-vuln-cve2012-2122)" --script-args mysqluser=bob,mysqlpass=password 10.0.0.1
```

## Connecting to MySQL
  *  Port forwarding not needed, use from shell

```
mysql -u root -p
mysql -u root -h 10.0.0.1 -P 3306 -p
```

## Default credentials
  *  `hydra` for quickly checking default/weak credentials
  *  `Google` DBMS/DBMS version to find default cred lists 

```
root : root
root : (blank)
sa : sa
sa : (blank)
```

```
hydra -C /usr/share/seclists/Passwords/Default-Credentials/mysql-betterdefaultpasslist.txt -vV mysql://10.0.0.1
```

## Searching for credentials
  *  Consider where credentials may be [stored within the DBMS](https://dev.mysql.com/doc/mysql-security-excerpt/8.3/en/assigning-passwords.html)
  *  Check directories of services that may use a DB
      *  e.g. web roots often contain creds in config files
      *  e.g. backend language/framework files
  *  [Log](https://www.oreilly.com/library/view/mysql-reference-manual/0596002653/ch04s09.html) [files](https://book.hacktricks.xyz/network-services-pentesting/pentesting-mysql#useful-files) can possibly contain credentials

```
~/.mysql.history
connections.log
update.log
common.log
```

## Config files
  *  Review [config files](https://book.hacktricks.xyz/network-services-pentesting/pentesting-mysql#useful-files) of `mysqld` for anything interesting
  *  `Google` DBMS/DBMS version and OS for specific locations

// *nix
```
my.cnf
/etc/mysql
/etc/my.cnf
/etc/mysql/my.cnf
/var/lib/mysql/my.cnf
~/.my.cnf
/etc/my.cnf
```

// Windows
```  
config.ini
my.ini
windows\my.ini
winnt\my.ini
[MYSQL INSTANCE DIR]/mysql/data/
```

## Command execution
  *  [`into dumpfile`](https://dev.mysql.com/doc/refman/8.0/en/select-into.html) can be used to write files to the filesystem
      *  Check target location permissions with [`load_file()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_load-file) and [`@@secure_file_priv`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_secure_file_priv)
  *  Write [loadable function](https://dev.mysql.com/doc/extending-mysql/8.0/en/adding-functions.html) data to filesystem to [facilitate code execution](https://book.hacktricks.xyz/network-services-pentesting/pentesting-mysql#privilege-escalation-via-library)
      *  Any upload mechanisms available?
      *  Use [`hex()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_hex)/[`unhex()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_unhex) to transfer binary data
      *  `metasploit` and `sqlmap` provide `.dll`/`.so` files for this purpose

// **NOTE**: The function in these files is `sys_exec`
```
locate *lib_mysqludf_sys*
```
