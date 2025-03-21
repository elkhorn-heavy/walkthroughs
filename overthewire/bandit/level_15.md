# OverTheWire - Bandit - Level 12

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to submit the `bandit14` password to port 30000 on
localhost.

Then use `ssh` to log into the server as the `bandit15` user.

## Commands Used to Solve This Challenge

- `telnet`: user interface to the TELNET protocol
- `ssh`: OpenSSH remote login client

## Initial Analysis

The challenge description mentions `telnet` as a command, so that is probably
what is needed to complete the challenge.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

It appears that the goal is to learn the new command `telnet` to connect to a
server.

## Approach Strategy

1. Log in using `ssh`
1. Use `telnet` to submit the current password

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit14`. The `telnet` command is then used to submit the password:

```
bandit14@bandit:~$ telnet localhost 30000
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
[PASSWORD REMOVED]
Correct!
[PASSWORD REMOVED]

Connection closed by foreign host.
bandit14@bandit:~$
```

The second removed password is the one for `bandit15`.

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit15` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit14@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit15@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit15@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit15@bandit:~$
```

## Key Takeaways

The `telnet` command can be used to connect to a server. Since `telnet` does not
use encryption, the data sent and received could be seen by an eavesdropper. For
this reason, `telnet` has mostly been replaced by `ssh` for normal server
connections. For security challenges, however, `telnet` is a useful command to
know.

## Beyond the Flag

The challenge description also mentioned the command `nc`. Could it have been
used instead of `telnet`?

```
bandit14@bandit:~$ nc localhost 30000
[PASSWORD REMOVED]
Correct!
[PASSWORD REMOVED]

^C
bandit14@bandit:~$
```

Note that CTRL-C is used to escape from the `nc` session.
