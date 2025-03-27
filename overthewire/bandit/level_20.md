# OverTheWire - Bandit - Level 19

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to use a `setuid` binary to get the next password.
No details are given, although the hint is to run the binary without arguments
to get usage information.

Then use `ssh` to log into the server as the `bandit20` user.

## Commands Used to Solve This Challenge

- `cat`: concatenate files and print on the standard output
- `id`: print real and effective user and group IDs
- `ls`: list directory contents
- `ssh`: OpenSSH remote login client

## Initial Analysis

A `setuid` file allow the command to run as the user who _owns_ the file, as
opposed to the usual behaviour of running the command as the user who _runs_ it.
This challenge starts as the `bandit19` user, so it is assumed that the `setuid`
file will be owned by the `bandit20` user - and then that file can read the
password in `/etc/bandit_pass/bandit20`.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

This challenge introduces the concept of a `setuid` file - something that is
powerful but also prone to being dangerous.

## Approach Strategy

1. Log in using `ssh`
1. Use `ls` to find the `setuid` binary
1. Use the `setuid` binary to read the `bandit20` password

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit19`. The `ls` command is used to get information about the `setuid` file:

```
bandit19@bandit:~$ ls -l
total 16
-rwsr-x--- 1 bandit20 bandit19 14880 Sep 19  2024 bandit20-do
bandit19@bandit:~$
```

The file has owner `bandit20` and group `bandit19`. The `s` character in the
first triplet of the permissions shows that it is a `setuid` file. This means
that any who can run the file will run it as the `bandit20` user. However, it is
only runnable by the `bandit20` user (`rws` implies that the third bit for
e`x`ecutable is set) and anyone in the `bandit19` group (the second "group"
triplet of `r-x` says that the file can be `r`ead and e`x`ecuted). As `bandit19`
is in the `bandit20` group, then `bandit19` has `r`ead and e`x`ecute permissions
on the file.

The file is called `bandit20-do`. This could be a play on words for the command
`sudo`, which runs commands as root (the super user). To get usage information
it supposedly can be run without arguments:

```
bandit19@bandit:~$ ./bandit20-do
Run a command as another user.
  Example: ./bandit20-do id
bandit19@bandit:~$
```

It suggests running the `id` command:

```
bandit19@bandit:~$ ./bandit20-do id
uid=11019(bandit19) gid=11019(bandit19) euid=11020(bandit20) groups=11019(bandit19)
bandit19@bandit:~$
```

That confirms that it is a `setuid`, as the effective user ID (`euid`) is that
of `bandit20`. If this file will take _any_ command and run it as `bandit20`,
then it is very powerful / dangerous:

```
bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20
[REMOVED: BANDIT20 PASSWORD]
bandit19@bandit:~$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit20` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit19@bandit:~$
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit20@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit20@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit20@bandit:~$
```

## Key Takeaways

Files with `setuid` permission are powerful, and should be closely examined to
see if they can be use for purposes that they weren't designed.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

Running one command is great, but what about running many? Is it possible to get
a shell running as `bandit20`?

```
bandit19@bandit:~$ ./bandit20-do bash
bash-5.2$ id
uid=11019(bandit19) gid=11019(bandit19) groups=11019(bandit19)
bash-5.2$ exit
exit
bandit19@bandit:~$
```

That didn't work! The `bash` shell has built-in safety features where it won't
run as the effective user if run from a `setuid` binary.

The man page for `bash` says that it has a `-p` switch to preserve the effective
user ID:

```
bandit19@bandit:~$ ./bandit20-do bash -p
bash-5.2$ id
uid=11019(bandit19) gid=11019(bandit19) euid=11020(bandit20) groups=11019(bandit19)
bash-5.2$
```
