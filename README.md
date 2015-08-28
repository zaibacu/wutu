About
=====
A fusion between AngularJS and Python Flask

Basic Usage
===========
```Python
from wutu import app
from wutu.util import current
myapp = app.create(index="index.html", locator=current)

@create_module(testing_app.api)
def greetings_module():
	return {"get": lambda req, id: "Hello, #{0}".format(id)}

myapp.run(host="localhost", port=5555)
```

It creates endpoint `GET /create_modules/<id>` on `http://localhost:5555`. Also, it creates `AngularJS` service called `GreetingsModuleService` which implements all the basic http requests to this module.

Version History
===============
0.0.1 on 2015.08.28
* First initial version made possible to use in development

