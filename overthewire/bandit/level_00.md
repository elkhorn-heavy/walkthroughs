# OverTheWire - Bandit - Level 0

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to use `ssh` (*s*ecure *sh*ell) to log into a
server.

## Commands Used to Solve This Challenge

- `man`: an interface to the system reference manuals
- `ssh`: OpenSSH remote login client

## Initial Analysis

This challenge provides all the information needed to `ssh` into a server:

- hostname: `bandit.labs.overthewire.org`
- port: `2220`
- username: `bandit0`
- password: `bandit0`

## Understanding the Challenge

It appears that the goal is to introduce the `ssh` command. The login
information is provided, and by logging into the server the challenge is
completed.

## Approach Strategy

1. Log in using `ssh`

## Step-by-Step Solution

All the login information is given, so the hard part is discovering how to call
`ssh` with the information in the correct places. The `man` command can be used
to read the "manual" for a command, so `man ssh` shows the `ssh` "man page". It
tells us that the basic format for `ssh` is:

```
$ ssh username@hostname
```

The above will `ssh` into `hostname` as the user `username`. By default the
connection will be made to the standard `ssh` port of `22`. In this challenge a
non-standard port is used, so the `-p` switch is needed:

```
$ ssh username@hostname -p port
```

What about the password? Reading the man page, `ssh` doesn't seem to have a way
to specify the password on the commmand line. This is common to most unix
commands, because secret information should never be passed as a command line
argument. The reason is that on multiuser systems the `ps` command will show all
the commands running in the system - any password on the command line would be
visible to other users!

So using the login information provided by the challenge, the command to run is:

```
$ ssh bandit0@bandit.labs.overthewire.org -p 2220
The authenticity of host '[bandit.labs.overthewire.org]:2220 ([16.16.163.126]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

This is a somewhat complicated response. What `ssh` is saying is that the host
`bandit.labs.overthewire.org` has never been seen before. This is a security
precaution to let the user know that the host is unexpected - if the user is in
fact hoping to connect to a host that has been used before, it's an indication
that something strange is going on.

Since this is the first time connecting to this server, `yes` is entered. This
will cause `ssh` to remember this server so that the next time a connection is
made the warning will not appear.

Carrying on:

```
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[bandit.labs.overthewire.org]:2220' (ED25519) to the list of known hosts.
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit0@bandit.labs.overthewire.org's password:
```

The connection to the server is successful. Some text called the _issue_ file
(`/etc/issue`) displays a pre-login banner, and then the password prompt is
given. Note that when the password is being typed in it is not displayed, which
prevents "shoulder surfing".

After entering the correct password, the server displays:

```
bandit0@bandit.labs.overthewire.org's password:

      ,----..            ,----,          .---.
     /   /   \         ,/   .`|         /. ./|
    /   .     :      ,`   .'  :     .--'.  ' ;
   .   /   ;.  \   ;    ;     /    /__./ \ : |
  .   ;   /  ` ; .'___,/    ,' .--'.  '   \' .
  ;   |  ; \ ; | |    :     | /___/ \ |    ' '
  |   :  | ; | ' ;    |.';  ; ;   \  \;      :
  .   |  ' ' ' : `----'  |  |  \   ;  `      |
  '   ;  \; /  |     '   :  ;   .   \    .\  ;
   \   \  ',  /      |   |  '    \   \   ' \ |
    ;   :    /       '   :  |     :   '  |--"
     \   \ .'        ;   |.'       \   \ ;
  www. `---` ver     '---' he       '---" ire.org


Welcome to OverTheWire!

If you find any problems, please report them to the #wargames channel on
discord or IRC.

--[ Playing the games ]--

  This machine might hold several wargames.
  If you are playing "somegame", then:

    * USERNAMES are somegame0, somegame1, ...
    * Most LEVELS are stored in /somegame/.
    * PASSWORDS for each level are stored in /etc/somegame_pass/.

  Write-access to homedirectories is disabled. It is advised to create a
  working directory with a hard-to-guess name in /tmp/.  You can use the
  command "mktemp -d" in order to generate a random and hard to guess
  directory in /tmp/.  Read-access to both /tmp/ is disabled and to /proc
  restricted so that users cannot snoop on eachother. Files and directories
  with easily guessable or short names will be periodically deleted! The /tmp
  directory is regularly wiped.
  Please play nice:

    * don't leave orphan processes running
    * don't leave exploit-files laying around
    * don't annoy other players
    * don't post passwords or spoilers
    * again, DONT POST SPOILERS!
      This includes writeups of your solution on your blog or website!

--[ Tips ]--

  This machine has a 64bit processor and many security-features enabled
  by default, although ASLR has been switched off.  The following
  compiler flags might be interesting:

    -m32                    compile for 32bit
    -fno-stack-protector    disable ProPolice
    -Wl,-z,norelro          disable relro

  In addition, the execstack tool can be used to flag the stack as
  executable on ELF binaries.

  Finally, network-access is limited for most levels by a local
  firewall.

--[ Tools ]--

 For your convenience we have installed a few useful tools which you can find
 in the following locations:

    * gef (https://github.com/hugsy/gef) in /opt/gef/
    * pwndbg (https://github.com/pwndbg/pwndbg) in /opt/pwndbg/
    * gdbinit (https://github.com/gdbinit/Gdbinit) in /opt/gdbinit/
    * pwntools (https://github.com/Gallopsled/pwntools)
    * radare2 (http://www.radare.org/)

--[ More information ]--

  For more information regarding individual wargames, visit
  http://www.overthewire.org/wargames/

  For support, questions or comments, contact us on discord or IRC.

  Enjoy your stay!

bandit0@bandit:~$
```

That's a lot of text! This is called the _message of the day_ (`/etc/motd`) and
is displayed on login. The last line, finally, is the shell prompt, also called
the command line prompt. The format of the prompt is:

```
username@hostname:current_directory$
```

For the prompt, the current directory is shown as `~`, which is a shortcut for
the user's home directory. The `$` at the end terminates the prompt, and means
that the shell is running with user permissions. If you log into a server and
have "root" or superuser permissions, it will be a `#` rather than `$`.

This completes the challenge.

## Key Takeaways

The `ssh` command is an important command for connecting to remote servers.

## Beyond the Flag

Exploring other capabilities of `ssh` is time well-invested. For example, `ssh`
also allows a URI-style destination, so the standard command:

```
$ ssh username@hostname -p port
```

can also be done as:

```
$ ssh ssh://username@hostname:port
```
