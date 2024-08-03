# Methodology

*  This file will **NOT** contain details of any one particular service
*  This file serves as more of a general overview of ideas to keep in mind

## Questions to ask yourself
  *  What is the totality of my current access?
  *  What was the view from outside the machine?
      *  How does information from within the machine change that?

## Guesswork
  *  Sometimes an educated guess is required
      *  Keyword **educated**, fully enumerate the machine for words of interest
  *  Consider the names of services/the hostname of the machine
  *  Any word you see during enumeration is a good candidate for guesses
      *  These guesses include usernames, passwords, HTTP URI paths, etc.

## Weak credentials
  *  There is no harm in quick checks for super-weak credentials
  *  Make sure to search for default credentials for all services!
      *  This can include wordlists of sets of default credentials

## Usernames
  *  Find valid usernames and try them everywhere
  *  Spray for weak creds using all usernames
  *  Identify naming conventions across different services
      *  If multiple conventions are found, convert known usernames between them

## Passwords
  *  Spray passwords against all services/usernames
      *  Continue spraying passwords, even if one service yields RCE
  *  Prioritize username enumeration when a stray password is found

## Source code
  *  Any form of code you interact with should be carefully reviewed
      *  Exploits, HTML source, any code found on-target: review all of it

## Vulnerabilities and exploits
  *  Search for vulnerabilites and exploits for **everything**
  *  Any notable fields/parameters in web pages should be noted for later investigation

## Looting
  *  Any file containing information you didn't already know is good loot
      *  This includes all forms of configuration files
