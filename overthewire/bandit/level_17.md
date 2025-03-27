# OverTheWire - Bandit - Level 17

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to submit the `bandit16` password to localhost
using TLS. The port is somewhere from 31000 to 32000, and will respond with the
`bandit17` credentials. All other ports will respond with whatever is sent. One
of the recommended commands mentioned is `ss`, but `netstat` and `nmap` are also
mentioned.

Then use `ssh` to log into the server as the `bandit17` user.

## Commands Used to Solve This Challenge

- `netstat`: Print network connections, routing tables, interface statistics,
  masquerade connections, and multicast memberships
- `nmap`: Network exploration tool and security / port scanner
- `openssl`: OpenSSL command line program
- `ss`: another utility to investigate sockets
- `ssh`: OpenSSH remote login client

## Initial Analysis

This challenge says that the port is somewhere from 31000 to 32000, which is a
lot of ports to try manually. Since `bandit16` has local access to the server, a
tool like `ss` can be used to find the port (if local access was not available,
then something like `nmap` could be used).

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

This is very similar to the previous challenge except that the port number is
unknown.

## Approach Strategy

1. Log in using `ssh`
1. Use `ss` to look for listening ports
1. Use `openssl` to submit the current password

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit16`.

The `ss` command shows information on network "sockets" that are available on a
server. The `-l` flag lists only sockets that a process uses to "listen" for
connections. The `-t` flag lists only "TCP" sockets. A `grep` is used to limit
the ports to those starting with "31", even though that will exclude 32000:

```
bandit16@bandit:~$ ss -lt | grep :31
LISTEN 0      4096         0.0.0.0:31790       0.0.0.0:*
LISTEN 0      4096         0.0.0.0:31518       0.0.0.0:*
LISTEN 0      64                 *:31960             *:*
LISTEN 0      64                 *:31691             *:*
LISTEN 0      64                 *:31046             *:*
```

That's great news - checking five ports will be much easier than checking
10,001. Since there's five, it's probably faster to just connect to each one:

```
bandit16@bandit:~$ openssl s_client -quiet localhost:31790
Can't use SSL_get_servername
depth=0 CN = SnakeOil
verify error:num=18:self-signed certificate
verify return:1
depth=0 CN = SnakeOil
verify return:1
[REMOVED: BANDIT16 PASSWORD]
Correct!
-----BEGIN RSA PRIVATE KEY-----
[REMOVED: BANDIT17 PRIVATE KEY]
-----END RSA PRIVATE KEY-----
```

A lucky first guess! The output starts with some complaints about the server
using a self-signed server TLS certificate - this can be ignored. It then waits
for user input, where the password for `bandit16` is entered. The server
responds with `Correct!` and the private key for `bandit17`.

With `ssh` the `-i` flag is used to specify the private key, but that key needs
to be in a file. The `mktemp` command can be used to create a file with a random
name, and then the `vi` command is used to paste in the key:

```
bandit16@bandit:~$ mktemp
/tmp/tmp.WkFMd3GKHc
bandit16@bandit:~$ vi /tmp/tmp.WkFMd3GKHc
```

Learrning `vi` is left as an exercise for the reader, haha. Now to use the
private key to log in as `bandit17`:

```
bandit16@bandit:~$ ssh -i /tmp/tmp.WkFMd3GKHc bandit17@localhost -p2220
[REMOVED: /etc/issue]
[REMOVED: /etc/motd]
bandit17@bandit:~$
```

It worked! Note that `localhost` is a shortcut to connect to the server the
user is already on. The full server name `bandit.labs.overthewire.org` could
also be used.

```
bandit17@bandit:~$ cat /etc/bandit_pass/bandit17
[REMOVED: BANDIT17 PASSWORD]
bandit17@bandit:~$
```

To confirm that the password is correct, disconnect from the servers and then
reconnect using the `bandit17` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit17@bandit:~$ exit
logout
Connection to localhost closed.
bandit16@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit17@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit17@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit17@bandit:~$
```

## Key Takeaways

The `ss` command is an important tool for discovering information about the
networking on a server.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

### Using `netstat`

One of the suggested commands for this challenge is `netstat`. This command is
the predecessor to `ss`, and on some systems may be the only command available.
To repeat the search for listening ports, the `-l` flag is used, and the `-t`
flag again limits the results to TCP ports:

