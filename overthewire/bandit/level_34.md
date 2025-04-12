# OverTheWire - Bandit - Level 33

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The description, as of 2025-04-11, says that there is no level 34 _yet_.

## Commands Used to Solve This Challenge

- `ssh`: OpenSSH remote login client

## Initial Analysis

What happens if we do log in as `bandit33`?

## Understanding the Challenge

This challenge is another lesson in how to escape from ... _something_.

## Approach Strategy

1. Log in using `ssh`
1. Poke around

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit33`. Using `ls` to look at the home directory gives:

```
bandit33@bandit:~$ ls -al
total 24
drwxr-xr-x  2 root     root     4096 Apr 10 14:23 .
drwxr-xr-x 70 root     root     4096 Apr 10 14:24 ..
-rw-r--r--  1 root     root      220 Mar 31  2024 .bash_logout
-rw-r--r--  1 root     root     3771 Mar 31  2024 .bashrc
-rw-r--r--  1 root     root      807 Mar 31  2024 .profile
-rw-------  1 bandit33 bandit33  430 Apr 10 14:23 README.txt
bandit33@bandit:~$
```

What's in the `README.txt`?

```
bandit33@bandit:~$ cat README.txt
Congratulations on solving the last level of this game!

At this moment, there are no more levels to play in this game. However, we are constantly working
on new levels and will most likely expand this game with more levels soon.
Keep an eye out for an announcement on our usual communication channels!
In the meantime, you could play some of our other wargames.

If you have an idea for an awesome new level, please let us know!
bandit33@bandit:~$
```
