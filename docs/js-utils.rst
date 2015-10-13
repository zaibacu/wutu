JavaScript Utils
================
`AngularJS` is an awesome framework, but in the end it still lacks some utilities.
Most of them are that way by design - to force users write clean code, and make creators' life easier.
However, `Wutu` aims at fast and easy start, so these utilities can make you start faster.
In the end, user is fully allowed to write proper `AngularJS` code...

Promise unwrap
--------------
`AngularJS` once had this feature (it was removed after 1.2 version), it is very handy,
but produces a lot of pain for `AngularJS` developers and some confusion for the users.
This unwrapping is done in other way, thus removing part of problems, but is not as comfortable to use.

.. code-block:: html

	<unwrap promise="some_function()">
		<span>{{ data.content }}</span>
	</unwrap>

If we assume, that `some_function` does a http call and returns dictionary with parameter called `content`,
this would certainly work. Keep in mind, that this will make page execute those promise statements on page load.
To avoid that, it is possible to use `ng-if` mechanism (if element is not visible - at the start - it is not executed).
