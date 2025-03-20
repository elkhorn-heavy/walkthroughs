# OverTheWire - Bandit - Level 4

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to view a hidden file in the `inhere` directory.
Then use `ssh` to log into the server as the `bandit4` user.

## Commands Used to Solve This Challenge

- `ssh`: OpenSSH remote login client
- `ls`: list directory contents
- `cat`: concatenate files and print on the standard output

## Initial Analysis

This challenge provides all the information needed: the password is in a hidden
file in the `inhere` directory. The information from the previous challenge is
used to `ssh` into the server.

The difficulty will be that the file is hidden.

## Understanding the Challenge

It appears that the goal is to teach that it is possible to create so-called
"hidden" files.

## Approach Strategy

1. Log in using `ssh`
1. Find the file using `ls`
1. Use `cat` to display the file

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit3`. To list the files in the directory, the `ls` command is used:

```
bandit3@bandit:~$ ls
inhere
bandit3@bandit:~$
```

That's good news, the `inhere` directory exists as promised. Now to do a
directory listing on that directory:

```
bandit3@bandit:~$ ls inhere
bandit3@bandit:~$
```

Nothing! Good thing that the challenge warned that the file is "hidden". By
default most commands hide system files (or "hidden" files) and directories.
These are the ones that start with a `.`.

To view hidden files, the `-a` flag for `ls` will display "all" files and
directories:

```
bandit3@bandit:~$ ls -a inhere
.  ..  ...Hiding-From-You
```

Hmm! So there's a `.` (the directory `inhere` itself), `..` (the directory above
`inhere`), and `...Hiding-From-You`. `...Hiding-From-You` is a probably a file,
and the `-l` flag for `ls` will give a "long" listing to confirm this.

```
bandit3@bandit:~$ ls -al inhere
total 12
drwxr-xr-x 2 root    root    4096 Sep 19 07:08 .
drwxr-xr-x 3 root    root    4096 Sep 19 07:08 ..
-rw-r----- 1 bandit4 bandit3   33 Sep 19 07:08 ...Hiding-From-You
```

And there it is, a 33 byte file. When the first character of the "long" listing
is a `d`, then it's a directory. If it's a `-` then it's a regular file.

Now a simple `cat` will display the password:

```
bandit3@bandit:~$ cat inhere/...Hiding-From-You
[PASSWORD REMOVED]
bandit3@bandit:~$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit4` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit3@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit4@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit4@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit4@bandit:~$
```

## Key Takeaways

This challenge teaches that files starting with `.` are hidden from many
commands.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

The shell autocomplete will solve this problem for us. By entering
`cat`, followed by space, followed by `inhere/`, followed by `TAB`, it
autocompletes the filename:

```
bandit3@bandit:~$ cat inhere/...Hiding-From-You
[PASSWORD REMOVED]
```
