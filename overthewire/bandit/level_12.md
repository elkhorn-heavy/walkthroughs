# OverTheWire - Bandit - Level 12

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to retrieve the next password from the file
`data.txt`. The lowercase and uppercase letters in this file have been rotated
by 13 positions.

Then use `ssh` to log into the server as the `bandit12` user.

## Commands Used to Solve This Challenge

- `cat`: concatenate files and print on the standard output
- `ls`: list directory contents
- `ssh`: OpenSSH remote login client
- `tr`: translate or delete characters

## Initial Analysis

This sounds like it's a ROT13 encoded file. This encoding is used to hide text
from being readable but at the same time be easily decoded. For example, a joke
and a ROT13 encoded punchline could be posted and the reader could decode the
punchline when desired. Since the alphabet has 26 characters, rotating by half
(13) those characters encodes the plaintext, and rotating another 13 characters
gets everything back to the plaintext.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

It appears that the goal is to learn the new command `tr` to implement the ROT13
function.

## Approach Strategy

1. Log in using `ssh`
1. Use `ls` to locate `data.txt`
1. Use `tr` to decode the file and find the password

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit11`. The `ls` command is used to confirm that `data.txt` exists:

```
bandit11@bandit:~$ ls -l
total 4
-rw-r----- 1 bandit12 bandit11 49 Sep 19  2024 data.txt
bandit11@bandit:~$
```

It's a good idea to take a look at the data.

```
bandit11@bandit:~$ cat data.txt
Gur cnffjbeq vf 7k16JArUVv5LxVuJfsSVdbbtaHGlw9D4
bandit11@bandit:~$
```

Spaces are not encoded, so the plaintext here will be four separate words and
the first three are easy to guess. Since we know it's ROT13 encoded, we don't
have to think too hard, though.

The `tr` command translates one set of characters into another set. For example,
to translate all `a` and `b` characters to `A` and `B`, the command is

```
$ tr ab AB
```

For ROT13, `a` is replaced by `n`, `b` by `o`, etc. To make this clear, the
one command could be:

```
bandit11@bandit:~$ cat data.txt | tr abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM
The password is [PASSWORD REMOVED]
bandit11@bandit:~$
```

That's quite the command to type out. Thankfully `tr` allows shortcuts, so that
`abcdef` can be replaced by `a-f`:

```
bandit11@bandit:~$ cat data.txt | tr a-zA-Z n-za-mN-ZA-M
The password is [PASSWORD REMOVED]
bandit11@bandit:~$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit12` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit11@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit11@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit12@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit12@bandit:~$
```

## Key Takeaways

The `tr` command is a useful tool when manipulating data. Not only can it be
used to change characters in a file, but it can be used to remove characters
too.

## Beyond the Flag

The `tr` command does a great job of handling ROT13. The `sed` (stream editor)
command could also be used, as could a general purpose programming language,
such as Python. `tr` is definitely the quick win, though.
