# OverTheWire - Bandit - Level 16

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to submit the `bandit15` password to port 30001 on
localhost using TLS.

Then use `ssh` to log into the server as the `bandit16` user.

## Commands Used to Solve This Challenge

- `openssl`: OpenSSL command line program
- `ssh`: OpenSSH remote login client

## Initial Analysis

This challenge says to use the Transport Layer Security (TLS) protocol to
connect to the server. It also mentions `openssl` as a command, so that is a
good place to start. The Secure Socket Layer (SSL) protocol preceded TLS, but
many people and tools still refer to TLS as SSL.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

It appears that the goal is to learn the new command `openssl` to connect to a
server.

## Approach Strategy

1. Log in using `ssh`
1. Use `openssl` to submit the current password

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit15`. The `openssl` command will be used with its `s_client` command to
connect to the server. The `-quiet` flag removes a large amount of output.

```
bandit15@bandit:~$ openssl s_client -quiet localhost:30001
Can't use SSL_get_servername
depth=0 CN = SnakeOil
verify error:num=18:self-signed certificate
verify return:1
depth=0 CN = SnakeOil
verify return:1
[REMOVED: BANDIT15 PASSWORD]
Correct!
[REMOVED: BANDIT16 PASSWORD]

bandit15@bandit:~$
```

The output starts with some complaints about the server using a self-signed
server TLS certificate - this can be ignored. It then waits for user input,
where the password for `bandit15` is entered. The server responds with
`Correct!` and the `bandit16` password.

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit16` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit15@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit16@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit16@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit16@bandit:~$
```

## Key Takeaways

The `s_client` command for `openssl` can be used to make TLS connections to
servers. It can be thought of as the encrypted version of `telnet`, or as `ssh`
without authentication.

## Beyond the Flag

As a hint this challenge links to Ivan Ristić's excellent
[OpenSSL Cookbook](https://www.feistyduck.com/library/openssl-cookbook/online/).
This online book is an accessible but in-depth resource for anyone wanting to
learn more about the SSL/TLS protocol.
