# OverTheWire - Bandit - Level 7

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to find a file that has very specific attributes:

- owned by user `bandit7`
- having the group `bandit6`
- 33 bytes in size

This file could be anywhere on the server, so under the root (`/`) directory.

Then use `ssh` to log into the server as the `bandit7` user.

## Commands Used to Solve This Challenge

- `cat`: concatenate files and print on the standard output
- `find`: search for files in a directory hierarchy
- `grep`: print lines that match patterns
- `ssh`: OpenSSH remote login client

## Initial Analysis

This would be very hard to do by scanning the thousands of files that are on the
server. The `find` tool used in the previous challenge will be useful. The
description also introduces `grep` as a new command.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

It appears that the goal is to use the `find` command to search the entire
filesystem on the server.

## Approach Strategy

1. Log in using `ssh`
1. Use `find` to locate the file with the matching attributes
1. Use `cat` to display the file

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit6`. The `find` command is used with the desired file attributes:

```
bandit6@bandit:~$ find / -user bandit7 -group bandit6 -size 33c
find: ‘/drifter/drifter14_src/axTLS’: Permission denied
find: ‘/root’: Permission denied
find: ‘/snap’: Permission denied
find: ‘/tmp’: Permission denied
find: ‘/proc/tty/driver’: Permission denied
find: ‘/proc/2087069/task/2087069/fd/6’: No such file or directory
find: ‘/proc/2087069/task/2087069/fdinfo/6’: No such file or directory
find: ‘/proc/2087069/fd/5’: No such file or directory
find: ‘/proc/2087069/fdinfo/5’: No such file or directory
find: ‘/home/bandit31-git’: Permission denied
...SNIP...
```

Over 100 lines have been snipped off the bottom of the output of this command,
as there are many directories and files that this user cannot access.

Good thing this challenge includes the new command `grep`. This command takes
lines of input and selects those that contain a given string. Similarly, it has
a `-v` flag used to remove lines of input that contain a given string. With
shell commands the `|` or "pipe" operator is used to send the output of one
command to the input of another:

```
bandit6@bandit:~$ find / -user bandit7 -group bandit6 -size 33c | grep -v "Permission denied"
find: ‘/drifter/drifter14_src/axTLS’: Permission denied
find: ‘/root’: Permission denied
find: ‘/snap’: Permission denied
find: ‘/tmp’: Permission denied
find: ‘/proc/tty/driver’: Permission denied
find: ‘/proc/2115415/task/2115415/fd/6’: No such file or directory
find: ‘/proc/2115415/task/2115415/fdinfo/6’: No such file or directory
find: ‘/proc/2115415/fd/5’: No such file or directory
find: ‘/proc/2115415/fdinfo/5’: No such file or directory
find: ‘/home/bandit31-git’: Permission denied
...SNIP...
```

Well that didn't work! The catch is that `|` only pipes `stdout` or "standard
output" to the next command. If the first command is writing error messages to
`stderr` or "standard error", then those lines are not passed through the pipe.
The fix is to use `|&`, which will send all `stderr` lines to `stdout`:

```
bandit6@bandit:~$ find / -user bandit7 -group bandit6 -size 33c |& grep -v "Permission denied"
find: ‘/proc/2128719/task/2128719/fd/6’: No such file or directory
find: ‘/proc/2128719/task/2128719/fdinfo/6’: No such file or directory
find: ‘/proc/2128719/fd/5’: No such file or directory
find: ‘/proc/2128719/fdinfo/5’: No such file or directory
/var/lib/dpkg/info/bandit7.password
bandit6@bandit:~$
```

Pretty good! There's the path to the file as the last line. However, there are
still some error lines in the output. To remove these, the output of `grep` can
be piped into another `grep` command:

```
bandit6@bandit$ find / -user bandit7 -group bandit6 -size 33c |& grep -v "Permission denied" | grep -v "No such file or directory"
/var/lib/dpkg/info/bandit7.password
bandit6@bandit:~$ cat /var/lib/dpkg/info/bandit7.password
[REMOVED: BANDIT7 PASSWORD]
bandit6@bandit:~$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit7` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit6@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit7@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit7@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit7@bandit:~$
```

## Key Takeaways

This challenge uses the `find` command again, but introduces `grep` to filter
out error messages to make it easier to find the one file that is needed.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

The `grep` command was introduced for this challenge, but what if it wasn't
available? One approach would be to send the `stderr` output from the find
command to `/dev/null`, which is a special file that consumes anything sent to
it (aka "the bit bucket"). This is done using `2> /dev/null`, which says that
all output from file descriptor 2 (aka, `stderr`) gets sent to `/dev/null`,
which then throws it away.

```
bandit6@bandit:~$ find / -user bandit7 -group bandit6 -size 33c 2> /dev/null
/var/lib/dpkg/info/bandit7.password
bandit6@bandit:~$
```
