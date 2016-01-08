About
=====
[![Build Status](https://travis-ci.org/zaibacu/wutu.svg?branch=master)](https://travis-ci.org/zaibacu/wutu)
[![Documentation Status](https://readthedocs.org/projects/wutu/badge/?version=latest)](http://wutu.readthedocs.org/en/latest/?badge=latest)

An angularJS-friendly Python framework, designed to work with one-page applications

Installiation
=============
```bash
pip install wutu
```

Basic Usage
===========
```Python
from wutu import Wutu
app = Wutu(index="index.html")

@app.create_module
def greetings_module():
    hellos = ["Hello", "Hola", "Labas"]
    return {
        "get": lambda req: [{"text": hello} for hello in hellos],
        "get_entity_name": lambda req: "greeting"
    }

app.run(host="localhost", port=5555)
```

It creates endpoint `GET /greetings_module` on `http://localhost:5555`. Also, it creates `AngularJS` service called `GreetingsModuleService` which implements all the basic http requests to this module, and
controller called `GreetingsModuleController` which injects and uses previously created service by default. 

`index.html` may look something like this

```html
<!DOCTYPE html>
<html lang="en" ng-app="wutu">
<head>
    <meta charset="UTF-8">
    <title>test</title>
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/angularjs/1.4.4/angular.min.js"></script>
    <script type="text/javascript" src="/wutu.js"></script>
</head>
<body>
    <div ng-controller="GreetingsModuleController">
        <span ng-repeat="greeting in greeting_list">
            {{ greeting.text }}
        </span>
    </div>
</body>
</html>
```

Version History
===============
0.1
---
    0.1.5 - Use jinja2 for templates rendering
    0.1.4 ... 0.1.1 - various small changes
    0.1.0 - First public version
