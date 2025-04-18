# OverTheWire - Bandit - Level 27

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

This challenge says that when logged in as `bandit26` it's time to grab the
password for `bandit27`.

Then use `ssh` to log into the server as the `bandit27` user.

## Commands Used to Solve This Challenge

- `ls`: list directory contents
- `ssh`: OpenSSH remote login client

## Initial Analysis

This one doesn't have many clues other than `ls` being the only command that is
suggested.

The information from the previous challenge is used to `ssh` into the server,
including the complicated escape from `more` to `vi` to a shell.

## Understanding the Challenge

This challenge seems to be a repeat of level 20 - perhaps as an easy way to wrap
up the complicated exploit in the previous level.

## Approach Strategy

1. Make the screen small to cause `more` to page the output
1. Log in using `ssh`
1. Escape from `more` into `vi`
1. Escape from `vi` into a shell
1. Figure out how to get the `bandit27` password

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit26`. A small terminal five lines high is used to force the `exec`ed login
script to page using `more`. Once `more` is waiting for input, the `v` key will
open the file in `vi`. Then the commands `:set shell=/bin/bash` and `:shell` are
used to escape into a shell. Using `ls` to look at the home directory gives:

```
bandit26@bandit:~$ ls -al
total 44
drwxr-xr-x  3 root     root      4096 Apr 10 14:23 .
drwxr-xr-x 70 root     root      4096 Apr 10 14:24 ..
-rwsr-x---  1 bandit27 bandit26 14884 Apr 10 14:23 bandit27-do
-rw-r--r--  1 root     root       220 Mar 31  2024 .bash_logout
-rw-r--r--  1 root     root      3771 Mar 31  2024 .bashrc
-rw-r--r--  1 root     root       807 Mar 31  2024 .profile
drwxr-xr-x  2 root     root      4096 Apr 10 14:23 .ssh
-rw-r-----  1 bandit26 bandit26   258 Apr 10 14:23 text.txt
bandit26@bandit:~$
```

That `setuid` file called `bandit27-do` looks similar to the `sudo`-like binary
that was found in level 20.

```
bandit26@bandit:~$ ./bandit27-do cat /etc/bandit_pass/bandit27
[REMOVED: BANDIT27 PASSWORD]
bandit26@bandit:~$
```

To confirm that the password is correct, disconnect from the servers, including
the `vi` session, and then reconnect using the `bandit27` user and the found
password (`/etc/issue` and `/etc/motd` removed):

```
$ ssh bandit27@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit27@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit27@bandit:~$
```

## Key Takeaways

This challenge re-uses the `setuid` binary concept in level 20 to wrap up the
previous complicated exploit. Not too much is new here.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

Similar to level 20, it would be nice to get a shell as `bandit27`. Using the
`-p` switch to preserve the effective user ID:

```
bandit26@bandit:~$ ./bandit27-do bash -p
bash-5.2$ id
uid=11026(bandit26) gid=11026(bandit26) euid=11027(bandit27) groups=11026(bandit26)
bash-5.2$
```
