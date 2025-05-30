# OverTheWire - Bandit - Level 30

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

This challenge says that there is a `git` repository on the server that is owned
by the user `bandit29-git`. The challenge is to clone the repository and then
find the password for `bandit30`.

Then use `ssh` to log into the server as the `bandit30` user.

## Commands Used to Solve This Challenge

- `git`: the stupid content tracker
- `ls`: list directory contents
- `mktemp`: create a temporary file or directory
- `ssh`: OpenSSH remote login client

## Initial Analysis

This is similar to the previous challenges, which had the password in a file in
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
1. Find the `bandit30` password in the repository

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit29`. Using `ls` to look at the home directory gives:

```
bandit29@bandit:~$ ls -al
total 20
drwxr-xr-x  2 root root 4096 Apr 10 14:22 .
drwxr-xr-x 70 root root 4096 Apr 10 14:24 ..
-rw-r--r--  1 root root  220 Mar 31  2024 .bash_logout
-rw-r--r--  1 root root 3771 Mar 31  2024 .bashrc
-rw-r--r--  1 root root  807 Mar 31  2024 .profile
bandit29@bandit:~$
```

Nothing of interest there. The next step is to make a temporary working area,
and then change directory into it.

```
bandit29@bandit:~$ mktemp -d
/tmp/tmp.ABrQILio6o
bandit29@bandit:~$ cd /tmp/tmp.ABrQILio6o
bandit29@bandit:/tmp/tmp.ABrQILio6o$
```

The next step is to clone the repository. The repository URL given in the
challenge description doesn't include the port number, but running
`git clone --help` describes where to put the port number in the URL:

```
bandit29@bandit:/tmp/tmp.ABrQILio6o$ git clone ssh://bandit29-git@localhost:2220/home/bandit29-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit29/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit29/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit29-git@localhost's password:
remote: Enumerating objects: 16, done.
remote: Counting objects: 100% (16/16), done.
remote: Compressing objects: 100% (11/11), done.
Receiving objects: 100% (16/16), 1.44 KiB | 1.44 MiB/s, done.
Resolving deltas: 100% (2/2), done.
remote: Total 16 (delta 2), reused 0 (delta 0), pack-reused 0
bandit29@bandit:/tmp/tmp.ABrQILio6o$
```

That was straightforward, and it looks to be a small repository. Now the `repo`
repository has been cloned to the temporary directory:

```
bandit29@bandit:/tmp/tmp.ABrQILio6o$ cd repo
bandit29@bandit:/tmp/tmp.ABrQILio6o/repo$ ls -al
total 16
drwxrwxr-x 3 bandit29 bandit29 4096 Apr 11 18:03 .
drwx------ 3 bandit29 bandit29 4096 Apr 11 18:03 ..
drwxrwxr-x 8 bandit29 bandit29 4096 Apr 11 18:03 .git
-rw-rw-r-- 1 bandit29 bandit29  131 Apr 11 18:03 README.md
bandit29@bandit:/tmp/tmp.ABrQILio6o/repo$
```

The repository has a `README.md` file in it, so that is a good place to start:

```
bandit29@bandit:/tmp/tmp.ABrQILio6o/repo$ cat README.md
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: <no passwords in production!>

bandit29@bandit:/tmp/tmp.ABrQILio6o/repo$
```

Rats! Interesting that it mentions no passwords in production. If they are not
in production, then where are they?

The `git` command can show the log of commit messages in the repository:

```
bandit29@bandit:/tmp/tmp.ABrQILio6o/repo$ git log
commit 3b8b91fc3c48f1a19d05670fd45d3e3f2621fcfa (HEAD -> master, origin/master, origin/HEAD)
Author: Ben Dover <noone@overthewire.org>
Date:   Thu Apr 10 14:23:21 2025 +0000

    fix username

commit 8d2ffeb5e45f87d0abb028aa796e3ebb63c5579c
Author: Ben Dover <noone@overthewire.org>
Date:   Thu Apr 10 14:23:21 2025 +0000

    initial commit of README.md
bandit29@bandit:/tmp/tmp.ABrQILio6o/repo$
```

This repository has two commits, with the most recent one at the top. The top
commit message says that the username is fixed, but no mention of the password.
That isn't too surprising, as this challenge won't have the same solution as the
previous challenge.

A `git` repository can have named "branches" that are code that has not been
merged into the main branch:

```
bandit29@bandit:/tmp/tmp.ABrQILio6o/repo$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/dev
  remotes/origin/master
  remotes/origin/sploits-dev
bandit29@bandit:/tmp/tmp.ABrQILio6o/repo$
```

So the current `HEAD` branch in our filesystem is also called `master` (more
modern repositories call the default branch `main`). There are also `dev` and
`sploits-dev` branches.

The `git` command can provide a difference between the current branch and one of
these named branches. The output can be huge, but hopefully for this sample
repository it is manageable:

```
bandit29@bandit:/tmp/tmp.Vg7mKsQ7HT/repo$ git diff remotes/origin/dev
diff --git a/README.md b/README.md
index bc6ad3d..1af21d3 100644
--- a/README.md
+++ b/README.md
@@ -4,5 +4,5 @@ Some notes for bandit30 of bandit.
 ## credentials

 - username: bandit30
-- password: [REMOVED: BANDIT30 PASSWORD]
+- password: <no passwords in production!>

diff --git a/code/gif2ascii.py b/code/gif2ascii.py
deleted file mode 100644
index 8b13789..0000000
--- a/code/gif2ascii.py
+++ /dev/null
@@ -1 +0,0 @@
-
bandit29@bandit:/tmp/tmp.Vg7mKsQ7HT/repo$
```

There it is, about halfway through the output: in the `README.md` file the
"password" line was changed in the `dev` branch to include the actual password.

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit30` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit29@bandit:~$
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit30@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit30@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit30@bandit:~$
```

## Key Takeaways

This challenge continues to teach about `git` repositories, which can contain
named branches that differ from the default branch. These branches may contain
sensitive information.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

This is a straightforward clone and examination of a `git` repository, with the
difficulty of the password being in one of the named branches. If there is a lot
of information in a branch, the `git diff` command output can be overwhelming.
It might be easier to check out the branch and examine it manually:

```
bandit29@bandit:/tmp/tmp.Vg7mKsQ7HT/repo$ git checkout remotes/origin/dev
Note: switching to 'remotes/origin/dev'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at a97d0db add data needed for development
bandit29@bandit:/tmp/tmp.Vg7mKsQ7HT/repo$ cat README.md
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: [REMOVED: BANDIT30 PASSWORD]

bandit29@bandit:/tmp/tmp.Vg7mKsQ7HT/repo$
```
