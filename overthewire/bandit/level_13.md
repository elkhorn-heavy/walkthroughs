# OverTheWire - Bandit - Level 13

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to retrieve the next password from the file
`data.txt`. This file is a hexdump, and the actual file itself has been
compressed multiple times.

Then use `ssh` to log into the server as the `bandit12` user.

## Commands Used to Solve This Challenge

- `bzip2`: a block-sorting file compressor
- `cat`: concatenate files and print on the standard output
- `cd`: change the shell working directory
- `cp`: copy files and directories
- `file`: determine file type
- `gunzip`: compress or expand files
- `ls`: list directory contents
- `mktemp`: create a temporary file or directory
- `mv`: move (rename) files
- `ssh`: OpenSSH remote login client
- `tar`: an archiving utility
- `xxd`: make a hex dump or do the reverse

## Initial Analysis

This challenge gives the hint that `xxd` will be needed to revert the hexdump.
Then `file` will be used to figure out how to undo the multiple compression
steps.

The information from the previous challenge is used to `ssh` into the
server.

## Understanding the Challenge

It seems that the goal of this challenge is to introduce the idea of archives
and/or compression, as well as hexdumps and basic filesystem commands like `cp`
and `mv`.

## Approach Strategy

1. Log in using `ssh`
1. Use `ls` to locate `data.txt`
1. Use `mktemp` to create a temporary working area
1. Use `cp` to make a copy of `data.txt` in the working area
1. Use `xxd` to revert the hexdump
1. Use `file` to determine the type of file
1. Use uncompression utilities to uncompress the file
1. Use `cat` to display the password

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit12`. The `ls` command is used to confirm that `data.txt` exists:

```
bandit12@bandit:~$ ls -l
total 4
-rw-r----- 1 bandit13 bandit12 2583 Sep 19  2024 data.txt
bandit12@bandit:~$
```

It's a good idea to take a look at the data.

```
bandit12@bandit:~$ cat data.txt | head
00000000: 1f8b 0808 dfcd eb66 0203 6461 7461 322e  .......f..data2.
00000010: 6269 6e00 013e 02c1 fd42 5a68 3931 4159  bin..>...BZh91AY
00000020: 2653 59ca 83b2 c100 0017 7fff dff3 f4a7  &SY.............
00000030: fc9f fefe f2f3 cffe f5ff ffdd bf7e 5bfe  .............~[.
00000040: faff dfbe 97aa 6fff f0de edf7 b001 3b56  ......o.......;V
00000050: 0400 0034 d000 0000 0069 a1a1 a000 0343  ...4.....i.....C
00000060: 4686 4341 a680 068d 1a69 a0d0 0068 d1a0  F.CA.....i...h..
00000070: 1906 1193 0433 5193 d4c6 5103 4646 9a34  .....3Q...Q.FF.4
00000080: 0000 d320 0680 0003 264d 0346 8683 d21a  ... ....&M.F....
00000090: 0686 8064 3400 0189 a683 4fd5 0190 001e  ...d4.....O.....
...SNIP...
```

That certainly does look like a hexdump. Hexdumps are one way to convert a
binary file into something that is _a little_ more readable for humans.

Now to create a temporary working directory, as recommended in the challenge
description. The `mktemp` command will create a temporary file, or with the `-d`
flag will create a temporary directory.

```
bandit12@bandit:~$ mktemp -d
/tmp/tmp.MFlKmHZ1qU
bandit12@bandit:~$
```

The directory is created in `/tmp`, a special directory used for creating
temporary files and directories. It's not meant for longterm storage, but for
this challenge it isn't needed for long.

The `cp` command will copy from "source" to "destination":

```
bandit12@bandit:~$ cp data.txt /tmp/tmp.MFlKmHZ1qU
bandit12@bandit:~$ cd !$
cd /tmp/tmp.MFlKmHZ1qU
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$
```

After copying the file, the `cd` shell command is used to change directory.
There are some things to note here:

- the `!$` shortcut means "the last item of the last command", and saves some
  typing
- the `cd` command is built into the shell, so there is no man page for it, but
  `cd --help` gives usage information
- the shell prompt has replaced the `~` signifying the user's home directory
  with the temporary directory in `/tmp`

After all that setup, it's time to get to work. The `xxd` command has a `-r`
flag to revert a hexdump:

```
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ xxd -r data.txt > data.out
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ ls -l
total 8
-rw-rw-r-- 1 bandit12 bandit12  607 Mar 21 10:17 data.out
-rw-r----- 1 bandit12 bandit12 2583 Mar 21 10:05 data.txt
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$
```

What happened here is that `xxd` will send the reverted hexdump to `stdout`,
which is common for many commands: read from `stdin` and write to `stdout`. To
write this output to a file, the `>` operator is used, and `data.out` is a
made-up filename. One has to be careful that the destination filename doesn't
already exist, though, as it will be overwritten without warning.

That's the first step described in the challenge description. Now to do the
decompression - but how is it compressed?

```
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ file data.out
data.out: gzip compressed data, was "data2.bin", last modified: Thu Sep 19 07:08:15 2024, max compression, from Unix, original size modulo 2^32 574
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$
```

This says that `gzip` compression was used, and that the original filename was
`data2.bin`. A `gzip` file can be decompressed with either `gzip -d` or
`gunzip`.

```
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ gunzip data.out
gzip: data.out: unknown suffix -- ignored
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$
```

One thing about `gzip` is that it is very being picky about the name of the file
being decompressed. The `mv` command is also used to rename files:

```
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ mv data.out data.gz
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ gunzip data.gz
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ ls -l
total 8
-rw-rw-r-- 1 bandit12 bandit12  574 Mar 21 10:17 data
-rw-r----- 1 bandit12 bandit12 2583 Mar 21 10:05 data.txt
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$
```

That's the decompression done. Note that `gunzip` removes the compressed file
and replaces it with the filename minus the `.gz` suffix.

Now to check what kind of file this is:

```
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ file data
data: bzip2 compressed data, block size = 900k
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$
```

It seems that this challenge is going to take us through a bunch of different
compression commands. Decompress this and then see what kind of file it is:

```
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ bzip2 -d data
bzip2: Can't guess original name for data -- using data.out
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ file data.out
data.out: gzip compressed data, was "data4.bin", last modified: Thu Sep 19 07:08:15 2024, max compression, from Unix, original size modulo 2^32 20480
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$
```

And it's back to `gzip` again!

```
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ mv data.out data.gz
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ gunzip data.gz
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ file data
data: POSIX tar archive (GNU)
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$
```

And now it's a `tar` file. This isn't technically compression, but it is a way
to archive files - usually it's used to collect a bunch of files into a single
archive to make them easier to move around. It's always a good idea to list the
contents of a tar file before untarring it.

```
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ tar tf data
data5.bin
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$
```

OK, so it will create a file called `data5.bin`. Now to untar it:

```
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ tar xf data
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ file data5.bin
data5.bin: POSIX tar archive (GNU)
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$
```

Another tar file! Let's untar it and see what it is:

```
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ tar tf data5.bin
data6.bin
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ tar xf data5.bin
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ file data6.bin
data6.bin: bzip2 compressed data, block size = 900k
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ bzip2 -d data6.bin
bzip2: Can't guess original name for data6.bin -- using data6.bin.out
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ file data6.bin.out
data6.bin.out: POSIX tar archive (GNU)
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ tar tf data6.bin.out
data8.bin
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ tar xf data6.bin.out
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ file data8.bin
data8.bin: gzip compressed data, was "data9.bin", last modified: Thu Sep 19 07:08:15 2024, max compression, from Unix, original size modulo 2^32 49
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ mv data8.bin data8.gz
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ gunzip data8.gz
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ file data8
data8: ASCII text
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$ cat data8
The password is [PASSWORD REMOVED]
bandit12@bandit:/tmp/tmp.MFlKmHZ1qU$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit13` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit12@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit13@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit13@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit13@bandit:~$
```

## Key Takeaways

There are many commands for compressing and archiving files, and it's good to
know how to work with them. The `file` command is our friend here.

## Beyond the Flag

It was a little tedious to manually do all the steps to extract the final file.
Shell scripting is a little advanced at this point in the challenges, but a
script that automatically does the repeated steps might come in useful some day.
