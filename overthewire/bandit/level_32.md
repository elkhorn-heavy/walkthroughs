# OverTheWire - Bandit - Level 32

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

This challenge says that there is a `git` repository on the server that is owned
by the user `bandit31-git`. The challenge is to clone the repository and then
find the password for `bandit32`.

Then use `ssh` to log into the server as the `bandit32` user.

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
1. Find the `bandit32` password in the repository

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit31`. Using `ls` to look at the home directory gives:

```
bandit31@bandit:~$ ls -al
total 24
drwxr-xr-x  2 root root 4096 Apr 10 14:23 .
drwxr-xr-x 70 root root 4096 Apr 10 14:24 ..
-rw-r--r--  1 root root  220 Mar 31  2024 .bash_logout
-rw-r--r--  1 root root 3771 Mar 31  2024 .bashrc
-rwxr-xr-x  1 root root   59 Apr 10 14:23 .gitconfig
-rw-r--r--  1 root root  807 Mar 31  2024 .profile
bandit31@bandit:~$
```

That's interesting - this user has a `.gitconfig` file:

```
bandit31@bandit:~$ cat .gitconfig
[user]
        email = bandit31@overthewire.org
        name = bandit31

bandit31@bandit:~$
```

However, the configuration file doesn't have anything of interest in it. The
next step is to make a temporary working area, and then change directory into
it.

```bandit31@bandit:~$ mktemp -d
/tmp/tmp.H858KUEatP
bandit31@bandit:~$ cd /tmp/tmp.H858KUEatP
bandit31@bandit:/tmp/tmp.H858KUEatP$
```

The next step is to clone the repository. The repository URL given in the
challenge description doesn't include the port number, but running
`git clone --help` describes where to put the port number in the URL:

```
bandit31@bandit:/tmp/tmp.H858KUEatP$ git clone ssh://bandit31-git@localhost:2220/home/bandit31-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit31/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit31/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit31-git@localhost's password:
remote: Enumerating objects: 4, done.
remote: Counting objects: 100% (4/4), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 4 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (4/4), 382 bytes | 191.00 KiB/s, done.
bandit31@bandit:/tmp/tmp.H858KUEatP$
```

That was straightforward, and it looks to be a small repository. Now the `repo`
repository has been cloned to the temporary directory:

```
bandit31@bandit:/tmp/tmp.H858KUEatP$ cd repo/
bandit31@bandit:/tmp/tmp.H858KUEatP/repo$ ls -al
total 20
drwxrwxr-x 3 bandit31 bandit31 4096 Apr 11 19:19 .
drwx------ 3 bandit31 bandit31 4096 Apr 11 19:19 ..
drwxrwxr-x 8 bandit31 bandit31 4096 Apr 11 19:19 .git
-rw-rw-r-- 1 bandit31 bandit31    6 Apr 11 19:19 .gitignore
-rw-rw-r-- 1 bandit31 bandit31  147 Apr 11 19:19 README.md
bandit31@bandit:/tmp/tmp.H858KUEatP/repo$
```

There is now a `.gitignore` file in the directory, which is different from the
previous challenges. However, the repository still has a `README.md` file in it,
so that is a good place to start:

```
bandit31@bandit:/tmp/tmp.H858KUEatP/repo$ cat README.md
This time your task is to push a file to the remote repository.

Details:
    File name: key.txt
    Content: 'May I come in?'
    Branch: master

bandit31@bandit:/tmp/tmp.H858KUEatP/repo$
```

Interesting - so this explains why there are new configuration files. The file
`~/.gitconfig` defines the credentials to log into the `git` server.

The first step is to create the file `key.txt`:

```
bandit31@bandit:/tmp/tmp.H858KUEatP/repo$ echo "May I come in?" > key.txt
bandit31@bandit:/tmp/tmp.H858KUEatP/repo$
```

Next the file needs to be added to the next `git` commit:

```
bandit31@bandit:/tmp/tmp.H858KUEatP/repo$ git add key.txt
The following paths are ignored by one of your .gitignore files:
key.txt
hint: Use -f if you really want to add them.
hint: Turn this message off by running
hint: "git config advice.addIgnoredFile false"
bandit31@bandit:/tmp/tmp.H858KUEatP/repo$
```

Oh, that failed! The new `.gitignore` file in this directory contains a list of
files that should not be committed to the repository. For example, a
configuration file could be excluded so that each contributor can configure it
their own way. According to the hint in the error message, the `-f` flag will
force the add:

```
bandit31@bandit:/tmp/tmp.H858KUEatP/repo$ git add -f key.txt
bandit31@bandit:/tmp/tmp.H858KUEatP/repo$
```

That succeeded. Now to commit the changes to this local copy of the default
branch:

```
bandit31@bandit:/tmp/tmp.H858KUEatP/repo$ git commit -m "my commit message"
[master 9acc231] my commit message
 1 file changed, 1 insertion(+)
 create mode 100644 key.txt
bandit31@bandit:/tmp/tmp.H858KUEatP/repo$
```

And now for the big finale - push the commit to the server to see what happens:

```
bandit31@bandit:/tmp/tmp.H858KUEatP/repo$ git push
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit31/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit31/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit31-git@localhost's password:
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 2 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 320 bytes | 320.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
remote: ### Attempting to validate files... ####
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
remote: Well done! Here is the password for the next level:
remote: [REMOVED: BANDIT32 PASSWORD]
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
To ssh://localhost:2220/home/bandit31-git/repo
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'ssh://localhost:2220/home/bandit31-git/repo'
bandit31@bandit:/tmp/tmp.H858KUEatP/repo$
```

And there in the middle of the "remote" lines is the next password. The server
has rejected the push, but that is probably so that the challenge will work
repeatedly.

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit32` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit31@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit32@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit32@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit32@bandit:~$
```

## Key Takeaways

This challenge continues to teach about `git` repositories, which allow users to
make changes and push those changes to the repository server.

## Beyond the Flag

This is a straightforward clone and examination of a `git` repository, with the
goal of learning how to make changes to an upstream repository. There isn't much
more to be done with this one.
