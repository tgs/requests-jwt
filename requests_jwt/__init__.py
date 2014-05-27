from __future__ import unicode_literals
import requests
import hashlib
from requests.auth import AuthBase
import time
import jwt


payload_method = lambda req: req.method
payload_path = lambda req: req.path_url


def payload_body(req):
    if req.method in ('POST', 'PUT'):
        #import pdb; pdb.set_trace()
        return {
                'hash': hashlib.sha256(req.body.encode('utf-8')).hexdigest(),
                'alg': 'sha256',
                }


class JWTAuth(AuthBase):
    """
    An Authorization/Authentication system for :mod:`requests`, implementing
    JSON Web Tokens.

    The basic usage is this:

        auth = JWTAuth(secret)
        resp = requests.get('http://example.com/', auth=auth)

    You can add fields to the signed payload using the expire() and add_field() methods.

    This is a 'Custom Authentication' mechanism for Kenneth Reitz's Requests
    library; see the example in the docs for some context:
    http://docs.python-requests.org/en/latest/user/advanced/#custom-authentication

    For more on JSON Web Tokens, see
    http://self-issued.info/docs/draft-ietf-oauth-json-web-token.html

    See the documentation of `PyJWT` for the list of available
    algorithms.
    """
    def __init__(self, secret, alg='HS256'):
        self.secret = secret
        self.alg = alg
        self._generators = {}

    def add_field(self, name, generator):
        """
        Add a field to the JWT payload.

         - name: The name of the field.  Should be a string.
         - generator: a value or generator, the value of the field.

        If `generator` is callable, then each time a request is made with
        this JWTAuth, the generator will be called with one argument:
        a `PreparedRequest` object.  See this page for a list of the
        available properties:
        http://docs.python-requests.org/en/latest/api/#requests.PreparedRequest

        For instance, here is field that will have your JWT sign the path that
        it is requesting:

            auth.add_field('path', lambda req: req.path_url)

        If `generator` is not callable, it will be included directly in the
        JWT payload.  It could be a string or a JSON-serializable object.
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
    
        request.headers['Authorization'] = 'JWT token="%s"' % token.decode('ascii')
        return request
