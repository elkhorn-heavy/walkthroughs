# OverTheWire - Bandit - Level 2

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to view the file named `-` to get the password for
level 2. Then use `ssh` to log into the server as the `bandit2` user.

## Commands Used to Solve This Challenge

- `ssh`: OpenSSH remote login client
- `ls`: list directory contents
- `cat`: concatenate files and print on the standard output

## Initial Analysis

This challenge provides all the information needed: the password is in the file
called `-`. The information from the previous challenge is used to `ssh` into
the server.

The difficulty will be that the `-` character is used as a prefix for command
flags, and is also used to indicate "standard input" (stdin) for commands.

## Understanding the Challenge

It appears that the goal is to teach how to view files with strange names.

## Approach Strategy

1. Log in using `ssh`
1. Find the file using `ls`
1. Use `cat` to display the file

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit1`:

```
bandit1@bandit:~$
```

To list the files in the directory, the `ls` command is used:

```
bandit1@bandit:~$ ls -al
total 24
-rw-r-----  1 bandit2 bandit1   33 Sep 19 07:08 -
drwxr-xr-x  2 root    root    4096 Sep 19 07:08 .
drwxr-xr-x 70 root    root    4096 Sep 19 07:09 ..
-rw-r--r--  1 root    root     220 Mar 31  2024 .bash_logout
-rw-r--r--  1 root    root    3771 Mar 31  2024 .bashrc
-rw-r--r--  1 root    root     807 Mar 31  2024 .profile
bandit1@bandit:~$
```

Yes indeed, there is a 33 byte file called `-` in bandit1's home directory. The
technique in the previous challenge was to `cat` the file:

```
bandit1@bandit:~$ cat -

```

Oh no - it's hung! The `-` has a special meaning of `stdin` or standard input.
The `cat` command, instead of printing the file, is waiting on input from the
user. This is never going to happen, so CTRL-C is used to break out of it:

```
bandit1@bandit:~$ cat -
^C
bandit1@bandit:~$
```

To `cat` the file with this special filename, we can include more of the path to
the file. In unix `.` represents the current directory, so `./-` is the same as
saying `-`.

```
bandit1@bandit:~$ cat ./-
[PASSWORD REMOVED]
bandit1@bandit:~$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit2` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit1@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit2@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit2@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit2@bandit:~$
```

## Key Takeaways

This challenge teaches that files named `-` are tricky to work with. This is
also true for files starting with a `-`, such as `-f`. They are also a little
too easy to accidentally create!

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

Other variations on the solution could be used, such as using the shortcut `~`
for the current directory:

```
bandit1@bandit:~$ cat ~/-
[PASSWORD REMOVED]
bandit1@bandit:~$
```

Similarly, the full path to the file could be used:

```
bandit1@bandit:~$ cat /home/bandit1/-
[PASSWORD REMOVED]
bandit1@bandit:~$
```
