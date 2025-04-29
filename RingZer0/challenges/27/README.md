# Client-side validation is bad!

- Category: JavaScript
- Points: 1

## The page:

Login box. Username, password. Green button. No promises.

Looked at the page source - saw this:

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

Nothing happening. Dead HTML. The trap isn't in the form - it's behind it.

Scrolling down, wham:

```javascript
$(".c_submit").click(function (event) {
  event.preventDefault();
  var u = $("#cuser").val();
  var p = $("#cpass").val();
  if (
    u == "admin" &&
    p ==
      String.fromCharCode(
        74,
        97,
        118,
        97,
        83,
        99,
        114,
        105,
        112,
        116,
        73,
        115,
        83,
        101,
        99,
        117,
        114,
        101
      )
  ) {
    if (document.location.href.indexOf("?p=") == -1) {
      document.location = document.location.href + "?p=" + p;
    }
  } else {
    $("#cresponse").html(
      "<div class='alert alert-danger'>Wrong password sorry.</div>"
    );
  }
});
```

That's it. **That's all of it**.

The lock, the key, the map to the house, all taped to the front door.

## How it works

- Form tries to submit? Nope. `preventDefault()` blocks the exit.

- Instead, it checks the username - must be `admin`.

- It builds a password on the fly using `String.fromCharCode()`. ASCII soup.

- If your inputs match their expectations, it hacks the URL and adds `?p=your_password_here`.

- If not? Flashing red "wrong password" - carnival buzzer sound.

## Decoding the Secret

Copy-pasted the numbers straight into Node:

```
$ node -e 'console.log(String.fromCharCode(74,97,118,97,83,99,114,105,112,116,73,115,83,101,99,117,114,101))'
JavaScriptIsSecure
```

Right there in the open.

Right there like a wallet sitting on the curb.

## What Went Wrong (and Why It Matters)

- **Never validate critical credentials client-side.** Ever.

- **Never store secrets in reversible JavaScript operations.** ASCII codes are not encryption.

- **Never assume people won’t look at your source.** They will.

- **Never assume your users are friendly.** They're not - not in CTF land.

Client-side validation is theater.
Server-side validation is law.

## Closing Thoughts

This wasn’t security. This was **security kabuki**.

A smiling mask over hollow bones.

A fairy tale for the bored and the reckless.

Punch through it, laugh, move on.

Challenge complete.
