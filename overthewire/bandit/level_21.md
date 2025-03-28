# OverTheWire - Bandit - Level 21

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to use a `setuid` binary to get the next password.
This binary will connect to a port specified on the command line, and if it
received the password for `bandit20` it will return the password for `bandit21`.
There is a hint to try connecting to our own network daemon, so maybe this is
the solution.

Then use `ssh` to log into the server as the `bandit20` user.

## Commands Used to Solve This Challenge

- `ls`: list directory contents
- `nc`: arbitrary TCP and UDP connections and listens
- `ssh`: OpenSSH remote login client

## Initial Analysis

The `nc` command can be used to listen on a port and return data. This seems to
be the solution.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

The `nc` command has previously been used as a network _client_. It seems that
this challenge involves using `nc` as a network _server_. It's unclear if there
is an actual server already listening on a port, and will print the current
password, or if the entire goal is to use `nc`.

This challenge also hints at using job control, such as running processes in
the background.

## Approach Strategy

1. Log in using `ssh`
1. Use `ls` to find the `setuid` binary
1. Use `nc` to listen on a port and provide the current password
1. Use the `setuid` binary to read the current password and display the next

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit20`. The `ls` command is used to get information about the `setuid` file:

```
bandit20@bandit:~$ ls -l
total 16
-rwsr-x--- 1 bandit21 bandit20 15604 Sep 19  2024 suconnect
bandit20@bandit:~$
```

The `nc` command has a `-l` flag to listen on a port. The `-p` flag defines the
port number. To get `nc` to respond to a connection with the password, `cat` is
used with the current password file:

```
bandit20@bandit:~$ cat /etc/bandit_pass/bandit20 | nc -l -p 33333 &
[1] 2755151
bandit20@bandit:~$
```

> Note that it is safe to `cat` the password file, but it would not be safe to
> `echo` the actual password. On a multi-user system it is possible to see the
> commands run by other users, so sensitive information should never be put on
> the command line as a literal value.

This `nc` command ends with `&`, which tells the shell to run this process in
the background. This is because `nc` will sit there until something connnects to
the port, and only then will the shell be returned to the user. By putting it in
the background the shell immediately returns to the user and more commands can
be run. This challenge could also be solved by running `nc` in the foreground
and opening another `ssh` session, but it seems that job control was something
to learn.

To see which jobs are currently running, there is a built-in `jobs` command in
the shell:

```
bandit20@bandit:~$ jobs
[1]+  Running                 cat /etc/bandit_pass/bandit20 | nc -l -p 33333 &
bandit20@bandit:~$
```

Since `nc` is patiently waiting for something to connect, the `setuid` binary
can be used:

```
bandit20@bandit:~$ ./suconnect 33333
Read: [REMOVED: BANDIT20 PASSWORD]
Password matches, sending next password
[REMOVED: BANDIT21 PASSWORD]
[1]+  Done                    cat /etc/bandit_pass/bandit20 | nc -l -p 33333
bandit20@bandit:~$
```

There is it. The last line is the shell announcing that the background `nc`
process has finished and is `Done`.

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit21` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit20@bandit:~$
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit21@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit21@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit21@bandit:~$
```

## Key Takeaways

The `nc` command is versatile and can act as both a client and a server.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

Perhaps this could be done using `socat` instead of `nc`?
