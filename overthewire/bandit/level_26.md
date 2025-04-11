# OverTheWire - Bandit - Level 25

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

This challenge says that when logged in as `bandit25` it will be easy to log in
as `bandit26`. However, `bandit26` has a non-standard shell, and the difficulty
will be discovering how it works and how to break out of it and retrieve the
password.

Then use `ssh` to log into the server as the `bandit26` user.

## Commands Used to Solve This Challenge

- `cat`: concatenate files and print on the standard output
- `file`: determine file type
- `ls`: list directory contents
- `more`: display the contents of a file in a terminal
- `ssh`: OpenSSH remote login client
- `vim`: Vi IMproved, a programmer's text editor

## Initial Analysis

There is much less "spoon feeding" of the answer as these challenges progress.
This challenge does have some helpful hints, though. One problem will be logging
in as the `bandit26` user. The login command / shell for that user is defined in
`/etc/passwd`. Then the problem will be how to escape from the shell.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

One thing this challenge introduces is the definition of the login command,
typically a shell, that is run when a user logs in.

## Approach Strategy

1. Log in using `ssh`
1. Figure out how to log in as `bandit26`
1. Look at the login command for `bandit26` to figure out how it works, and how
   to escape it.

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit25`. Using `ls` to look at the home directory gives:

```
bandit25@bandit:~$ ls -al
total 40
drwxr-xr-x  2 root     root     4096 Apr 10 14:23 .
drwxr-xr-x 70 root     root     4096 Apr 10 14:24 ..
-rw-r-----  1 bandit25 bandit25   33 Apr 10 14:23 .bandit24.password
-r--------  1 bandit25 bandit25 1679 Apr 10 14:23 bandit26.sshkey
-rw-r-----  1 bandit25 bandit25  151 Apr 10 14:23 .banner
-rw-r--r--  1 root     root      220 Mar 31  2024 .bash_logout
-rw-r--r--  1 root     root     3771 Mar 31  2024 .bashrc
-rw-r-----  1 bandit25 bandit25   66 Apr 10 14:23 .flag
-rw-r-----  1 bandit25 bandit25    4 Apr 10 14:23 .pin
-rw-r--r--  1 root     root      807 Mar 31  2024 .profile
bandit25@bandit:~$
```

The challenge description was right - it appears to be easy to log in as
`bandit26` if `bandit26.sshkey` is the private key for that user:

```
bandit25@bandit:~$ ssh -i bandit26.sshkey bandit26@localhost -p 2220
[REMOVED: /etc/issue]
[REMOVED: /etc/motd]
  _                     _ _ _   ___   __
 | |                   | (_) | |__ \ / /
 | |__   __ _ _ __   __| |_| |_   ) / /_
 | '_ \ / _` | '_ \ / _` | | __| / / '_ \
 | |_) | (_| | | | | (_| | | |_ / /| (_) |
 |_.__/ \__,_|_| |_|\__,_|_|\__|____\___/
Connection to localhost closed.
bandit25@bandit:~$
```

Given that big `bandit26` banner, it's safe to say that the login as `bandit26`
is successful. However, the login command exits immediately and it's back to
being `bandit25`.

The `/etc/passwd` file defines what command is run when a user logs in. For the
current `bandit25` user, the command is:

```
bandit25@bandit:~$ grep bandit25 /etc/passwd
bandit25:x:11025:11025:bandit level 25:/home/bandit25:/bin/bash
bandit25@bandit:~$
```

At the end it says that it's using `/bin/bash` as the shell that the user starts
with, which is fairly normal. What's going on with `bandit26`?

```
bandit25@bandit:~$ grep bandit26 /etc/passwd
bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext
bandit25@bandit:~$
```

The `/usr/bin/showtext` file doesn't seem like it's the name of a shell. To look
into that command:

```
bandit25@bandit:~$ man showtext
No manual entry for showtext
bandit25@bandit:~$ file /usr/bin/showtext
/usr/bin/showtext: POSIX shell script, ASCII text executable
bandit25@bandit:~$
```

There is no `man` page for it, so it's possibly not a standard unix command. The
`file` command shows that it's an ASCII shell script, so that will be easier to
investigate than a binary executable:

```
bandit25@bandit:~$ cat /usr/bin/showtext
#!/bin/sh

export TERM=linux

exec more ~/text.txt
exit 0
bandit25@bandit:~$
```

This is a little bit complicated. The first line of this script says that it
runs using the `/bin/sh` shell. The `exec` command is built into `sh` and
replaces the current process with the `more` command that prints `~/text.txt`
to the user.

The `more` command is a "pager" that allows the user to page through long
documents, so that they don't scroll off the screen. If `~/text.txt` was longer,
then `more` would have stopped when the screen was full, and waited for user
input.

The length of `~/text.txt` can't be made longer to force paging to happen, but
the terminal window can be made _smaller_! Making the terminal window five lines
high gives:

```
bandit25@bandit:~$ ssh -i bandit26.sshkey bandit26@localhost -p 2220
[REMOVED: /etc/issue]
[REMOVED: /etc/motd]
  _                     _ _ _   ___   __
 | |                   | (_) | |__ \ / /
 | |__   __ _ _ __   __| |_| |_   ) / /_
 | '_ \ / _` | '_ \ / _` | | __| / / '_ \
--More--(66%)
```

That forced paging to happen, and now `more` is waiting for input. Pressing the
space bar will print the rest of the file, but then the command will end and
it's back to being `bandit25`. How to stay as `bandit26`?

Pressing the `v` key will open up `vi` to edit the file. Once in the editor, the
trick to opening a shell is to change the shell to something else with
`:set shell=/bin/bash`, followed by `:shell`, which gives:

```
bandit26@bandit:~$ cat /etc/bandit_pass/bandit26
[REMOVED: BANDIT26 PASSWORD]
bandit26@bandit:~$
```

To confirm that the password is correct, disconnect from the servers, including
the `vi` session, and then reconnect using the `bandit26` user and the found
password (`/etc/issue` and `/etc/motd` removed):

```
$ ssh bandit26@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit26@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
  _                     _ _ _   ___   __
 | |                   | (_) | |__ \ / /
 | |__   __ _ _ __   __| |_| |_   ) / /_
 | '_ \ / _` | '_ \ / _` | | __| / / '_ \
 | |_) | (_| | | | | (_| | | |_ / /| (_) |
 |_.__/ \__,_|_| |_|\__,_|_|\__|____\___/
Connection to bandit.labs.overthewire.org closed.
$
```

That's not unexpected - it's still running the same `/usr/bin/showtext` login
command, so this same exploit will be needed to start the next challenge.

## Key Takeaways

The possibility of escaping from a "secure" environment is always something to
look for. While doing an `exec` of a new process seems like it's going to
sandbox the user, the `more` command is a little too powerful to be safe.

## Beyond the Flag

The `vi` command also allows running commands with something like `:!ls`, but in
this case it seems to be locked down. However, there are other things that `vi`
can do, such as including a file into the document using `:r filename`. The
interesting thing here is that it will do filename completion using the `tab`
key, so it's possible to poke around the filesystem somewhat. None of these get
a shell, though - perhaps there is another way?
