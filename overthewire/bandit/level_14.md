# OverTheWire - Bandit - Level 14

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to retrieve the next password from the file
`/etc/bandit_pass/bandit14`. Only the `bandit14` user can read this file, but
the challenge provides an SSH private key to be used.

Then use `ssh` without the key to log into the server as the `bandit14` user
using the password.

## Commands Used to Solve This Challenge

- `cat`: concatenate files and print on the standard output
- `ls`: list directory contents
- `ssh`: OpenSSH remote login client

## Initial Analysis

This challenge gives us a private key for `bandit14`, so ideally it can be used
to `ssh` as that user and then read the key.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

It seems that the goal of this challenge is to introduce the idea of private SSH
keys.

## Approach Strategy

1. Log in using `ssh`
1. Use `ls` to find the private key
1. Use `ssh` to log in as `bandit14`
1. Use `cat` to display the password

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit13`. The `ls` command is used to confirm that the key exists:

```
bandit13@bandit:~$ ls -l
total 4
-rw-r----- 1 bandit14 bandit13 1679 Sep 19  2024 sshkey.private
bandit13@bandit:~$
```

That definitely looks like the file that is needed. The `ssh` man page says that
the `-i` flag is used to specify the private key:

```
bandit13@bandit:~$ ssh -i sshkey.private bandit14@localhost -p 2220
[REMOVED: /etc/issue]
[REMOVED: /etc/motd]
bandit14@bandit:~$
```

It worked! Note that `localhost` is a shortcut to connect to the server the
user is already on. The full server name `bandit.labs.overthewire.org` could
also be used.

```
bandit14@bandit:~$ cat /etc/bandit_pass/bandit14
[PASSWORD REMOVED]
bandit14@bandit:~$
```

To confirm that the password is correct, disconnect from the servers and then
reconnect using the `bandit14` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit14@bandit:~$ exit
logout
Connection to localhost closed.
bandit13@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit14@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit14@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit14@bandit:~$
```

## Key Takeaways

This challenge introduces the very powerful concept of an SSH private key. This
key allows anyone to log into the server as the owner of the key. It's very
important that private keys remain - as the name suggests - private.

## Beyond the Flag

This challenge is fairly simple and using the key to `ssh` to the server is the
obvious answer.
