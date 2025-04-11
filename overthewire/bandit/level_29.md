# OverTheWire - Bandit - Level 29

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

This challenge says that there is a `git` repository on the server that is owned
by the user `bandit28-git`. The challenge is to clone the repository and then
find the password for `bandit29`.

Then use `ssh` to log into the server as the `bandit29` user.

## Commands Used to Solve This Challenge

- `git`: the stupid content tracker
- `ls`: list directory contents
- `mktemp`: create a temporary file or directory
- `ssh`: OpenSSH remote login client

## Initial Analysis

This is similar to the previous challenge, which had the password in a file in
the main branch of the repository. This challenge again has the password hidden
in the repository, but it will probably be more difficult to find it. As
described, the approach will be to clone the repository and then poke around
until the password is found.

## Understanding the Challenge

This challenge continues to teach about the `git` command and repositories.

## Approach Strategy

1. Log in using `ssh`
1. Use `mktemp` to create a working directory
1. Use `git clone` to clone the repository
1. Find the `bandit29` password in the repository

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit28`. Using `ls` to look at the home directory gives:

```
bandit28@bandit:~$ ls -al
total 20
drwxr-xr-x  2 root root 4096 Apr 10 14:22 .
drwxr-xr-x 70 root root 4096 Apr 10 14:24 ..
-rw-r--r--  1 root root  220 Mar 31  2024 .bash_logout
-rw-r--r--  1 root root 3771 Mar 31  2024 .bashrc
-rw-r--r--  1 root root  807 Mar 31  2024 .profile
bandit28@bandit:~$
```

Nothing of interest there. The next step is to make a temporary working area,
and then change directory into it.

```
bandit28@bandit:~$ mktemp -d
/tmp/tmp.v21xLs8MN1
bandit28@bandit:~$ cd /tmp/tmp.v21xLs8MN1
bandit28@bandit:/tmp/tmp.v21xLs8MN1$
```

The next step is to clone the repository. The repository URL given in the
challenge description doesn't include the port number, but running
`git clone --help` describes where to put the port number in the URL:

```
bandit28@bandit:/tmp/tmp.v21xLs8MN1$ git clone ssh://bandit28-git@localhost:2220/home/bandit28-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit28/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit28/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit28-git@localhost's password:
remote: Enumerating objects: 9, done.
remote: Counting objects: 100% (9/9), done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 9 (delta 2), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (9/9), 798 bytes | 399.00 KiB/s, done.
Resolving deltas: 100% (2/2), done.
bandit28@bandit:/tmp/tmp.v21xLs8MN1$
```

That was straightforward, and it looks to be a small repository. Now the `repo`
repository has been cloned to the temporary directory:

```
bandit28@bandit:/tmp/tmp.v21xLs8MN1$ cd repo
bandit28@bandit:/tmp/tmp.v21xLs8MN1/repo$ ls -al
total 16
drwxrwxr-x 3 bandit28 bandit28 4096 Apr 11 17:43 .
drwx------ 3 bandit28 bandit28 4096 Apr 11 17:43 ..
drwxrwxr-x 8 bandit28 bandit28 4096 Apr 11 17:43 .git
-rw-rw-r-- 1 bandit28 bandit28  111 Apr 11 17:43 README.md
bandit28@bandit:/tmp/tmp.v21xLs8MN1/repo$
```

The repository has a `README.md` file in it, so that is a good place to start:

```
bandit28@bandit:/tmp/tmp.v21xLs8MN1/repo$ cat README.md
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: xxxxxxxxxx

bandit28@bandit:/tmp/tmp.v21xLs8MN1/repo$
```

Rats! The password in the file literally is `xxxxxxxxxx`, so obviously that is a
dummy password. This makes sense, as that was the location of the password for
the last challenge, and this challenge will probably be harder.

The `git` command can show the log of commit messages in the repository:

```
bandit28@bandit:/tmp/tmp.v21xLs8MN1/repo$ git log
commit 674690a00a0056ab96048f7317b9ec20c057c06b (HEAD -> master, origin/master, origin/HEAD)
Author: Morla Porla <morla@overthewire.org>
Date:   Thu Apr 10 14:23:19 2025 +0000

    fix info leak

commit fb0df1358b1ff146f581651a84bae622353a71c0
Author: Morla Porla <morla@overthewire.org>
Date:   Thu Apr 10 14:23:19 2025 +0000

    add missing data

commit a5fdc97aae2c6f0e6c1e722877a100f24bcaaa46
Author: Ben Dover <noone@overthewire.org>
Date:   Thu Apr 10 14:23:19 2025 +0000

    initial commit of README.md
bandit28@bandit:/tmp/tmp.v21xLs8MN1/repo$
```

This repository has three commits, with the most recent one at the top. The top
commit message is the clue that is needed - it fixes an information leak. So the
commit before it should contain the un-fixed information.

The `git` command can revert to a previous commit. Where `HEAD` refers to the
latest commit in a repository, `HEAD~1` is the commit before it. The `git`
command can check out that commit, so that the filesystem looks like the latest
commit was never made:

```
bandit28@bandit:/tmp/tmp.v21xLs8MN1/repo$ git checkout HEAD~1
Note: switching to 'HEAD~1'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at fb0df13 add missing data
bandit28@bandit:/tmp/tmp.v21xLs8MN1/repo$
```

OK, so now to look at the `README.md` file again:

```
bandit28@bandit:/tmp/tmp.v21xLs8MN1/repo$ cat README.md
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: [REMOVED: BANDIT29 PASSWORD]

bandit28@bandit:/tmp/tmp.v21xLs8MN1/repo$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit29` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit28@bandit:~$
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit29@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit29@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit29@bandit:~$
```

## Key Takeaways

This challenge continues to teach about `git` repositories. Since `git` is a
revision control system, new commits never remove old data. In other words, if
sensitive data like a password is accidentally commited to a repository, that
password _must_ be changed, in addition to removing it from the repository. An
attacker can go back in time through the repository and retrieve the password.

## Beyond the Flag

This is a straightforward clone and examination of a `git` respository, and then
simply looking at a previous version of a file in the repo.
