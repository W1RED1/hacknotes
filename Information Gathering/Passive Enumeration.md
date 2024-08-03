# Passive enumeration

## Questions to ask yourself
  *  How many users are within the target organization?
  *  Does the target organization have any known partner/parent/sister orgs?
      *  Could those related organizations have any information on the target?
  *  What vendors/service providers does the target employ?
      *  What goods/services does the target acquire from them?
      *  Who are the points of contact between the target and vendor?

## Things to remember
  *  WHOIS is [old](https://datatracker.ietf.org/doc/html/rfc812) and has [changed a lot](https://datatracker.ietf.org/doc/html/rfc3912)
      *  Hosting services often have their own WHOIS servers
  *  **TONS** of online OSINT resources exist... GTS

## Useful tools
  *  [`theHarvester`](https://github.com/laramies/theHarvester) and [`recon-ng`](https://github.com/lanmaster53/recon-ng) for automatically gathering info from passive sources
  *  [`whois`](https://linux.die.net/man/1/whois) [clients](https://whois.domaintools.com) for gathering domain registration info
  *  [`gitleaks`](https://gitleaks.io/) for finding secrets in code repositories
  *  [`OSINT Framework`](https://osintframework.com/) for **tons** of OSINT resources
  *  [`Social Searcher`](https://www.social-searcher.com/) for searching various social media platforms
  *  [`Netcraft`](https://www.netcraft.com/tools/) for various OSINT analysis
  *  [`Security Headers`](https://securityheaders.com/), [`BuiltWith`](https://builtwith.com), and [`SSL Labs`](https://www.ssllabs.com/ssltest/) for fingerprinting public web services
  *  [`Shodan`](https://www.shodan.io/), [`Censys`](https://censys.com/), and [`WiGLE`](https://wigle.net/) for fingerprinting various public-facing infrastructure
  *  [`Depix`](https://github.com/spipm/Depix) for de-pixelating censored information

## Automatic passive enumeration
  *  `theHarvester` and `recon-ng` for gathering users, e-mails, hosts, etc.
      *  Many info sources will require an API key in order to function
      *  Not all modules/options within these are passive: choose carefully

```
theHarvester -d example.com -b yahoo,duckduckgo
theHarvester -d example.com -b yahoo,duckduckgo -f example.com-harvester
```

```
recon-ng
[recon-ng][default] > workspaces create example
[recon-ng][example] > marketplace search
[recon-ng][example] > marketplace install recon/domains-hosts/hackertarget
[recon-ng][example] > marketplace install recon/hosts-hosts/ssltools
[recon-ng][example] > modules load recon/domains-hosts/hackertarget
[recon-ng][example][hackertarget] > options set SOURCE example.com
[recon-ng][example][hackertarget] > run
[recon-ng][example][hackertarget] > back
[recon-ng][example] > db schema
[recon-ng][example] > db query SELECT host FROM HOSTS
[recon-ng][example] > modules load recon/hosts-hosts/ssltools
[recon-ng][example][ssltools] > options set SOURCE query SELECT host from HOSTS
[recon-ng][example][ssltools] > run
```

## Public websites
  *  Browse the target organizations websites as a normal user
      *  Watch for usernames/name formats, social media accounts, etc.
      *  Search for employee directories/listings
  *  Consider scraping words of interest from public webpages

## WHOIS queries
  *  WHOIS servers provide public domain registration info
      *  Registration/expiration dates, organization/IT staff names, etc.
      *  Query the proper WHOIS server for the most information

```
whois example.com
```

## Google dorking
  *  Use [operators](https://www.googleguide.com/advanced_operators_reference.html) to search for specific resources/patterns
      *  [`GHDB`](https://www.exploit-db.com/google-hacking-database) for various Google dorks

```
site:example.com -site:subdomain.example.com
site:example.com intext:"Employee directory"
site:example.com filetype:txt
```

## Code diving
  *  Search [code hosting sites](https://en.wikipedia.org/wiki/Comparison_of_source-code-hosting_facilities) for sensitive info within publicly readable code
  *  `gitleaks` for automatically detecting secrets in larger codebases
      *  Other tools exist for this and often require configuring tokens/API keys

```
git clone https://github.com/example/example.git && cd example
gitleaks detect -v
gitleaks detect -v -f csv -r /path/to/log.csv
```

## Weak censorship
  *  Certain methods of censorship can be effectively reversed
      *  Search social media for censored images
      *  Search for censored data within any public/stolen documents
  *  Search GitHub for tools to reverse various censorship methods
  *  `Depix` for de-pixelating images of text