```
bandit16@bandit:~$ netstat -lt | grep :31
netstat: no support for `AF INET (tcp)' on this system.
tcp6       0      0 [::]:31960              [::]:*                  LISTEN
tcp6       0      0 [::]:31691              [::]:*                  LISTEN
tcp6       0      0 [::]:31046              [::]:*                  LISTEN
```

Interesting! The `ss` command showed five ports, but netstat is only showing
three, and is producing an error. The first column shows that these are all IPv6
ports. The `-6` flag for `netstat` limits results to IPv6 ports:

```
bandit16@bandit:~$ netstat -lt6 | grep :31
tcp6       0      0 [::]:31960              [::]:*                  LISTEN
tcp6       0      0 [::]:31691              [::]:*                  LISTEN
tcp6       0      0 [::]:31046              [::]:*                  LISTEN
bandit16@bandit
```

As expected, those are the same three ports from before. The `-4` flag limits
results to IPv4 ports:

```
bandit16@bandit:~$ netstat -lt4 | grep :31
netstat: no support for `AF INET (tcp)' on this system.
bandit16@bandit:~$
```

Interesting! The short explanation is that `netstat` uses filesystem-based
resources and the IPv4 resource is not readable by `bandit17`:

```
bandit16@bandit:~$ ls -l /proc/net/tcp
-r-------- 1 root root 0 Mar 27 10:58 /proc/net/tcp
bandit16@bandit:~$
```

The `ss` command sees the IPv4 ports because instead of `/proc/net/tcp` it
directly calls the kernel's networking subsystem.

### Using `nmap`

Another suggested command for this challenge is `nmap`. This command is similar
to `ss` and `netstat` except that instead of querying the local server, `nmap`
is used against remote servers. This means that `nmap` has to actually open
connections to the remote server to find open ports. The `-p` flag is used to
specify a port range to scan. A quick scan shows:

```
bandit16@bandit:~$ nmap -p31000-32000 localhost
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-27 11:11 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00018s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT      STATE SERVICE
31046/tcp open  unknown
31518/tcp open  unknown
31691/tcp open  unknown
31790/tcp open  unknown
31960/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 0.19 seconds
bandit16@bandit:~$
```

This scan completed quickly and returned the same results as using `ss`. `nmap`
has a lot more features, though, and the `-sV` flag will try to determine which
services are running, and if possible their versions - but it takes longer:

```
bandit16@bandit:~$ nmap -p31000-32000 -sV localhost
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-27 11:13 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0011s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT      STATE SERVICE     VERSION
31046/tcp open  echo
31518/tcp open  ssl/echo
31691/tcp open  echo
31790/tcp open  ssl/unknown
31960/tcp open  echo
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port31790-TCP:V=7.94SVN%T=SSL%I=7%D=3/27%Time=67E532CF%P=x86_64-pc-linu
SF:x-gnu%r(GenericLines,32,"Wrong!\x20Please\x20enter\x20the\x20correct\x2
SF:0current\x20password\.\n")%r(GetRequest,32,"Wrong!\x20Please\x20enter\x
SF:20the\x20correct\x20current\x20password\.\n")%r(HTTPOptions,32,"Wrong!\
SF:x20Please\x20enter\x20the\x20correct\x20current\x20password\.\n")%r(RTS
SF:PRequest,32,"Wrong!\x20Please\x20enter\x20the\x20correct\x20current\x20
SF:password\.\n")%r(Help,32,"Wrong!\x20Please\x20enter\x20the\x20correct\x
SF:20current\x20password\.\n")%r(FourOhFourRequest,32,"Wrong!\x20Please\x2
SF:0enter\x20the\x20correct\x20current\x20password\.\n")%r(LPDString,32,"W
SF:rong!\x20Please\x20enter\x20the\x20correct\x20current\x20password\.\n")
SF:%r(SIPOptions,32,"Wrong!\x20Please\x20enter\x20the\x20correct\x20curren
SF:t\x20password\.\n");

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 159.73 seconds
bandit16@bandit:~$
```

Although this scan took much longer, it identified that four of the ports are
running the `echo` service. The challenge description said that one service
would return the `bandit17` credentials but the others would return whatever
input was sent to them. So `nmap` has identified that `31790` is the port to
use.
