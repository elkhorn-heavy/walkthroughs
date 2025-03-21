# OverTheWire - Bandit - Level 6

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to look in the `inhere` directory and find a file
with very specific attributes:

- human-readable
- 1033 bytes in size
- not executable

Then use `ssh` to log into the server as the `bandit6` user.

## Commands Used to Solve This Challenge

- `cat`: concatenate files and print on the standard output
- `file`: determine file type
- `find`: search for files in a directory hierarchy
- `ls`: list directory contents
- `ssh`: OpenSSH remote login client

## Initial Analysis

This might be possible by just scanning all the files, but it depends how many
there are. The information from the previous challenge is used to `ssh` into the
server.

## Understanding the Challenge

It appears that the goal is to introduce the `find` command, which is one of the
commands in the hints.

## Approach Strategy

1. Log in using `ssh`
1. Try to find the file by scanning the `ls` output
1. If not, then try to use `find` to reduce the set of files
1. Use `file` to look at the file types
1. Use `cat` to display the file

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit5`. To list the files in the directory, the `ls -al` command is used:

```
bandit5@bandit:~$ ls -al inhere
total 88
drwxr-x--- 22 root bandit5 4096 Sep 19 07:08 .
drwxr-xr-x  3 root root    4096 Sep 19 07:08 ..
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere00
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere01
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere02
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere03
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere04
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere05
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere06
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere07
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere08
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere09
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere10
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere11
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere12
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere13
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere14
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere15
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere16
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere17
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere18
drwxr-x---  2 root bandit5 4096 Sep 19 07:08 maybehere19
bandit5@bandit:~$
```

Oh boy. That's 20 directories and who knows how many files in each one. To stick
with the plan, the next approach will be to use the `find` command. This command
is great for, well, finding files and directories within a filesystem:

```
bandit5@bandit:~$ find inhere -size 1033
bandit5@bandit:~$
```

Nothing?! The `find` man page says that the default units for the `-size` flag
is 512 byte blocks. The proper command is:

```
bandit5@bandit:~$ find inhere -size 1033c
inhere/maybehere07/.file2
bandit5@bandit:~$
```

Well, there's only one file that is 1033 bytes in size. Another attribute of the
file is that it's not executable, so adding that to the find command to confirm:

```
bandit5@bandit:~$ find inhere -size 1033c ! -executable
inhere/maybehere07/.file2
bandit5@bandit:~$
```

Looking good. Finally, the file must be human-readable. Using what was learned
in the previous challenge:

```
bandit5@bandit:~$ file inhere/maybehere07/.file2
inhere/maybehere07/.file2: ASCII text, with very long lines (1000)
bandit5@bandit:~$
```

Now to `cat` the file:

```
bandit5@bandit:~$ cat inhere/maybehere07/.file2
[REMOVED: BANDIT6 PASSWORD]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        bandit5@bandit:~$
```

Oh boy, that is indeed a really long line, but it looks like the password with
1000 spaces appended to it. To confirm that the password is correct, disconnect
from the server and then reconnect using the `bandit6` user and the found
password (`/etc/issue` and `/etc/motd` removed):

```
bandit5@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit6@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit6@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit6@bandit:~$
```

## Key Takeaways

This challenge introduces the `find` command, which is very useful when trying
to find files or directories with specific attributes.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

### Using `ls` to Check Permissions

Instead of using `find` to check that the file is not executable, `ls` can be
used:

```
bandit5@bandit:~$ ls -l inhere/maybehere07/.file2
-rw-r----- 1 root bandit5 1033 Sep 19 07:08 inhere/maybehere07/.file2
bandit5@bandit:~$
```

The first column of information is the permissions on the file. The first
character is a `-`, indicating that this isn't a directory (`d`) - although it
is a little more complicated than that. Following the first character is three
triplets of `r`ead, `w`rite, e`x`ecute. We can see that none of the three has
an `x`. Compare to:

```
bandit5@bandit:~$ ls -l /bin/ls
-rwxr-xr-x 1 root root 142312 Apr  5  2024 /bin/ls
bandit5@bandit:~$
```

The command `ls` is executable. The three groups indicate the permissions for
the owner of the file, everyone in the group of the file, and then the "world"
or everyone else.

Similarly, `find` can also be used to display the "long" listing of matches:

```
bandit5@bandit:~$ find inhere -size 1033c ! -executable -ls
   544599      4 -rw-r-----   1 root     bandit5      1033 Sep 19  2024 inhere/maybehere07/.file2
bandit5@bandit:~$
```

### Using `find` to Run `file`

Another tactic would have been to have the `find` command run `file` on
everything that matches the given parameters. The syntax is a little tricky but
it looks like:

```
bandit5@bandit:~$ find inhere -size 1033c ! -executable -exec file '{}' \;
inhere/maybehere07/.file2: ASCII text, with very long lines (1000)
bandit5@bandit:~$
```
