# NFS/111/2049 (TCP)

## Questions to ask yourself
  *  What are my permissions?
      *  Directories/files of interest, can we read/write them?
      *  Gaining creds means gaining permissions, check back in later
  *  Where does this FTP directory exist on the filesystem?
      *  Does it overlap with another service?
      *  `Google` names of interesting directories and files

## Things to remember
  *  Always use `ls -la` to list hidden files/dirs
  *  Check all files for sensitive information
  *  Watch for `no_root_squash` in config files, easy privesc

## Useful tools
  *  [`nmap`](https://nmap.org/) for various NSE enum scripts
  *  [`showmount`](https://linux.die.net/man/8/showmount)/[`mount`](https://linux.die.net/man/8/mount) commands to interact with NFS services
  *  [`exiftool`](https://exiftool.org/) for extracting metadata from any readable files

## Additional NSE enumeration
  *  `nmap` has a few [NFS recon scripts](https://nmap.org/search/?q=nfs)
      *  Gather NFS version information from [`rpcbind`](https://nmap.org/nsedoc/scripts/rpcinfo.html) service

```
nmap -sS -p 111 -T4 -sC --script "nfs*" -vv 10.0.0.1
nmap -sS -p 111 -T4 -sC --script=rpcinfo -vv 10.0.0.1
```

## Mounting NFS
  *  `showmount` command to list exports of an NFS server
  *  `mount` command to create a mount point for an NFS share
      *  Mounting through a pivot requires port forwarding

```
showmount -e 10.0.0.1
```

```
mkdir /tmp/mount
sudo mount -t nfs 10.0.0.1:/path/to/share /tmp/mount/ -nolock
sudo mount -o nolock 10.0.0.1:/path/to/share /tmp/mount/
sudo mount -v -t nfs -o port=3049,tcp,nolock 127.0.0.1:/path/to/share /tmp/mount
sudo umount /tmp/mount && rm -r /tmp/mount
```

## Manual `no_root_squash` check
  *  Perform a manual check for `no_root_squash`
      *  Mount the share as normal and create a new file as root
      *  Root squash is enabled if the file owner has been changed

## Extract metadata from files
  *  `exiftool` for extracting metadata from readable files
  *  Metadata can contain a plethora of information!

```
exiftool example.xlsx
exiftool -a -u example.pdf
```

## UID spoofing
  *  NFS was originally designed to [rely on the operating system](https://datatracker.ietf.org/doc/html/rfc1094#section-3.3) for [UNIX style authentication](https://nvlpubs.nist.gov/nistpubs/Legacy/FIPS/fipspub151-1.pdf) ([UIDs/GIDs](https://man7.org/linux/man-pages/man7/credentials.7.html))
      *  Newer protocols are supported, but this behavior still occurs by default
      *  Gather UIDs of file owners from exported NFS shares
      *  Create a local user with a matching UID and re-mount the share

```
ls -an
sudo useradd -u [TARGET UID] -s /bin/bash -p $(echo 'password' | openssl passwd -stdin) bob
```

## NFS config information
  *  Find more exported NFS shares from [config files](https://book.hacktricks.xyz/network-services-pentesting/nfs-service-pentesting#config-files)

```
cat /etc/exports
cat /etc/default/nfs*
```
