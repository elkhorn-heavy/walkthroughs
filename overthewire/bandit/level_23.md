# OverTheWire - Bandit - Level 23

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to find a process that is being run by the
`cron` daemon.

Then use `ssh` to log into the server as the `bandit23` user.

## Commands Used to Solve This Challenge

- `cat`: concatenate files and print on the standard output
- `cut`: remove sections from each line of files
- `ls`: list directory contents
- `md5sum`: compute and check MD5 message digest
- `ssh`: OpenSSH remote login client

## Initial Analysis

This is similar to the last challenge and comes as no surprise after seeing the
contents of `/etc/cron.d`.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

The `cron` daemon is used to schedule commands to be run on the server, such as
taking a backup or doing daily restarts of a process.

## Approach Strategy

1. Log in using `ssh`
1. Use `ls` to see what is in `/etc/cron.d`
1. Use `cat` to display what is hopefully an obvious file

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit22`. The `ls` command is used to get the contents of `/etc/cron.d`.

```
bandit22@bandit:~$ ls -l /etc/cron.d
total 24
-rw-r--r-- 1 root root 120 Sep 19  2024 cronjob_bandit22
-rw-r--r-- 1 root root 122 Sep 19  2024 cronjob_bandit23
-rw-r--r-- 1 root root 120 Sep 19  2024 cronjob_bandit24
-rw-r--r-- 1 root root 201 Apr  8  2024 e2scrub_all
-rwx------ 1 root root  52 Sep 19  2024 otw-tmp-dir
-rw-r--r-- 1 root root 396 Jan  9  2024 sysstat
bandit22@bandit:~$
```

It's probably not too hard to guess that the cron job is called
`cronjob_bandit23`. Next step is to see what it does:

```
bandit22@bandit:~$ cat /etc/cron.d/cronjob_bandit23
@reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
bandit22@bandit:~$
```

So this says that when the cron job runs, it runs the command
`/usr/bin/cronjob_bandit23.sh`. The `@reboot` means that the job is run when
the server is rebooted. The `* * * * *` means that the job runs every minute, of
every hour, of every day of the month, of every month of the year, and every
day of the week. Where it says `bandit23` is the user that the cron job is to
run as.

The next step is to see what the command actually does:

```
bandit22@bandit:~$ cat /usr/bin/cronjob_bandit23.sh
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
bandit22@bandit:~$
```

So the script is continuously writing the password to a file with a very hard to
guess name in `/tmp`. In the previous challenge the filename was a static value
in the shell script. This script is a bit more involved.

This cron job runs as the user `bandit23`, so the commands for the `mytarget`
variable create a message digest (MD) of the string "I am user bandit23":

```
bandit22@bandit:~$ echo I am user bandit23 | md5sum
8ca319486bfbbc3663ea0fbe81326349  -
bandit22@bandit:~$
```

The script follows this by using `cut` to only use part of the output. The `-d`
flag defines the delimiter used to break the file into fields, and `-f` is used
to define which field to keep:

```
bandit22@bandit:~$ echo I am user bandit23 | md5sum | cut -d ' ' -f 1
8ca319486bfbbc3663ea0fbe81326349
bandit22@bandit:~$
```

That means the file should be:

```
bandit22@bandit:~$ cat /tmp/8ca319486bfbbc3663ea0fbe81326349
[REMOVED: BANDIT23 PASSWORD]
bandit22@bandit:~$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit23` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit22@bandit:~$
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit23@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit23@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit23@bandit:~$
```

## Key Takeaways

The `cron` daemon periodically run commands defined for the server. It is a good
source of information about what the server is doing.

## Beyond the Flag

This one is pretty straightforward and there isn't much else to do.
