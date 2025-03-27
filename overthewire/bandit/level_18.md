# OverTheWire - Bandit - Level 18

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to find the line that is different between the
files `passwords.old` and `passwords.new`.

Then use `ssh` to log into the server as the `bandit18` user.

## Commands Used to Solve This Challenge

- `diff`: compare files line by line
- `ls`: list directory contents
- `ssh`: OpenSSH remote login client

## Initial Analysis

If the lines in the file are similar except that the new file has a changed
line, then `diff` will quickly solve the problem.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

It appears that the goal is to learn the new command `diff` to compare files.

## Approach Strategy

1. Log in using `ssh`
1. Use `ls` to locate the files
1. Use `diff` to find the changed line

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit17`. The `ls` command is used to confirm that the password files exist:

```
bandit17@bandit:~$ ls -l
total 8
-rw-r----- 1 bandit18 bandit17 3300 Sep 19  2024 passwords.new
-rw-r----- 1 bandit18 bandit17 3300 Sep 19  2024 passwords.old
bandit17@bandit:~$
```

The two files exist and are both 3300 characters long. Now to try `diff`:

```
bandit17@bandit:~$ diff passwords.old passwords.new
42c42
< ktfgBvpMzWKR5ENj26IbLGSblgUG9CzB
---
> [REMOVED: BANDIT18 PASSWORD]
```

That looks good. The old file is the first parameter, and the new file second.
The output of `diff` says `42c42` meaning that line 42 in the first file is
changed as line 42 in the second file. The `<` indicates the line from the first
file, and the `>` indicates the line from the second file.

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit18` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit17@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit18@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit18@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
Byebye !
Connection to bandit.labs.overthewire.org closed.
```

That's interesting. It said `Byebye !` and then terminated the connection. Not
to worry as the challenge description warned of this behaviour, as it is part of
the next challenge.

## Key Takeaways

The `diff` command is a great way to find differences between files.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

Previously in the `bandit9` challenge the commands `sort` and `uniq` were used.
They can be used here to find the lines that differ:

```
bandit17@bandit:~$ sort passwords.old passwords.new | uniq -u
ktfgBvpMzWKR5ENj26IbLGSblgUG9CzB
[REMOVED: BANDIT18 PASSWORD]
bandit17@bandit:~$
```

Although the password for `bandit18` has been removed above, when the command is
run it isn't obvious which one is the old password and which one is new. The
context that `diff` gives is lost here, but since it's only one password the
`grep` command can be used to check each of them. For the first:

```
bandit17@bandit:~$ grep ktfgBvpMzWKR5ENj26IbLGSblgUG9CzB passwords.new
bandit17@bandit:~$
```

No luck. So it must be the second one:

```
bandit17@bandit:~$ grep [REMOVED: BANDIT18 PASSWORD] passwords.new
[REMOVED: BANDIT18 PASSWORD]
bandit17@bandit:~$
```

Success.
