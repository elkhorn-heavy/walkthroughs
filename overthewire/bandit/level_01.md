# OverTheWire - Bandit - Level 1

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to view the file `readme` to get the password for
level 1. Then use `ssh` to log into the server as the `bandit1` user.

## Commands Used to Solve This Challenge

- `ssh`: OpenSSH remote login client
- `ls`: list directory contents
- `cat`: concatenate files and print on the standard output

## Initial Analysis

This challenge provides all the information needed: the password is in the file
called `readme`. The information from the previous challenge is used to `ssh`
into the server:

- hostname: `bandit.labs.overthewire.org`
- port: `2220`
- username: `bandit0`
- password: `bandit0`

## Understanding the Challenge

It appears that the goal is to introduce the `ls` and `cat` commands.

## Approach Strategy

1. Log in using `ssh`
1. Find the file using `ls`
1. Use `cat` to display the file

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit0`:

```
bandit0@bandit:~$
```

The format of the prompt is:

```
username@hostname:current_directory$
```

For the prompt, the current directory is shown as `~`, which is a shortcut for
the user's home directory. The `$` at the end terminates the prompt, and means
that the shell is running with user permissions. If you log into a server and
have "root" or superuser permissions, it will be a `#` rather than `$`.

To list the files in the directory, the `ls` command is used:

```
bandit0@bandit:~$ ls
readme
```

Excellent - the file named `readme` is in the current directory, which is the
user's home directory. Now to display the file using the `cat` command:

```
bandit0@bandit:~$ cat readme
Congratulations on your first steps into the bandit game!!
Please make sure you have read the rules at https://overthewire.org/rules/
If you are following a course, workshop, walkthrough or other educational activity,
please inform the instructor about the rules as well and encourage them to
contribute to the OverTheWire community so we can keep these games free!

The password you are looking for is: [PASSWORD REMOVED]
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit1` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit0@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit1@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit1@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit1@bandit:~$
```

## Key Takeaways

This challenge teaches important unix commands:

- `ls` to list directory contents
- `cat` to print the contents of a file

## Beyond the Flag

Exploring other capabilities of the `ls` and `cat` commands is time
well-invested.

### Exploring `ls`

The `ls` command has a `-l` flag to provide a "long" listing:

```
bandit0@bandit:~$ ls -l
total 4
-rw-r----- 1 bandit1 bandit0 438 Sep 19 07:08 readme
```

There is a wealth of information here. The line for the `readme` file contains:

- `-rw-r-----`: the file permissions
- `1`: the number of "links" to the file
- `bandit1`: the owner of the file
- `bandit0`: the group of the file
- `438`: the size of the file, in bytes
- `Sep 19 07:08`: the date and time the file was last modified
- `readme`: the filename

Similarly, `ls` has a `-a` flag to display "all" files, including "hidden"
system files:

```
bandit0@bandit:~$ ls -al
total 24
drwxr-xr-x  2 root    root    4096 Sep 19 07:08 .
drwxr-xr-x 70 root    root    4096 Sep 19 07:09 ..
-rw-r--r--  1 root    root     220 Mar 31  2024 .bash_logout
-rw-r--r--  1 root    root    3771 Mar 31  2024 .bashrc
-rw-r--r--  1 root    root     807 Mar 31  2024 .profile
-rw-r-----  1 bandit1 bandit0  438 Sep 19 07:08 readme
```

This shows that there are actually six files / directories:

- `.`: the current directory
- `..`: the directory above this one
- `.bash_logout`: a script that is run when the user logs out
- `.bashrc`: a script that is run when the user logs in
- `.profile`: another script run when the user logs in
- `readme`: the file containing this challenge's password

### Exploring `cat`

The `cat` command is used in this challenge to display a single file, but is
is designed to concatenate multiple files and then display them:

```
$ cat file1
file1 contents
$ cat file 2
file2 contents
$ cat file1 file2
file1 contents
file2 contents
```

### Alternative Solutions

It's good practice to solve things in different ways. For example, what if the
`ls` command didn't exist? The shell does filename completion using the TAB key,
so typing `cat`, and a space, and then hitting TAB, it displays the multiple
possibilities:

```
bandit0@bandit:~$ cat
.bash_logout  .bashrc       .profile      readme
```

Similarly it will complete partial filenames, so typing `cat`, and a space, and
`r`, and then hitting TAB autocompletes to:

```
bandit0@bandit:~$ cat readme
```

This saves a lot of typing!

If there are multiple matches, it will complete as far as it can, so typing
`cat`, and a space, and `.b`, and then hitting TAB autocompletes to:

```
bandit0@bandit:~$ cat .bash
```

at this point, hitting TAB again will display the options:

```
bandit0@bandit:~$ cat .bash
.bash_logout  .bashrc
```
