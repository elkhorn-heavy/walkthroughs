# OverTheWire - Bandit - Level 33

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

This challenge says that it's time to move on from `git`, and that this
challenge is another escape. That is really vague, but somehow the password for
`bandit33` will be found.

Then use `ssh` to log into the server as the `bandit33` user.

## Commands Used to Solve This Challenge

- `man`: an interface to the system reference manuals
- `sh`: command interpreter (shell)
- `ssh`: OpenSSH remote login client

## Initial Analysis

Hard to say what this is going to be.

## Understanding the Challenge

This challenge is another lesson in how to escape from ... _something_.

## Approach Strategy

1. Log in using `ssh`
1. Figure out what is going on
1. Find the `bandit33` password

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit32`:

```
$ ssh bandit32@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit32@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
WELCOME TO THE UPPERCASE SHELL
>>
```

This is interesting! What is the "uppercase shell"? First get a directory
listing of the user's home directory:

```
>> ls
sh: 1: LS: Permission denied
>>
```

Huh! So whatever is typed in is translated to uppercase, then it is executed? It
also doesn't do filename completion using the TAB character, so that is not an
option.

As a bit of a cheat perhaps, start a new session using an old user and password
and see what the `bandit32` shell is:

```
bandit31@bandit:~$ grep bandit32 /etc/passwd
bandit32:x:11032:11032:bandit level 32:/home/bandit32:/home/bandit32/uppershell
bandit31@bandit:~$ cat /home/bandit32/uppershell
cat: /home/bandit32/uppershell: Permission denied
bandit31@bandit:~$ ls -al /home/bandit32/uppershell
-rwsr-x--- 1 bandit33 bandit32 15140 Apr 10 14:23 /home/bandit32/uppershell
bandit31@bandit:~$
```

So it's running a custom command in the `bandit32` home directory as the login
shell. The file is only readable by the `bandit33` user and those in the
`bandit32` group, which is only the `bandit32` user. So there is no way of
looking at the login shell file now.

Interestingly, the login shell file is owned by `bandit33` and is `setuid`, so
when run by any user it can read any file readable by `bandit33`. So this shell
can read the password in `/etc/bandit_pass/bandit33`.

Switching back to the `bandit32` user running the uppercase shell:

```
>> cat /etc/bandit_pass/bandit33
sh: 1: CAT: Permission denied
>>
```

Again the uppercasing gets in the way. The vast majority of unix commands are
lowercase, so there aren't any uppercase commands that will work. What about
commands that are neither lowercase nor uppercase? Input redirection using the
`<` will print a file:

```
>> < /etc/bandit_pass/bandit33
>> sh: 1: cannot open /ETC/BANDIT_PASS/BANDIT33: No such file
>>
```

So input redirection seems to be working, but it's also uppercasing the
filename. Perhaps wildcards are the answer here:

```
>> < /*/*/*33
>> sh: 1: cannot open /*/*/*33: No such file
```

Either it isn't allowing wildcards or perhaps it is expanding to too many files?
The `?` character matches a single character, so `/etc/bandit_pass/bandit33`
would be:

```
>> < /???/??????_????/??????33
>> sh: 1: cannot open /???/??????_????/??????33: No such file
```

Still no luck, so maybe `?` isn't allowed as a wildcard character in this shell.
What about:

```
>> $PATH
>> sh: 1: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin: not found
```

Aha! So the contents of an environment variable can be printed by using the
error message that happens. Looking at `$SHELL`:

```
>> $SHELL
WELCOME TO THE UPPERCASE SHELL
>>
```

That is not what expected: instead of printing the value of the `SHELL`
environment variable, it is actually running the shell. This could also be
useful! What about setting the `SHELL` variable and then executing it:

```
>> SHELL=/bin/bash
>> $SHELL
WELCOME TO THE UPPERCASE SHELL
>>
```

Oh no, that didn't work. Stumped.

Looking at the challenge description again, it says that the commands needed are
`man` and `sh`. Doing a deep read of the `sh` man page gives a lot of
information, including that `$0` is the current shell. Can it be that easy?

```
>> $0
$
```

And there it is, dropped into a shell. Does it work?

```
$ cat /etc/bandit_pass/bandit33
[REMOVED: BANDIT33 PASSWORD]
$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit33` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
$ exit
>>
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit33@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit33@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit33@bandit:~$
```

## Key Takeaways

The key to this challenge is that `$0` can be used to start up the shell.

## Beyond the Flag

Perhaps there are other solutions to this one, it's a bit tricky.
