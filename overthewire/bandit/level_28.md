# OverTheWire - Bandit - Level 28

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

This challenge says that there is a `git` repository on the server that is owned
by the user `bandit27-git`. The challenge is to clone the repository and then
find the password for `bandit28`.

Then use `ssh` to log into the server as the `bandit28` user.

## Commands Used to Solve This Challenge

- `git`: the stupid content tracker
- `ls`: list directory contents
- `mktemp`: create a temporary file or directory
- `ssh`: OpenSSH remote login client

## Initial Analysis

It sounds like the password is hidden in the repository somewhere. As described,
the approach will be to clone the repository and then poke around until the
password is found.

## Understanding the Challenge

This challenge provides an introduction to the `git` command.

## Approach Strategy

1. Log in using `ssh`
1. Use `mktemp` to create a working directory
1. Use `git clone` to clone the repository
1. Find the `bandit28` password in the repository

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit27`. Using `ls` to look at the home directory gives:

```
bandit27@bandit:~$ ls -al
total 20
drwxr-xr-x  2 root root 4096 Apr 10 14:22 .
drwxr-xr-x 70 root root 4096 Apr 10 14:24 ..
-rw-r--r--  1 root root  220 Mar 31  2024 .bash_logout
-rw-r--r--  1 root root 3771 Mar 31  2024 .bashrc
-rw-r--r--  1 root root  807 Mar 31  2024 .profile
bandit27@bandit:~$
```

Nothing of interest there. The next step is to make a temporary working area,
and then change directory into it.

```
bandit27@bandit:~$ mktemp -d
/tmp/tmp.oOwhSGgqIj
bandit27@bandit:~$ cd /tmp/tmp.oOwhSGgqIj
bandit27@bandit:/tmp/tmp.oOwhSGgqIj$
```

The next step is to clone the repository. The repository URL given in the
challenge description doesn't include the port number, but running
`git clone --help` describes where to put the port number in the URL:

```
bandit27@bandit:/tmp/tmp.oOwhSGgqIj$ git clone ssh://bandit27-git@localhost:2220/home/bandit27-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit27/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit27/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit27-git@localhost's password:
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (3/3), done.
bandit27@bandit:/tmp/tmp.oOwhSGgqIj$
```

That was straightforward, and it looks to be a small repository. Now the `repo`
repository has been cloned to the temporary directory:

```
bandit27@bandit:/tmp/tmp.oOwhSGgqIj$ cd repo
bandit27@bandit:/tmp/tmp.oOwhSGgqIj/repo$ ls -al
total 16
drwxrwxr-x 3 bandit27 bandit27 4096 Apr 11 11:42 .
drwx------ 3 bandit27 bandit27 4096 Apr 11 11:41 ..
drwxrwxr-x 8 bandit27 bandit27 4096 Apr 11 11:42 .git
-rw-rw-r-- 1 bandit27 bandit27   68 Apr 11 11:42 README
bandit27@bandit:/tmp/tmp.oOwhSGgqIj/repo$
```

The repository has a `README` file in it, so that is a good place to start:

```
bandit27@bandit:/tmp/tmp.oOwhSGgqIj/repo$ cat README
The password to the next level is: [REMOVED: BANDIT28 PASSWORD]
```

The password was thankfully in an obvious place. With a `git` repository it
could have been more complicated.

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit28` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit27@bandit:~$
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit28@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit28@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit28@bandit:~$
```

## Key Takeaways

This challenge introduces `git` repositories as sources of information. They can
contain source code to be examined for vulnerabilities, lists of external
dependencies that may have vulnerabilities, or even API keys and passwords.

## Beyond the Flag

This is a straightforward clone and examination of a `git` respository, and then
simply looking at a file in the repo.
