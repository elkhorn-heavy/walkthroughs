# RingZer0 CTF: Client side validation is bad!

- Category: JavaScript
- Points: 1

## The Scene

![Index Page](00_index_page.png)

The screen greets with a facade: username, password, and a big green button that whispers _security theater_.

A glance beneath the curtain (View Source) reveals the real act:

```html
<form action="" method="post">
  <label>Username</label>
  <input
    class="form-control"
    type="text"
    name="username"
    id="cuser"
    placeholder="Username"
  />

  <label>Password</label>
  <input
    class="form-control"
    type="password"
    name="password"
    id="cpass"
    placeholder="Password"
  />

  <input
    type="submit"
    style="margin-top: 12px;"
    value="Login"
    class="c_submit form-control btn btn-success"
  />
</form>
```

And tucked inside a `<script>` tag, something juicier than breakfast whiskey:

```javascript
<script>
// Look's like weak JavaScript auth script :)
$(".c_submit").click(function(event) {
  event.preventDefault()
  var u = $("#cuser").val();
  var p = $("#cpass").val();
  if (u == "admin" && p == String.fromCharCode(74,97,118,97,83,99,114,105,112,116,73,115,83,101,99,117,114,101)) {
    if (document.location.href.indexOf("?p=") == -1) {
      document.location = document.location.href + "?p=" + p;
    }
  } else {
    $("#cresponse").html("<div class='alert alert-danger'>Wrong password sorry.</div>");
  }
});
</script>
```

The real password check happens entirely client-side - like leaving the keys taped to the front door and whispering "_don't tell anyone._"

`String.fromCharCode` is the suspiciously clean window through which to peek: a list of numbers disguised as rigor[^1].

Fire up a Node in the shell:

```
$ node -e 'console.log(String.fromCharCode(74,97,118,97,83,99,114,105,112,116,73,115,83,101,99,117,114,101))'
JavaScriptIsSecure
```

Welcome to the answer[^2].

## Reflections from the Console:

- The form never actually submits to the server - `.preventDefault()` interrupts the usual dance[^3].

- Instead, the script compares the input directly against a hardcoded username and a JavaScript-built password[^4].

- The password isn't even obfuscated cleverly - it's just character codes for `JavaScriptIsSecure`[^5].

- If matched, it redirects the user to the same page with `?p=JavaScriptIsSecure` in the URL[^6].

- Any other input causes a red error box to flash like a cheap motel vacancy sign[^7].

- There's no backend check, no server-side logic - this is smoke and mirrors[^8].

---

[^1]: ASCII codes, baby. `String.fromCharCode(74)` = `J`, `97` = `a`, etc. A long-winded way to spell `JavaScriptIsSecure` without typing it directly.
[^2]: And, of course, the final redirect includes the password in plaintext in the URL. Always nice when things are gift-wrapped.
[^3]: `event.preventDefault()` is JavaScript's way of saying, "Don't do the normal thing." In this case, it blocks the form submission.
[^4]: If the username isn't `admin` or the password isn't the exact match, no dice. That's it. No crypto. No hash. Just strings.
[^5]: This kind of obfuscation might fool someone glancing at code, but any curious attacker will try running it.
[^6]: This behavior hints at how the challenge checks the solution - the URL itself probably gets parsed by the server.
[^7]: UX designed by a hungover intern. A `<div>` just appears with "Wrong password sorry."
[^8]: Classic example of why client-side validation can't be trusted. The browser is the attacker's playground.
