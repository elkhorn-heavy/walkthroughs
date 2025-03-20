# OverTheWire - Bandit - Level 10

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to look in the file `data.txt` to find one of the
few human readable strings that is preceded with several `=` characters.

Then use `ssh` to log into the server as the `bandit10` user.

## Commands Used to Solve This Challenge

- `grep`: print lines that match patterns
- `ls`: list directory contents
- `ssh`: OpenSSH remote login client
- `strings`: print the sequences of printable characters in files

## Initial Analysis

Going to guess that this file has plenty of unreadable data in it. This
challenge mentions the `strings` command, which will be useful.

The information from the previous challenge is used to `ssh` into the
server.

## Understanding the Challenge

It appears that the goal is to learn the new command `strings` to find readable
data in the file.

## Approach Strategy

1. Log in using `ssh`
1. Use `ls` to locate `data.txt`
1. Use `strings` and `grep` to find the password

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit9`. The `ls` command is used to confirm that `data.txt` exists:

```
bandit9@bandit:~$ ls -l
total 20
-rw-r----- 1 bandit10 bandit9 19379 Sep 19 07:08 data.txt
bandit9@bandit:~$
```

The `strings` command will look for readable strings within a file:

```
bandit9@bandit:~$ strings data.txt
h!]v
r>)1
v0i)b
B:PyZ
#0/u
dyaE
F#X[
7$'0'T
^^^K
Y5}|
...SNIP...
```

There are many, many lines output by `strings`, but at least it's all a little
bit readable. The challenge said to look for several `=` characters, and that is
a job for `grep`:

```
bandit9@bandit:~$ strings data.txt | grep ===
}========== the
3JprD========== passwordi
~fDV3========== is
D9========== [PASSWORD REMOVED]
```

The final line here contains the password.

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit10` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit9@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit10@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit10@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit10@bandit:~$
```

## Key Takeaways

The `strings` command is useful for finding readable data within a binary file.
The `grep` command can then be used if some of the target text is known.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

Reading the man page for `strings`, there is also a way to control the minumum
number of printable characters needed to be considered a string. Knowing that so
far the passwords have all been 32 characters, then the target text must be at
least 32 characters:

```
bandit9@bandit:~$ strings -32 data.txt
D9========== [PASSWORD REMOVED]
bandit9@bandit:~$
```
