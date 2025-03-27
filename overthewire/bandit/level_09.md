# OverTheWire - Bandit - Level 9

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> The Bandit wargame is aimed at absolute beginners. It will teach the basics
> needed to be able to play other wargames.

## Challenge Overview

The goal of this challenge is to look in the file `data.txt` to find the only
line that occurs one time - this is the password.

Then use `ssh` to log into the server as the `bandit9` user.

## Commands Used to Solve This Challenge

- `ls`: list directory contents
- `sort`: sort lines of text files
- `ssh`: OpenSSH remote login client
- `uniq`: report or omit repeated lines

## Initial Analysis

Going to guess that this is a large file and has plenty of duplicate lines. This
challenge mentions the `sort` and `uniq` commands, which will be useful.

The information from the previous challenge is used to `ssh` into the server.

## Understanding the Challenge

It appears that the goal is to learn the new commands `sort` and `uniq` to
search the file.

## Approach Strategy

1. Log in using `ssh`
1. Use `ls` to locate `data.txt`
1. Use `sort` and `uniq` to find the only unrepeated line

## Step-by-Step Solution

The login information from the previous challenge is used to get a shell as user
`bandit8`. The `ls` command is used to confirm that `data.txt` exists:

```
bandit8@bandit:~$ ls -l
total 36
-rw-r----- 1 bandit9 bandit8 33033 Sep 19 07:08 data.txt
bandit8@bandit:~$
```

This file is only 33033 bytes long, so how hard can it be to just visually
search through it?

```
bandit8@bandit:~$ cat data.txt
aMKlTMrptUxxTypCHocCTrqYRkR2gT8h
PRerp5EfTVxJHKuCZDXfAfRyCQSdPjMi
0BKVRLEJQcpNx8wnSPxDLFnFKlQafKK6
6Boy6esAjnIxCYn8uI6KZ7VD7zysDM8i
tgHSfEXcbYCejWXfsWDO4VXXbqtTVcqS
KZJOZECxhLxDhxDbGzdNy8m0uplzvP11
w6x5XtaoRWDqMCsYxgZIWuOKVdiGByAu
0kJ7XHD4gVtNSZIpqyP1V45sfz9OBLFo
Wr4hWlUhGCKJpGDCeio8C1pLVt7DZm3X
Su9w1lri9UACf53cL1evAMKXVgI0nfqe
...SNIP...
```

Oh boy, that would not be a good approach.

The man page for `uniq` says that it will filter _adjacent_ matching lines. So
the data first needs to be sorted:

```
bandit8@bandit:~$ sort data.txt
0BKVRLEJQcpNx8wnSPxDLFnFKlQafKK6
0BKVRLEJQcpNx8wnSPxDLFnFKlQafKK6
0BKVRLEJQcpNx8wnSPxDLFnFKlQafKK6
0BKVRLEJQcpNx8wnSPxDLFnFKlQafKK6
0BKVRLEJQcpNx8wnSPxDLFnFKlQafKK6
0BKVRLEJQcpNx8wnSPxDLFnFKlQafKK6
0BKVRLEJQcpNx8wnSPxDLFnFKlQafKK6
0BKVRLEJQcpNx8wnSPxDLFnFKlQafKK6
0BKVRLEJQcpNx8wnSPxDLFnFKlQafKK6
0BKVRLEJQcpNx8wnSPxDLFnFKlQafKK6
...SNIP...
```

That looks like it is working. Now it can be piped into `uniq` using the `-u`
flag to only print unique lines:

```
bandit8@bandit:~$ sort data.txt | uniq -u
[REMOVED: BANDIT9 PASSWORD]
bandit8@bandit:~$
```

To confirm that the password is correct, disconnect from the server and then
reconnect using the `bandit9` user and the found password (`/etc/issue` and
`/etc/motd` removed):

```
bandit8@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
$ ssh bandit9@bandit.labs.overthewire.org -p 2220
[REMOVED: /etc/issue]
bandit9@bandit.labs.overthewire.org's password:
[REMOVED: /etc/motd]
bandit9@bandit:~$
```

## Key Takeaways

The `sort` and `uniq` commands are good to know when files need to be processed.

## Beyond the Flag

It's good practice to solve things in different ways. What are some other ways
to solve this challenge?

Reading the man page for `uniq`, the `-c` flag provides a count:

```
bandit8@bandit:~$ sort data.txt | uniq -c
     10 0BKVRLEJQcpNx8wnSPxDLFnFKlQafKK6
     10 0eJPctF8gK96ykGBBaKydhJgxSpTlJtz
     10 0kJ7XHD4gVtNSZIpqyP1V45sfz9OBLFo
     10 0lPOvKhpHZebxji0gdjtGCd5GWiZnNBj
     10 0REUhKk0yMqQOwei6NK9ZqIpE5dVlWWM
     10 1jfUH1m4XCjr7eWAeleGdaNSxFXRtX0l
     10 1VKPEkd0bCtIRwMFVQfY7InulwOFyDsn
     10 2u8fvAzvnaFlvQG3iPt4Wc1TFhPcGxhH
     10 35l6mr3f6TvlJyDwU6aUgJX07cLhr6t9
     10 3FIgajXBiaQAiTMVGo1gxRDSiACNyvvJ
...SNIP...
```

Now `grep` for the one with a single occurrence:

```
bandit8@bandit:~$ sort data.txt | uniq -c | grep " 1 "
      1 [REMOVED: BANDIT9 PASSWORD]
bandit8@bandit:~$
```
