from __future__ import unicode_literals
import requests
import hashlib
from requests.auth import AuthBase
import time
import jwt


__all__ = [
        'JWTAuth',
        'payload_method',
        'payload_path',
        'payload_body',
        ]


payload_method = lambda req: req.method
"""
A generator that will include the request method in the JWT payload.

>>> auth = JWTAuth('secret')
>>> auth.add_field('method', payload_method)
"""


payload_path = lambda req: req.path_url
"""
A generator that will include the request's path ('/blah/index.html') in the
JWT payload.

>>> auth = JWTAuth('secret')
>>> auth.add_field('path', payload_path)
"""


def payload_body(req):
    """
    A generator that will include the sha256 signature of the request's body
    in the JWT payload.  This is only done if the request could have a body:
    if the method is POST or PUT.

    >>> auth = JWTAuth('secret')
    >>> auth.add_field('body', payload_body)
    """
    to_hash = req.body if type(req.body) is bytes else req.body.encode('utf-8')

    if req.method in ('POST', 'PUT'):
        return {
                'hash': hashlib.sha256(to_hash).hexdigest(),
                'alg': 'sha256',
                }


class JWTAuth(AuthBase):
    """
    An Authorization/Authentication system for :mod:`requests`, implementing
    JSON Web Tokens.

    The basic usage is this:

    .. code::

        auth = JWTAuth(secret)
        # Maybe add more fields to the payload (see below)
        resp = requests.get('http://example.com/', auth=auth)

    You can add fields to the signed payload using the :meth:`expire` and
    :meth:`add_field` methods.

    This is a 'Custom Authentication' mechanism for Kenneth Reitz's Requests
    library; see the `example in the docs
    <http://docs.python-requests.org/en/latest/user/advanced/#custom-authentication>`_
    for some context.

    For more on JSON Web Tokens, see `the standard
    <http://self-issued.info/docs/draft-ietf-oauth-json-web-token.html>`_.

    See the documentation of :mod:`PyJWT` for the list of available
    algorithms.
    """
    def __init__(self, secret, alg='HS256', header_format='JWT token="%s"'):
        self.secret = secret
        self.alg = alg
        self._header_format = header_format
        self._generators = {}

    def add_field(self, name, generator):
        """
        Add a field to the JWT payload.

         - name: The name of the field.  Should be a string.
         - generator: a value or generator, the value of the field.

        If `generator` is callable, then each time a request is made with
        this JWTAuth, the generator will be called with one argument:
        a `PreparedRequest` object.  See `this page`_ for a list of the
        available properties:

        .. _`this page`: http://docs.python-requests.org/en/latest/api/#requests.PreparedRequest

        For instance, here is field that will have your JWT sign the path that
        it is requesting:

        .. code::

            auth.add_field('path', lambda req: req.path_url)

        If `generator` is not callable, it will be included directly in the
        JWT payload.  It could be a string or a JSON-serializable object.

        This module provides several payload fields ready to go:
        :func:`payload_method`, :func:`payload_path`, and :func:`payload_body`.
        :meth:`expire` is also a wrapper around ``add_field``.
        """
        self._generators[name] = generator

    def expire(self, secs):
        """
        Adds the standard 'exp' field, used to prevent replay attacks.

        Adds the 'exp' field to the payload.  When a request is made,
        the field says that it should expire at now + `secs` seconds.

        Of course, this provides no protection unless the server reads
        and interprets this field.
        """
        self.add_field('exp',
                lambda req: int(time.time() + secs))

    def set_header_format(self, new_format):
        """
        Modify the contents of the ``Authorization:`` header.  This must
        be a format string with one ``%s`` in it.
        """
        self._header_format = new_format

    def _generate(self, request):
        """
        Generate a payload for the given request.
        """
        payload = {}
        for field, gen in self._generators.items():
            value = None
            if callable(gen):
                value = gen(request)
            else:
                value = gen

            if value:
                payload[field] = value
        return payload

    def __call__(self, request):
        """
        Called by requests when a request is made.

        The `request` parameter is a PreparedRequest object.

        Prepares the payload using the field generators, and then
        adds an `Authorization` header to the request.
        """
        payload = self._generate(request)
        #import pdb; pdb.set_trace()
        token = jwt.encode(payload, self.secret, self.alg)
    
        request.headers['Authorization'] = self._header_format % token.decode('ascii')
        return request
