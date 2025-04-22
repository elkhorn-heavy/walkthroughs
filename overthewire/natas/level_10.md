# OverTheWire - Natas - Level 10

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> Natas teaches the basics of serverside web-security.

## Challenge Overview

After discovering the `natas10` password in the previous challenge, it can be
used to log into http://natas10.natas.labs.overthewire.org:

![The Index Page](images/level_10/00_index_page.png)

## Initial Analysis

This looks very similar to the previous challenge except that there is new text
saying:

> For security reasons, we now filter on certain characters

The prompt is the same

> Find words containing:

There's an input box for entering the "words". There is also a `View sourcecode`
link that seems like a hint.

## Approach Strategy

1. Click the `View sourcecode` link
1. The code has probably been tightened up a bit but see if it can be
   exploited

## Step-by-Step Solution

Clicking the `View sourcecode` link shows the source code for the web page. The
passwords are censored, but the PHP code for the page is shown:

![Index Source Code](images/level_10/01_index_source_code.png)

This code is very similar to the previous challenge. Some formatting and
comments help to understand what this PHP code is doing:

```php
// Initialize the "$key" variable to the empty string.
$key = "";

// The "$_REQUEST" is all the input parameters in the HTTP request. So this will
// check to see if the "needle" parameter is defined. The form on this page has
// an input named "needle", so this checks if the user has submitted a value.
if (array_key_exists("needle", $_REQUEST)) {
  // If the user put a value into the input box, then set "$key" to that value.
  $key = $_REQUEST["needle"];
}

// If the "$key" variable has a value - that is, it was entered by the user -
// then run the code within this clause.
if ($key != "") {
  // This is the new code: check if the input contains any of the characters
  // ';', '|', or '&'.
  if (preg_match('/[;|&]/', $key)) {
    // Tell the user that the input can't contain the illegal characters.
    print "Input contains an illegal character!";
  } else {
    // Run the "grep" command in case-insensitive ("-i") mode to look for the
    // value of "$key" in the file "dictionary.txt". Print the output of the
    // grep command.
    passthru("grep -i $key dictionary.txt");
  }
}
```

This code is pretty good, but it doesn't have anything to do with passwords. It
just looks up words in a dictionary and prints anything that matches. Entering
the word `hacker` and clicking the `Search` button displays:

![Search for Hacker](images/level_10/02_hacker_search.png)

If there are no secrets or passwords or anything else in this code, then what is
the solution to the challenge? All this code appears to do is print out words
from a dictionary file. The `$key` used in the `passthru` command now has some
sanitizing of the input: the characters `;`, `|`, and `&` are no longer allowed.
This filter can be tried by tweaking the input from the previous challenge to
print the `natas11` password for this level:
`hacker dictionary.txt; cat /etc/natas_webpass/natas11; grep -i hacker`:

![Illegal Character](images/level_10/03_illegal_character.png)

This is expected as the character `;` is no longer allowed.

The code runs `passthru` with the command:

```
$ grep -i $key dictionary
```

Looking at the `man` page for `grep`, it can also search for regular
expressions. So running `grep . file` would return every line of `file` that has
one or more characters. Combining this with the comment character `#`, the input
string `. /etc/natas_webpass/natas11 #` will run the command:

```
$ grep -i . /etc/natas_webpass/natas11 # dictionary
```

This looks like it will work! Every non-empty line of the `natas11` file will be
printed and then the `#` comment throws away the remainder of the command line:

![The Password](images/level_10/04_password.png)

There it is: the `natas11` password (removed).

## Key Takeaways

- It's important to never trust user input
- It's dangerous to allow user input in commands that execute shell commands
- Input filters have to catch every malicious character - it is better to use a
  list of characters that are safe, rather than try to find every unsafe
  character

## Beyond the Challenge

It's always a good idea to think about other solutions. However, even though
this filter is flawed, it does prevent most attacks.
