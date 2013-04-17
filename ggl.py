import logging
import os
import webapp2
import json
from google.appengine.ext.webapp import template
from google.appengine.api import users
from functools import wraps

class RouteRegister(object):
    """Register urls and functions and build webapp2.RequestHandler's for them"""

    urls = []
    reverse_mapping = {}

    @classmethod
    def add_url(cls, url, function, method):
        """Register an URL"""

        def render_json(self, obj):
            """Render a json string of the given object"""
            json_str = json.dumps(obj)
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json_str)

        def render(self, template_file, **values):
            """Render the template"""
            self.response.out.write(template.render(template_file, values))

        def func_helper(func):
            """Extract the url query-string and put it into kwargs"""
            def wrapper(context, *args, **kwargs):
                query = context.request
                queries = dict((q, query.get(q)) for q in query.arguments())
                logging.info("query: " + str(queries))
                return func(context, *args, **queries)
            return wrapper

        RouteRegister.reverse_mapping[function.__name__] = url
        klass_name = "URL_{0}".format(len(RouteRegister.urls))
        klass = type(klass_name, (webapp2.RequestHandler,), {method:func_helper(function), "render":render, "render_json":render_json,})
        RouteRegister.urls.append((url, klass))
        logging.info("CLASS:'{5}' URL:'{0}' METHOD:'{1}' FUNCTION:'{2}' FILE:'{3}' LINE:{4}".format(url, method, function.__name__, function.func_code.co_filename, function.func_code.co_firstlineno, klass_name))

def login(context, return_url="/"):
    """Force the user to log in."""
    login_url = users.create_login_url(return_url)
    context.render("templates/login.html", login_url=login_url, )

def force_login(func):
    """Force the user to login with his google-account"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = users.get_current_user()
        context = args[0]
        func_name = func.__name__
        url = get_url_for_func(func_name)
        if not user:
            ### force user login
            login(context, url)
        else:
            ### return function
            context.logout_url = users.create_logout_url(url)
            context.user = users.get_current_user()
            return func(*args, **kwargs)
    return wrapper


def route(url, method="get"):
    "Register a function to an url."
    def wrap(func):
        RouteRegister.add_url(url, func, method.lower())
        def wrap_function(*args, **kwargs):
            return func(*args, **kwargs)
        return func
    return wrap

def get_url_for_func(func):
    """Reverse url-mapper; return the url to a function-name"""
    return RouteRegister.reverse_mapping[func]

def build_app(*args, **kwargs):
    """Return a WSGIApplication"""
    return webapp2.WSGIApplication(RouteRegister.urls, *args, **kwargs)