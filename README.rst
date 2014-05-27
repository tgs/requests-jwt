requests-jwt
=============

This package allows for HTTP authentication using `JSON Web Tokens
<http://self-issued.info/docs/draft-ietf-oauth-json-web-token.html>`_.

.. image:: https://api.travis-ci.org/tgs/requests-jwt.svg
   :target: https://travis-ci.org/tgs/requests-jwt

.. image:: https://coveralls.io/repos/tgs/requests-jwt/badge.png
   :target: https://coveralls.io/r/tgs/requests-jwt

Usage
-----

``JWTAuth`` extends requests ``AuthBase``, so usage is simple:

.. code:: python

    import requests
    from requests_jwt import JWTAuth

    auth = JWTAuth('secretT0Ken')
    requests.get("http://jwt-protected.com", auth=auth)

More documentation is available at `Read the Docs <http://requests-jwt.rtfd.org>`_.

Installation
------------

    pip install requests_jwt

Requirements
------------

- requests_
- PyJWT_

.. _requests: https://github.com/kennethreitz/requests/
.. _PyJWT: https://github.com/progrium/pyjwt
