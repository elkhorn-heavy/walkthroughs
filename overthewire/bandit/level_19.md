# OverTheWire - Bandit - Level 19

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge get the password out of the `readme` file. The
difficulty is that the `.bashrc` file automatically logs out the user when they
log in.

Then use `ssh` to log into the server as the `bandit19` user.

## Commands Used to Solve This Challenge

- `bash`: GNU Bourne-Again SHell
- `cat`: concatenate files and print on the standard output
- `ssh`: OpenSSH remote login client

## Initial Analysis

Since the `.bashrc` file prevents the user from logging in, the secret must be
to find a way to bypass the `.bashrc` file. Perhaps `ssh` has something that
helps with this task.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

It appears that the goal is to learn more about the command `ssh`.

## Approach Strategy

1. Use `ssh` to log in without reading the `.bashrc` file

## Step-by-Step Solution

In the previous challenge using `ssh` to log in as user `bandit18` resulted in
an automatic logout:

```
$ ssh bandit18@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit18@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
Byebye !
Connection to bandit.labs.overthewire.org closed.
$
```

This makes things difficult - but not impossible. The `ssh` command allows a
command line parameter that is the command to run after connecting. Since this
is run instead of the default shell, it can be used to get around the
limitation.

```
$ ssh bandit18@bandit.labs.overthewire.org -p 2220 bash
[REMOVED: /etc/issue]
bandit18@bandit.labs.overthewire.org's password:
```

Oh boy - the connection is hung! Looks like that's not going to work. It looks
like `bash` is expecting a terminal when it runs, but isn't finding one. That's
why `ssh` has a `-t` flag to create a pseudo-terminal:

```
$ ssh -t bandit18@bandit.labs.overthewire.org -p 2220 bash
[REMOVED: /etc/issue]
bandit18@bandit.labs.overthewire.org's password:
Byebye !
Connection to bandit.labs.overthewire.org closed.
$
```

Progress! So this is the original behaviour, except that now the `bash` command
being run can be controlled. `bash` has a `--norc` flag to not run the `.bashrc`
file on login:

```
$ ssh -t bandit18@bandit.labs.overthewire.org -p 2220 bash --norc
[REMOVED: /etc/issue]
bandit18@bandit.labs.overthewire.org's password:
bash-5.2$
```

There it is. Note that the prompt is different - it doesn't contain the
username, hostname, or the working directory. That's because it's using the
default `bash` prompt, not the one set in the `.bashrc` file.

Now to `cat` the `readme` file containing the password for `bandit19`:

```
bash-5.2$ cat readme
[REMOVED: BANDIT19 PASSWORD]
bash-5.2$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit19` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bash-5.2$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit19@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit19@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit19@bandit:~$
```

## Key Takeaways

The `.bashrc` file is run when the `bash` shell starts. This is great for
setting up user preferences for using the server. However, if there are problems
with the file then it could prevent logins. It's good to know that `bash` and
`ssh` have flags that can get around this potentially grim situation.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

### Other Shells

The `bash` shell is just one of many shells. What about using a shell like `sh`
that doesn't run the `.bashrc` file?

```
$ ssh -t bandit18@bandit.labs.overthewire.org -p 2220 sh
[REMOVED: /etc/issue]
bandit18@bandit.labs.overthewire.org's password:
$ cat readme
[REMOVED: BANDIT19 PASSWORD]
$
```

### Other Commands

The goal here is to log in, and then `cat` the `readme` file. Is there any need
to run a shell? The command itself can be run:

```
$ ssh bandit18@bandit.labs.overthewire.org -p 2220 cat readme
[REMOVED: /etc/issue]
bandit18@bandit.labs.overthewire.org's password:
[REMOVED: BANDIT19 PASSWORD]
$
```

This is powerful: `ssh` into a server, run a command, and exit.
