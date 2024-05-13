# SSH/22 (TCP)

## Questions to ask yourself
  *  What is the version number?
      *  Unlikely to find an exploit, but `Google` and `searchsploit` anyways 
  *  What forms of authentication will the SSH service accept?
      *  Will it accept an SSH key?
  *  Have read/write over any `.ssh` directories/files? 

## Connecting to [older hosts](https://www.openssh.com/legacy.html)
  *  Take the SSH error output into consideration
      *  `Google` these errors and add config arguments accordingly
  *  Be wary of transferring sensitive data using legacy cipher suites

```
ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no" -o "HostKeyAlgorithms=+ssh-rsa" -o "PubkeyAcceptedAlgorithms=+ssh-rsa" bob@10.0.0.1
ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no" -o "HostKeyAlgorithms=+ssh-rsa" -o "PubkeyAcceptedAlgorithms=+ssh-rsa" -o "KexAlgorithms=+diffie-hellman-group1-sha1" bob@10.0.0.1
```
