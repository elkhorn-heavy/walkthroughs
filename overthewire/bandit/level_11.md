# OverTheWire - Bandit - Level 11

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to retrieve the next password from the file
`data.txt`, which is `base64` encoded text.

Then use `ssh` to log into the server as the `bandit11` user.

## Commands Used to Solve This Challenge

- `base64`: base64 encode/decode data and print to standard output
- `cat`: concatenate files and print on the standard output
- `ls`: list directory contents
- `ssh`: OpenSSH remote login client

## Initial Analysis

This sounds like it's going to be an easy introduction to using the `base64`
command.

The information from the previous challenge is used to `ssh` into the
server.

## Understanding the Challenge

It appears that the goal is to learn the new command `base64` to decode the
file.

## Approach Strategy

1. Log in using `ssh`
1. Use `ls` to locate `data.txt`
1. Use `base64` to find the password

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit10`. The `ls` command is used to confirm that `data.txt` exists:

```
bandit10@bandit:~$ ls -l
total 4
-rw-r----- 1 bandit11 bandit10 69 Sep 19  2024 data.txt
```

It's a good idea to take a look at the data:

```
bandit10@bandit:~$ cat data.txt
VGhlIHBhc3N3b3JkIGlzIGR0UjE3M2ZaS2IwUlJzREZTR3NnMlJXbnBOVmozcVJyCg==
bandit10@bandit:~$
```

That certainly does look like base 64 encoded data. It consists of only the
letters `a` to `z`, and `A` to `Z`, the digits `0` to `9`, `+` and `/`, with
some `=` characters at the end for padding. The `base64` command is used for
both encoding and decoding, with the `-d` flag used for decoding.

```
bandit10@bandit:~$ base64 -d data.txt
The password is [PASSWORD REMOVED]
bandit10@bandit:~$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit11` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit10@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit11@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit11@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit11@bandit:~$
```

## Key Takeaways

The `base64` command is useful for encoding to the base 64 format, and decoding
from the base 64 format. While this simple example is only encoding text, the
power of base 64 encoding is when used with binary data. Binary data can be
encoded into a string made up of the 64 printable characters (plus `=` for
padding at the end, if needed).

## Beyond the Flag

`base64` is the clear winner when decoding base 64 data. The `basenc` command
can also be used to encode and decode base 64 (among other encodings) but that
might be getting a little ahead of the challenges.

```
bandit10@bandit:~$ basenc --base64 -d data.txt
The password is [PASSWORD REMOVED]
bandit10@bandit:~$
```
