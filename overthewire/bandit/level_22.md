# OverTheWire - Bandit - Level 22

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to find a process that is being run by the
`cron` daemon.

Then use `ssh` to log into the server as the `bandit21` user.

## Commands Used to Solve This Challenge

- `cat`: concatenate files and print on the standard output
- `ls`: list directory contents
- `ssh`: OpenSSH remote login client

## Initial Analysis

This seems fairly straightforward as long as the command being run is obvious.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

The `cron` daemon is used to schedule commands to be run on the server, such as
taking a backup or doing daily restarts of a process. The challenge says that
the `cron` daemon's files can be found in `/etc/cron.d`.

## Approach Strategy

1. Log in using `ssh`
1. Use `ls` to see what is in `/etc/cron.d`
1. Use `cat` to display what is hopefully an obvious file

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit21`. The `ls` command is used to get the contents of `/etc/cron.d`.

```
bandit21@bandit:~$ ls -l /etc/cron.d
total 24
-rw-r--r-- 1 root root 120 Sep 19  2024 cronjob_bandit22
-rw-r--r-- 1 root root 122 Sep 19  2024 cronjob_bandit23
-rw-r--r-- 1 root root 120 Sep 19  2024 cronjob_bandit24
-rw-r--r-- 1 root root 201 Apr  8  2024 e2scrub_all
-rwx------ 1 root root  52 Sep 19  2024 otw-tmp-dir
-rw-r--r-- 1 root root 396 Jan  9  2024 sysstat
bandit21@bandit:~$
```

It's probably not too hard to guess that the cron job is called
`cronjob_bandit22`. Next step is to see what it does:

```
bandit21@bandit:~$ cat /etc/cron.d/cronjob_bandit22
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
bandit21@bandit:~$
```

So this says that when the cron job runs, it runs the command
`/usr/bin/cronjob_bandit22.sh`. The `@reboot` means that the job is run when
the server is rebooted. The `* * * * *` means that the job runs every minute, of
every hour, of every day of the month, of every month of the year, and every
day of the week.

The next step is to see what the command actually does:

```
bandit21@bandit:~$ cat /usr/bin/cronjob_bandit22.sh
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
bandit21@bandit:~$
```

So the script is continuously writing the password to a file with a very hard to
guess name in `/tmp`. Since the filename is known, there is no need to guess:

```
bandit21@bandit:~$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
[REMOVED: BANDIT22 PASSWORD]
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit22` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit21@bandit:~$
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit22@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit22@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit22@bandit:~$
```

## Key Takeaways

The `cron` daemon periodically run commands defined for the server. It is a good
source of information about what the server is doing.

## Beyond the Flag

This one is pretty straightforward and there isn't much else to do.
