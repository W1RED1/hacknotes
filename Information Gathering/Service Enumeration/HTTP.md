# HTTP/80/443 (TCP)  

## Questions to ask yourself
  *  What is the web stack being used?
      *  Is there more than one?
  *  Is there a CMS being used?
      *  Any plugins installed?
  *  Anything weird in the source code?
  *  What HTTP methods are available?
  *  Any writable WebDAV shares appear to be frequently opened?
      *  Consider setting a [trap to coerce authentication](https://www.ired.team/offensive-security/initial-access/t1187-forced-authentication)

## Things to remember
  *  `searchsploit` and `Google` **all the things**
  *  Watch out for sites running multiple backends
  *  Interact with the site as a normal user
      *  Read and click through **everything**
  *  Review source code carefully
      *  View source on **ALL THE PAGES ALWAYS**
      *  Values of input fields in the HTML source can expose parameters
      *  Use browser `Inspector` to view the [DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model)
  *  Pass all traffic through Burp proxy
      *  Look at GET/POST parameters, cookies, etc.
      *  Try different HTTP methods for any interesting requests

## Useful tools
  *  [`Burpsuite`](https://portswigger.net/burp/communitydownload) for manipulating web requests
  *  [`FoxyProxy`](https://getfoxyproxy.org/) for switching between proxies while browsing
  *  [`curl`](https://curl.se/) for quickly grabbing HTTP response headers
  *  [`nmap`](https://nmap.org/) for various NSE enum scripts
  *  [`nikto`](https://github.com/sullo/nikto) for web server vuln scanning
  *  [`gobuster`](https://github.com/OJ/gobuster) for bruteforce discovery of various domains and resources
  *  [`seclists`](https://github.com/danielmiessler/SecLists) for various fuzzing/discovery wordlists
  *  [`wfuzz`](https://www.edge-security.com/wfuzz.php) for web fuzzing/discovery
  *  [`davtest`](https://github.com/cldrn/davtest) and [`cadaver`](https://github.com/notroj/cadaver) for testing/interacting with WebDAV file shares
  *  [`whatweb`](https://morningstarsecurity.com/research/whatweb) for gathering web stack info via HTTP response headers
  *  [`wpscan`](https://wpscan.com/)/[`droopescan`](https://github.com/SamJoan/droopescan) for scanning respective CMSes

## Browsing through a proxy
  *  Some sites may require you to reach other sites on the internet to render properly
      *  Configure pattern matching in `FoxyProxy` to only proxy certain URLs
      *  Clear the configuration when done!

## Header grab
  *  `curl` for grabbing any interesting HTTP response headers
      *  Useful for confirming OS/web server software

```
curl -i 10.0.0.1
```

## Additional NSE enumeration
  *  `nmap` has plenty of [HTTP recon/scanning scripts](https://nmap.org/search/?q=http)

```
nmap -p 80 -T4 -sC -sV --script=http-enum -vv 10.0.0.1
nmap -p 80 -T4 -sC -sV --script="vuln" -vv 10.0.0.1
```

## Identify web stack
  *  Collect data on underlying web technology
  *  What is the server OS?
  *  What web server soft is serving it?
      *  Response headers can expose this and more
  *  What database server soft is it running?
      *  The presence of certain admin consoles can indicate DB software
  *  What backend language/frameworks is the app using?
      *  File extensions are not always reliable, but still useful
      *  Check browser dev console functions: `Inspector`, `Debugger`, `Network`, etc.
  *  What dependencies are used underneath the application?
      *  Monitor HTTP headers during site interactions
      *  Metadata of generated content can expose dependencies

## Web server scanning
  *  `nikto` for generic web server vuln scanning: **read all of it**

```
nikto -h http://10.0.0.1
```

## Source code review
  *  **VIEW THE SOURCE LUKE**
      *  Watch out for anything that resembles an HTTP resource
      *  Read all comments, and watch for web stack related info
  *  Consider creating a personal sitemap to track reviewed pages
  *  Don't mangle code when using online deobfuscators/beautifiers

## Directory busting
  *  `gobuster` for bruteforcing HTTP resources
  *  **Run more than one wordlist**
      *  Consider running multiple times during unfavorable network conditions
      *  Combine multiple wordlists to eliminate duplicate values
  *  Common sitemaps include `robots.txt` and `sitemap.xml`
  *  Check for HTTP resources matching words of interest

```
gobuster dir --url http://10.0.0.1 --wordlist /usr/share/wordlists/dirb/big.txt -t 40 -x php,zip,bak
```

// List of extensions
```
txt,php,aspx,cgi,asp,html,jsp,pdf,doc,docx,xls,xlsx,rtf,bak,xml,xsl,phpthml,sh,pl,py,config,php7,exe
```

## Directory/File wordlists
  *  Various `seclists` files for HTTP directory/file discovery
  *  More at [`/usr/share/seclists/Discovery/Web-Content/`](https://github.com/danielmiessler/SecLists/tree/master/Discovery/Web-Content)

```
/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
/usr/share/seclists/Discovery/Web-Content/common.txt
/usr/share/seclists/Discovery/Web-Content/big.txt
/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
```

## VHOST busting
  *  `gobuster` for bruteforcing [Virtual Hosts](https://httpd.apache.org/docs/current/vhosts/)
  *  Found any subdomains already?
      *  Consider modifying a wordlist based on that naming convention

```
gobuster vhost --url http://example.com --wordlist /usr/share/seclists/Discovery/DNS/namelist.txt -t 40
```

## VHOST/subdomain wordlists
  *  Various `seclists` files for VHOST discovery
  * More at [`/usr/share/seclists/Discovery/DNS/`](https://github.com/danielmiessler/SecLists/tree/master/Discovery/DNS)

```
/usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt
/usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt
/usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt
```

## Parameter fuzzing
  *  `wfuzz` for fuzzing parameters of an HTTP resource
      *  Also applies to REST APIs
      *  Parameters often exist without being listed in the HTML source
  *  Fuzz parameter values as well
      *  This will multiply the number of requests
      *  Consider creating a smaller wordlist to avoid massive request amounts
      *  Use alphanum characters, web attack strings, commands, anything!
      *  Fuzz multiple times using different HTTP methods

```
wfuzz -w /path/to/wordlist.txt http://10.0.0.1/page?FUZZ=id
wfuzz -w /path/to/wordlist1.txt -w /path/to/wordlist2.txt http://10.0.0.1/page?FUZZ=FUZ2Z
```

## Parameter wordlists
  *  Various `seclists` files for fuzzing parameters
      *  Includes wordlists for fuzzing various web attacks
      *  Consider using a directory list as well

```
/usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt
/usr/share/seclists/Discovery/Web-Content/api/*
/usr/share/seclists/Fuzzing/command-injection-commix.txt
/usr/share/seclists/Fuzzing/LFI/*
/usr/share/seclists/Fuzzing/SQLi/*
/usr/share/seclists/Fuzzing/XSS/*
```

## [WebDAV](http://www.webdav.org/)
  *  Upload/download files from a shared portion of the filesystem
  *  `davtest` useful for quickly testing a bunch of filetypes
  *  `cadaver` useful for manually interacting with WebDAV shared files

```
davtest -url 'http://10.0.0.1/'
davtest -auth bob:password -url 'http://10.0.0.1/'
cadaver http://10.0.0.1
```

## CMS detection
  *  `whatweb` and HTTP response headers can potentially disclose CMS
      *  CMS can appear in source code but may not disclose version number
      *  CMS directories may appear disallowed in **robots.txt**
  *  Once a CMS is identified check default/install/config files for version numbers

```
whatweb 'http://10.0.0.1'
whatweb -v 'http://10.0.0.1'
```

## [Wordpress](https://wordpress.com/) enumeration
  *  `wpscan` will withhold vulnerability info if you do not supply an API key
      *  `searchsploit` **everything**
      *  Do both passive and aggressive plugin detection
      *  It can also enumerate users!
  *  There are a variety of methods to achieve RCE using wordpress admin creds: **GTS**

```
wpscan --url http://example.com
wpscan --url http://example.com --plugins-detection aggressive
wpscan --url http://example.com -e u1-10000
wpscan --url http://example.com --enumerate ap,at,cb,dbe
```

## [Coldfusion](https://www.adobe.com/products/coldfusion-family.html) [enumeration](https://nets.ec/Coldfusion_hacking)
  *  `nmap` has [NSE scripts for CF vuln scanning](https://nmap.org/search/?q=coldfusion)
  *  Version number should be obvious if login panels are available
      *  `searchsploit` all the things

## [Drupal](https://www.drupal.org/) enumeration
  *  Drupal version often exposed via website source code
  *  `droopescan` useful for quick enumeration of drupal
      *  No longer maintained, easiest to run with `docker`
  *  NSE has some scripts for drupal enum
  *  `searchsploit` and probably check `drupalgeddon`

```
nmap -p 80 --script="*drupal*" 10.0.0.1
```

// Docker build and usage
```
git clone https://github.com/droope/droopescan.git && cd droopescan
sudo docker build -t droope/droopescan .
sudo docker run --rm droope/droopescan scan drupal -u http://10.0.0.1/
```

// Docker image/container cleanup
```
sudo docker rm $(sudo docker ps -aq)
sudo docker rmi $(sudo docker images -a -q)
```
