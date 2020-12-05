---
title: The Secret Side to My Static Site
date: May 14, 2020
---

I host this website on github pages which means I don't have access to a server or database. My website is hosted on computers I don't own and is accessible by anyone.

And I want a login service.

Specifically I want a place where I can type in a password and gain access to private information. However, because my site is public and I haven't made a server, I have to be able to do this from any computer.

While I've been thinking about this problem for quite a while, it wasn't until I finished taking a cryptography class at college that I discovered a nice encryption algorithm for this problem: AES.

AES is a secure encryption algorithm where you encrypt data with a key. When you want your data back, you use the key again to decrypt. As far as I know, AES has a long enough key that it hasn't been cracked and it probably won't be cracked any time soon.

From a high level, I use sha256 to hash my password and AES to encrypt and decrypt the contents of my secret web pages. Here's the encryption process:

![encryption process](website-encryption.svg)

The decryption process is very similar, except I use the password hash to decrypt the encrypted website.

Before encryption, my secret website looks like:

```
main.html
other.html
```

When my website is encrypted, the file structure looks as follows:

```
007a69b693fbc1f43f7ce8f4c9779621.html
222e1238c95503abd14586130ee685c1.html
aes.js
landing.html
sha256.js
```

The html files with hex names correspond to `main.html` and `other.html`, and the additional files are libraries to help decrypt the pages. These file names are randomly generated hex strings and have no connection to the file's name or contents which makes it harder for people to get any information from even the file structure.

`aes.js` and `sha256.js` are encryption libraries I found online and `landing.html` is the webpage through which you access the private site.

My claim is that it is very hard to decode the webpages without the password.

For example, this is what `007a69b693fbc1f43f7ce8f4c9779621.html` looks like:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Encrypted Page</title>
    <script type="text/javascript" src="aes.js"></script>
  </head>
  <body>
    <script type="text/javascript">
      const page =
        "42df955a2a180ffdc2da342c5ab550524ba3a28cbb99cf1f1f13d57e338b8e480d7ad11a716239cad703a54a06a78ffcbccda81f69f1732f365fdc7cc6eed9fc8bd8d2535a4e7b78956a8dd6239e052e29fa96564c69218c0212cf4ad5dcb7d3727e1bf18dc93b10bf7e9408ee8c1206761540d25320294f0ae0a05ce5dee27b56b3c703dded0be07528c3f6013792fc34005e6bcd6c5d19220cb30ca83764aa13f16c056e711ade30ee55dab8dae42a172ebcbc3a9cec3f9ee30934264c8c20a5208ae1157567672d103ab7ddd6ef236c6a65959a7b6f91ca4814a51fdcace10d95b26b62c19c7c3afa70e2b1b05435c9cbe5e72c25b05e7a136fb1d075b7df447819244237b0c23c6ae79b39da3c5c0654b7a95a82d1be6f81a9c2cd5531fc";
      window.onload = () => {
        const url = window.location.href;
        const hexKey = window.localStorage.getItem("password hash");
        console.assert(hexKey !== null);
        console.assert(hexKey.length == 32);
        const byteKey = aesjs.utils.hex.toBytes(hexKey);
        const aes = new aesjs.ModeOfOperation.ctr(
          byteKey,
          new aesjs.Counter(1)
        );
        const pageBytes = aesjs.utils.hex.toBytes(page);
        const decryptedBytes = aes.decrypt(pageBytes);
        const decryptedPage = aesjs.utils.utf8.fromBytes(decryptedBytes);
        document.body.innerHTML = decryptedPage;
      };
    </script>
  </body>
</html>
```

It's pretty hard to tell that hex string decrypts into the following page.

```html
<html><head>
  <meta charset="UTF-8">
  <title>Encrypted Page</title>
  <script type="text/javascript" src="aes.js"></script>
</head>
<body><h1>Main Page</h1>
<p>Welcome to the ecnrypted page!</p>
<p>You are here because you managed to type in the correct password.</p>
<p>Here's a link to the <a href="222e1238c95503abd14586130ee685c1.html>other page</a>.</p>
</body></html>
```

When the page loads, it uses the hashed+salted password stored in `window.localStorage` to decrypt the page contents and sets the decrypted message as the body's innerHTML.

# The Landing Page

`landing.html` is very similar except it only stores the encrypted url of the first secret page.

To get the first link, the landing page:

1. gets the first 128 bits of the sha256 of the password and a random salt.
2. uses those bits as an AES key to decrypt the link.
3. stores the hashed+salted password in `window.localStorage`

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Encrypted Page</title>
    <script type="text/javascript" src="aes.js"></script>
    <script type="text/javascript" src="sha256.js"></script>
  </head>
  <body>
    <script type="text/javascript">
      const link = "7f8dbd40a7dac976d04169bafa678c2b";
      const salt = "0e12d61a450492ec3600cc70fddb051e";
      function login() {
        const pass = document.getElementsByTagName("input")[0].value;
        const m = sha256.create();
        m.update(pass);
        m.update(salt);
        const hexPass = m.hex().substr(0, 32);
        window.localStorage.setItem("password hash", hexPass);
        const byteKey = aesjs.utils.hex.toBytes(hexPass);
        const aes = new aesjs.ModeOfOperation.ctr(
          byteKey,
          new aesjs.Counter(1)
        );
        const linkBytes = aesjs.utils.hex.toBytes(link);
        const decryptedLink = aesjs.utils.hex.fromBytes(aes.decrypt(linkBytes));
        const url = `${decryptedLink}.html`;
        window.location.href = url;
      }
      window.onload = () => {
        const input = document.getElementsByTagName("input")[0];
        input.addEventListener("keydown", (event) => {
          if (event.key === "Enter") {
            login();
          }
        });
      };
    </script>
    <h3>Password:</h3>
    <input type="password" />
    <div>
      <button onclick="login()">Click to login</button>
    </div>
  </body>
</html>
```

If you want to give it a try, here's [the landing page](/secret) and the password is `pass`.

# Restrictions and Future Ideas

The main restriction of this setup is it only works for one user. I'm sure there are algorithms that support multiple passwords but at that point it would make sense to switch to a dedicated password service.

**Pro**: The password isn't stored and the hashed password never even leaves your computer.

**Con**: If a malicious person gets a hold of a computer with the hashed password in localstorage, they can use it to access secret webpages.

**Pro**: That malicious person can't get the original password.

**Pro**: I can regenerate the website which generates a new random salt and invalidates all current logins.

This setup means I can go on a random computer and browse my secret site in igcognito mode. When I close the browser, localstorage clears and I probably won't leave a trace.

**Con**: The title of secret pages always says "Encrypted Page". I could fix this by encrypting the page title along with page contents and it would probably be more secure to encrypt them together. Maybe json would be a good encoding format.

**Pro**: On the other hand, it is kinda cool that the page appears as "Encrypted Page" in my browser history.

Now that I have an AES-secured secret site, I'm not sure what to do with it. Maybe I'll host some e-books I'm reading, or posts I'm working on, or a journal, or a todo list.

But whatever it is, I think it'll be secure.
