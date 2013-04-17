ggl
===

a google app engine framework

## installation
simply check out ggl.py and put it into your google app engine app.

## usage

### routes

```python
### main.py
from ggl import build_app, route

@route("/app")
def app(context):
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
def app(context):
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
    context.redirect(get_url_for_func("app"))

app = build_app()
```
