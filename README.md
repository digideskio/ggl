ggl
===

a tiny google app engine framework, to make your life even easier

## installation
simply check out ggl.py and put it into your google app engine app. The ggl-framework just contains some tiny 
shortcuts. Besides these shortcuts you need to use the standard 
[google app engine framework](https://developers.google.com/appengine/docs/python/overview).

## usage

### routes

```python
### main.py
from ggl import build_app, route

@route("/app")
def app_get(context):
    ### your code here
    context.render("templates/app.html")

app = build_app()
```

```python
### main.py
from ggl import build_app, route


### for /app?name=Marco&year=2013
### query strings will be provided via **kwargs
@route("/app")
def app_get(context, name, year):
    ### your code here
    context.render("templates/app.html")

app = build_app()
```

```python
### main.py
from ggl import build_app, route

@route("/app")
def app_get(context):
    ### your code here
    context.render("templates/app.html")

@route("/app", "post")
def app_post(context):
    ### your code here
    context.render("templates/app.html")

@route("/app", "put")
def app_put(context):
    ### your code here
    context.render("templates/app.html")

@route("/app", "delete")
def app_delete(context):
    ### your code here
    context.render("templates/app.html")

app = build_app()
```



### force users to login with google account

```python
### main.py
from ggl import build_app, route, force_login

@route("/app")
@force_login
def app_get(context):
    """this function will only be accessed when the user 
    has successfully logged into his google account
    and given your application permission to use it"""
    ### your code here
    context.render("templates/app.html")

app = build_app()
```

### reverse - function lookups for redirects
```python
### main.py
from ggl import build_app, route, get_url_for_func

@route("/newcall")
def newcall(context):
    """this function will redirect the request to the url 
    of the function 'app'"""
    ### your code here
    context.redirect(get_url_for_func("app_get"))

@route("/app")
def app_get(context):
    ### ...

app = build_app()
```

## how the backend works
Here is some standard google app engine code:
```python
import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')
    
    def post(self):
        name = self.response.get("name")
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
```
this will map to the following ggl-framework code:
```python
from ggl import build_app, route

@route("/")
def app_get(context):
    context.write('Hello world!')

@route("/", "post")
def app_post(context, name):
    context.write('Hello world!')

app = build_app(debug=True)
```
For each route a "webapp2.RequestHandler" class will be created and receives one class function. This function
exactly mapps to the get/post/put/delete function of the "webapp2.RequestHandler". Also, all query strings will
me mapped to kwargs, so you don't have to go through the context/response-object to get them.

## why I have done this
I have implemented quite a view applications with the [flask framework](http://flask.pocoo.org/) and grew 
quite comfortable with its application design. With just a few lines of code you are up and running.
I also like the (google app engine)[https://developers.google.com/appengine/] project a lot, since it 
basically gives me a cloud instance, running python for free. However, I found the 
[python framework](https://developers.google.com/appengine/docs/python/overview) in parts a bit too heavy
and therefore implemented some short-cuts, which you can find in this project.

If you think I might have missed something or could do things even better please let me know about it and 
send me a github message/bug-report!
