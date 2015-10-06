About
=====
An angularJS-friendly Python framework, designed to work with one-page applications

Basic Usage
===========
```Python
from wutu import Wutu
app = Wutu(index="index.html")

@app.create_module
def greetings_module():
	return {"get": lambda req, id: "Hello, #{0}".format(id)}

app.run(host="localhost", port=5555)
```

It creates endpoint `GET /create_modules/<id>` on `http://localhost:5555`. Also, it creates `AngularJS` service called `GreetingsModuleService` which implements all the basic http requests to this module.

Version History
===============
...

