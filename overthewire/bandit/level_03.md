# OverTheWire - Bandit - Level 3

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to view the file named `spaces in this filename`
to get the password for level 3. Then use `ssh` to log into the server as the
`bandit3` user.

## Commands Used to Solve This Challenge

- `cat`: concatenate files and print on the standard output
- `ls`: list directory contents
- `ssh`: OpenSSH remote login client

## Initial Analysis

This challenge provides all the information needed: the password is in the file
called `spaces in this filename`. The information from the previous challenge is
used to `ssh` into the server.

The difficulty will be that the `spaces in this filename` file has (wait for it)
spaces in the filename. Spaces are special characters in unix, and are used to
separate arguments to commands.

## Understanding the Challenge

It appears that the goal is to teach how to view files with strange names.

## Approach Strategy

1. Log in using `ssh`
1. Find the file using `ls`
1. Use `cat` to display the file

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit2`. To list the files in the directory, the `ls` command is used:

```
bandit2@bandit:~$ ls -al
total 24
drwxr-xr-x  2 root    root    4096 Sep 19 07:08 .
drwxr-xr-x 70 root    root    4096 Sep 19 07:09 ..
-rw-r--r--  1 root    root     220 Mar 31  2024 .bash_logout
-rw-r--r--  1 root    root    3771 Mar 31  2024 .bashrc
-rw-r--r--  1 root    root     807 Mar 31  2024 .profile
-rw-r-----  1 bandit3 bandit2   33 Sep 19 07:08 spaces in this filename
bandit2@bandit:~$
```

Yes indeed, there is a 33 byte file called `spaces in this filename` in
bandit2's home directory. The technique in the previous challenges was to `cat`
the file. The "obvious" command is:

```
bandit2@bandit:~$ cat spaces in this filename
cat: spaces: No such file or directory
cat: in: No such file or directory
cat: this: No such file or directory
cat: filename: No such file or directory
bandit2@bandit:~$
```

Oh no - this command tells `cat` to print four different files named `spaces`,
`in`, `this`, and `filename`.

One way to _escape_ the spaces is to put the filename in double quotes:

```
bandit2@bandit:~$ cat "spaces in this filename"
[REMOVED: BANDIT3 PASSWORD]
bandit2@bandit:~$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit3` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit2@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit3@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit3@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit3@bandit:~$
```

## Key Takeaways

This challenge teaches that files containing spaces need to be escaped before
they can be used by commands.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

One other way to escape filenames is to use single quotes. There are very
important differences between using single and double quotes, but in this case
it doesn't matter:

```
bandit2@bandit:~$ cat 'spaces in this filename'
[REMOVED: BANDIT3 PASSWORD]
bandit2@bandit:~$
```

To escape a single character, a backslash can be used:

```
bandit2@bandit:~$ cat spaces\ in\ this\ filename
[REMOVED: BANDIT3 PASSWORD]
bandit2@bandit:~$
```

The shell also will do filename expansion using `*` as a wildcard:

```
bandit2@bandit:~$ cat spaces*
[REMOVED: BANDIT3 PASSWORD]
bandit2@bandit:~$
```

And finally, the shell autocomplete will solve this problem for us. By entering
`cat`, followed by space, followed by `s`, followed by `TAB`, it autocompletes
the filename _and_ escapes it:

```
bandit2@bandit:~$ cat spaces\ in\ this\ filename
[REMOVED: BANDIT3 PASSWORD]
bandit2@bandit:~$
```
