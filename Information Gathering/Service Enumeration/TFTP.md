# TFTP/69 (UDP)

## Questions to ask yourself
  *  Where does the TFTP chroot exist on the filesystem?
      *  Does it overlap with another service?
  *  What are my permissions?
      *  Directories/files of interest, can we read/write them?

## Things to remember:
  *  [TFTP](https://en.wikipedia.org/wiki/Trivial_File_Transfer_Protocol) is primarily used to [deliver boot images](https://en.wikipedia.org/wiki/Preboot_Execution_Environment)
  *  TFTP services from [different](https://git.kernel.org/pub/scm/network/tftp/tftp-hpa.git/tree/tftpd) [developers](https://www.solarwinds.com/free-tools/free-tftp-server) have different permissions philosophies
      *  R/W privs may be that of a public user (very low) or the TFTP service itself (potentially high)
      *  Identify and research TFTP service version or manually check for R/W permissions
  *  TFTP provides [no authentication nor directory listing](https://datatracker.ietf.org/doc/html/rfc1350#section-1)
      *  Bruteforce or infer the location of files of interest

## Useful tools
  *  [`nmap`](https://nmap.org/) for various NSE enum scripts
  *  [`tftp-hpa`](https://linux.die.net/man/1/ftp) client for basic TFTP interactions
  *  [`tftpy`](https://pypi.org/project/tftpy/) for more control over TFTP transfer

## Additional NSE enumeration
  *  `nmap` has a couple of [TFTP recon/bruteforce scripts](https://nmap.org/search/?q=tftp)
      *  Research popular TFTP services for the target OS when `tftp-version` fails
      *  If a scan errors, use debug (`-d`) and run it again

```
nmap -sU -p69 -T4 --script="tftp-version" -sV -vv 10.0.0.1
nmap -sU -p69 -T4 --script="tftp-enum" -sV -vv 10.0.0.1
nmap -sU -p69 -T4 --script="tftp-enum" --script-args tftp-enum.filelist=/path/to/filenames.txt -sV -vv 10.0.0.1
```

## TFTP help list
  *  List available `tftp-hpa` client commands (not many)

```
tftp 10.0.0.1
tftp> help
```

## Python TFTP transfer
  *  `tftpy` for transferring files with specific filepaths

```
import tftpy
client = tftpy.TftpClient("10.0.0.1", 69)
client.download("/path/to/remote/file.txt", "/path/to/local/file.txt", timeout=5)
client.upload("/path/to/remote/file.txt", "/path/to/local/file.txt", timeout=5)
```

## Extract metadata from files
  *  `exiftool` for extracting metadata from readable files
  *  Metadata can contain a plethora of information!

```
exiftool example.xlsx
exiftool -a -u example.pdf
```
