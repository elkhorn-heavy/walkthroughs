# OverTheWire - Bandit - Level 31

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

This challenge says that there is a `git` repository on the server that is owned
by the user `bandit30-git`. The challenge is to clone the repository and then
find the password for `bandit31`.

Then use `ssh` to log into the server as the `bandit31` user.

## Commands Used to Solve This Challenge

- `git`: the stupid content tracker
- `ls`: list directory contents
- `mktemp`: create a temporary file or directory
- `ssh`: OpenSSH remote login client

## Initial Analysis

This is similar to the previous challenges, which had the password hidden
somewhere in the repository. This challenge will probably be more difficult than
the previous ones. As described, the approach will be to clone the repository
and then poke around until the password is found.

## Understanding the Challenge

This challenge continues to teach about the `git` command and repositories.

## Approach Strategy

1. Log in using `ssh`
1. Use `mktemp` to create a working directory
1. Use `git clone` to clone the repository
1. Find the `bandit31` password in the repository

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit30`. Using `ls` to look at the home directory gives:

```
bandit30@bandit:~$ ls -al
total 20
drwxr-xr-x  2 root root 4096 Apr 10 14:22 .
drwxr-xr-x 70 root root 4096 Apr 10 14:24 ..
-rw-r--r--  1 root root  220 Mar 31  2024 .bash_logout
-rw-r--r--  1 root root 3771 Mar 31  2024 .bashrc
-rw-r--r--  1 root root  807 Mar 31  2024 .profile
bandit30@bandit:~$
```

Nothing of interest there. The next step is to make a temporary working area,
and then change directory into it.

```
bandit30@bandit:~$ mktemp -d
/tmp/tmp.a3E2W5NH9i
bandit30@bandit:~$ cd /tmp/tmp.a3E2W5NH9i
bandit30@bandit:/tmp/tmp.a3E2W5NH9i$
```

The next step is to clone the repository. The repository URL given in the
challenge description doesn't include the port number, but running
`git clone --help` describes where to put the port number in the URL:

```
bandit30@bandit:/tmp/tmp.a3E2W5NH9i$ git clone ssh://bandit30-git@localhost:2220/home/bandit30-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit30/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit30/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit30-git@localhost's password:
remote: Enumerating objects: 4, done.
remote: Counting objects: 100% (4/4), done.
remote: Total 4 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (4/4), done.
bandit30@bandit:/tmp/tmp.a3E2W5NH9i$
```

That was straightforward, and it looks to be a small repository. Now the `repo`
repository has been cloned to the temporary directory:

```
bandit30@bandit:/tmp/tmp.a3E2W5NH9i$ cd repo
bandit30@bandit:/tmp/tmp.a3E2W5NH9i/repo$ ls -al
total 16
drwxrwxr-x 3 bandit30 bandit30 4096 Apr 11 18:43 .
drwx------ 3 bandit30 bandit30 4096 Apr 11 18:42 ..
drwxrwxr-x 8 bandit30 bandit30 4096 Apr 11 18:43 .git
-rw-rw-r-- 1 bandit30 bandit30   30 Apr 11 18:43 README.md
bandit30@bandit:/tmp/tmp.a3E2W5NH9i/repo$
```

The repository has a `README.md` file in it, so that is a good place to start:

```
bandit30@bandit:/tmp/tmp.a3E2W5NH9i/repo$ cat README.md
just an epmty file... muahaha
bandit30@bandit:/tmp/tmp.a3E2W5NH9i/repo$
```

Harrumph! Next check the commits for the repository:

```
bandit30@bandit:/tmp/tmp.a3E2W5NH9i/repo$ git log
commit fb05775f973256dc6d8d5bb6a8e6b96b0d8795c8 (HEAD -> master, origin/master, origin/HEAD)
Author: Ben Dover <noone@overthewire.org>
Date:   Thu Apr 10 14:23:24 2025 +0000

    initial commit of README.md
bandit30@bandit:/tmp/tmp.a3E2W5NH9i/repo$
```

A single commit, so what is in the filesystem is what is in the repository. The
next obvious thing is to look for other branches:

```
bandit30@bandit:/tmp/tmp.a3E2W5NH9i/repo$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
bandit30@bandit:/tmp/tmp.a3E2W5NH9i/repo$
```

There's only a single branch in the repository, so no luck there. The `git`
command also can list the commits that are "tagged" because the user wanted to
mark them in a special way. To get the tags:

```
bandit30@bandit:/tmp/tmp.a3E2W5NH9i/repo$ git tag
secret
bandit30@bandit:/tmp/tmp.a3E2W5NH9i/repo$
```

A tag named `secret`, how interesting! To fetch the details about the tag:

```
bandit30@bandit:/tmp/tmp.a3E2W5NH9i/repo$ git show secret
[REMOVED: BANDIT31 PASSWORD]
bandit30@bandit:/tmp/tmp.a3E2W5NH9i/repo$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit31` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit30@bandit:~$
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit31@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit31@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit31@bandit:~$
```

## Key Takeaways

This challenge continues to teach about `git` repositories, which can contain
tags that themselves may contain sensitive information. This is somewhat
unlikely but good to know about.

## Beyond the Flag

This is a straightforward clone and examination of a `git` repository, with the
difficulty of the password being in a tag. There isn't much more to be done with
this one.
