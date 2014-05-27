requests-jwt
=============

This package allows for HTTP authentication using `JSON Web Tokens
<http://self-issued.info/docs/draft-ietf-oauth-json-web-token.html>`_.

Usage
-----

``JWTAuth`` extends requests ``AuthBase``, so usage is simple:

.. code:: python

    import requests
    from requests_jwt import JWTAuth

    auth = JWTAuth('secretT0Ken')
    requests.get("http://jwt_protected.com", auth=auth)

Installation
------------

    pip install requests_jwt

Requirements
------------

- requests_
- PyJWT_

.. _requests: https://github.com/kennethreitz/requests/
.. _PyJWT: https://github.com/progrium/pyjwt