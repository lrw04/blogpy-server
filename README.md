# blogpy-server

blogpy-server is a server for blog.py blogs hosted on GitHub. In particular, to be used with this server, the repository must contain `blog.py` in its root.

## Running

First build the image:

```
$ docker build -t blogpy-server .
```

Then run the image, specifying the URL of the repository (if private, add the credentials in the URL) and the webhook secret:

```
$ docker run -d -p 80:80 -p 81:81 -e 'REPO=https://github.com/user/repo' -e SECRET=secret blogpy-server
```

In the command above, port 80 is bound to the blog web page and port 81 to the webhook handler (the endpoint is `/postreceive`).
