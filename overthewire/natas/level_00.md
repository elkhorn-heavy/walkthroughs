# OverTheWire - Natas - Level 0

[OverTheWire](https://overthewire.org) offers a series of "wargames" that teach
security skills. From their website:

> Natas teaches the basics of serverside web-security.

## Challenge Overview

The first challenge is the introduction, and the username and password are
provided:

> - Username: natas0
> - Password: natas0
> - URL: http://natas0.natas.labs.overthewire.org

This displays the following web page:

![The main page](images/level_00/00_main_page.png)

## Initial Analysis

The web page instructions are:

> You can find the password for the next level on this page.

Looking around the web page should reveal the next password.

## Approach Strategy

1. Look at the page source to see what is there

## Step-by-Step Solution

Browsers provide a way to look at the "source code" of a web page. For example
in Firefox, right-clicking anywhere on a page brings up a context menu that
includes an item to "View Page Source":

![The Firefox Context Menu](images/level_00/01_context_menu.png)

The page source is the HTML that makes up the page. In this first challenge the
password is very obvious, as it is stored in a comment in the HTML. Note that
the password has been removed in this image:

![The Page Source (password removed)](images/level_00/02_view_source.png)

## Key Takeaways

HTML comments contain data that is not displayed on a web page. These comments
can be a valuable source of information.

## Beyond the Challenge

The "View Page Source" context menu item is one way to see the HTML code for a
web page. Browsers also have "Developer Tools" that can be used to look at the
source for a web page. These tools are also called the "F12 Tools" as the `F12`
key is used to run them:

![Developer Tools (password removed)](images/level_00/03_developer_tools.png)
