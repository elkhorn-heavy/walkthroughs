# OverTheWire - Bandit - Level 8

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to look in the file `data.txt` to find the word
`millionth` - the password will be next to it.

Then use `ssh` to log into the server as the `bandit8` user.

## Commands Used to Solve This Challenge

- `grep`: print lines that match patterns
- `ls`: list directory contents
- `ssh`: OpenSSH remote login client

## Initial Analysis

Going to guess that this is a very large file, something that is too big to read
through looking for the word "millionth".

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

It appears that the goal is to use `grep` to search the file.

## Approach Strategy

1. Log in using `ssh`
1. Use `ls` to locate `data.txt`
1. Use `grep` to find the word `millionth` within `data.txt`

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit7`. The `ls` command is used to confirm that `data.txt` exists:

```
bandit7@bandit:~$ ls -l
total 4088
-rw-r----- 1 bandit8 bandit7 4184396 Sep 19 07:08 data.txt
bandit7@bandit:~$
```

That big number `4184396` is the number of bytes in the file. The `ls` command
also has a `-h` flag that converts it to a human-readable number:

```
bandit7@bandit:~$ ls -lh
total 4.0M
-rw-r----- 1 bandit8 bandit7 4.0M Sep 19 07:08 data.txt
bandit7@bandit:~$
```

Four megabytes of data is a lot to look through line by line to find the word
`millionth`. The command `grep` was used in the previous challenge, so maybe it
is helpful here:

```
bandit7@bandit:~$ grep millionth data.txt
millionth	[REMOVED: BANDIT8 PASSWORD]
bandit7@bandit:~$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit8` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit7@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit8@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit8@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit8@bandit:~$
```

## Key Takeaways

This challenge uses the `grep` command, which is a great tool for finding known
strings in files.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

In the solution above the file wasn't even examined. What does it look like?

```
bandit7@bandit:~$ cat data.txt
momentary	MBLQ2x4SPU4Y6XIscWooXopjdSntWOhY
vicuña	6nKKKgzHbJvPFsEFQgzd2wqJWcv8TGGQ
equities	ZhOy86fNIP8sWsOLLYiHrtjRsrpu1bND
various	Eg1ZcmYmpvkXS10Vu04areb2hhT9Pkft
redefinition's	vPzYXGDGwByIVBRIKQDRHn5xqoekZKME
Allison	4JPUMGRznD4JAyy1SX2Cf5zAwEhT7AP7
compels	8XgWaEyaUVmm1FLZksXE6vRBAKfm7xGB
misstep	0p0wfzDrUfyAbU6V5MVGlrvDKjmc6a0Z
coagulating	Ff0C46bfOMzwOojIDTWJAq9O59WdKSdw
Onega's	YiR7TkXXHKpt0Oqs2EtFzRSXu8XGCqQA
...SNIP...
```

So it looks like a keyword then a tab, and then a password. The `grep` command
is the clear winner here! Something like `awk` could be used, but that's a more
complex tool to use.

```
bandit7@bandit:~$ awk /millionth/ data.txt
millionth	[REMOVED: BANDIT8 PASSWORD]
bandit7@bandit:~$
```

Since the data in the file is in a random order, to visually scan for the word
`millionth` would involve looking at every line. It would be much easier if the
data was in alphabetical order:

```
bandit7@bandit:~$ sort data.txt
	2BujrOE5SK0phlacrV5vV1NGL7WcNbxl
Aachen	2yNZFLlP4m9pQCMpfbMniFiYS6SPYYHk
Aachen's	sixxTyGODFSalVr6S0pLA77UpQllpAyT
Aaliyah	8kXw1Uy3foVPh1UGt9foJg4uSSLsxvB5
Aaliyah's	O1EcqLTmkbuxuy5hzbpUpAb9ghqvP0eX
aardvark	iQP6yyqd74qGMAmGDVdUXgzabSwPRVbF
aardvark's	CWEEUibko34AZC1hC0mQK6r6jJAhax7Z
aardvarks	SXXDuvSHdgXiZuveaqATkXuPbjNnTlKG
Aaron's	iWT5QBaFjCaHxjb5sW1MxEgn356vaz18
Aaron	U4cr1d0o8h8V3GyzObNOa8aMbm6GvI3B
...SNIP...
```

It would still be tedious to scroll through this, but easier than looking at
every line.
