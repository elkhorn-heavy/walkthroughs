# OverTheWire - Bandit - Level 5

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to view the only human-readable file in the
`inhere` directory. Then use `ssh` to log into the server as the `bandit5` user.

## Commands Used to Solve This Challenge

- `ssh`: OpenSSH remote login client
- `ls`: list directory contents
- `file`: determine file type
- `cat`: concatenate files and print on the standard output

## Initial Analysis

This challenge looks interesting: what is meant by "human readable", and how can
that be determined? The information from the previous challenge is used to `ssh`
into the server.

## Understanding the Challenge

It appears that the goal is to introduce the `file` command, which is one of the
commands in the hints.

## Approach Strategy

1. Log in using `ssh`
1. Look at the file metadata using `ls`
1. Look at the file types using `file`
1. Use `cat` to display the file

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit4`. To list the files in the directory, the `ls -al` command is used:

```
bandit4@bandit:~$ ls -al inhere/
total 48
drwxr-xr-x 2 root    root    4096 Sep 19 07:08 .
drwxr-xr-x 3 root    root    4096 Sep 19 07:08 ..
-rw-r----- 1 bandit5 bandit4   33 Sep 19 07:08 -file00
-rw-r----- 1 bandit5 bandit4   33 Sep 19 07:08 -file01
-rw-r----- 1 bandit5 bandit4   33 Sep 19 07:08 -file02
-rw-r----- 1 bandit5 bandit4   33 Sep 19 07:08 -file03
-rw-r----- 1 bandit5 bandit4   33 Sep 19 07:08 -file04
-rw-r----- 1 bandit5 bandit4   33 Sep 19 07:08 -file05
-rw-r----- 1 bandit5 bandit4   33 Sep 19 07:08 -file06
-rw-r----- 1 bandit5 bandit4   33 Sep 19 07:08 -file07
-rw-r----- 1 bandit5 bandit4   33 Sep 19 07:08 -file08
-rw-r----- 1 bandit5 bandit4   33 Sep 19 07:08 -file09
bandit4@bandit:~$
```

There's only ten files, so that is good. Now to see if `file` will tell which
file is human-readable.

```
bandit4@bandit:~$ file inhere/*
inhere/-file00: data
inhere/-file01: data
inhere/-file02: data
inhere/-file03: data
inhere/-file04: data
inhere/-file05: data
inhere/-file06: data
inhere/-file07: ASCII text
inhere/-file08: data
inhere/-file09: data
bandit4@bandit:~$
```

One of these things is not like the others. Now to `cat` the file:

```
bandit4@bandit:~$ cat inhere/-file07
[PASSWORD REMOVED]
bandit4@bandit:~$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit5` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit4@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit5@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit5@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit5@bandit:~$
```

## Key Takeaways

This challenge introduces the `file` command, which will often give information
about the type of data in a file.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

One way would be to `cat` every file and see what happens. Since `file` showed
that the other nine files are "data" and not printable ASCII text, they are
going to look like garbage.

```
bandit4@bandit:~$ cat inhere/-file00
�p��&�y�,�(jo�.at�:uf�^���@bandit4@bandit:~$
```

This works, but it's tedious and messy. The `file` command is very helpful in
this case.
