"""
Test utils.

.. currentmodule:: tests.utils
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>

This module provides utilities for unit tests.
"""


from base64 import b64encode, b64decode
from hashlib import md5
from requests import (
    head as requests_head,
    get as requests_get,
    post as requests_post
)

from requests.structures import CaseInsensitiveDict
from urllib.parse import quote
from unittest.mock import patch
import json
import os
import requests


def mock_http(app, context="test"):
    # pragma: no cover
    """
    HTTP test method decorator.

    A function decorator that mocks `requests` HEAD and GET
    requests. If a fixture hasn't been created for the test, it
    will be created and saved as a JSON file. Future calls will
    return the JSON fixture.
    """

    class Response(object):
        def __init__(self, **kwargs):
            self.status_code = kwargs.pop("status_code")
            self.headers = CaseInsensitiveDict(
                kwargs.pop("headers")
            )

            self.content = b64decode(kwargs.pop("body"))
            self.url = kwargs.pop("url")

        def raise_for_status(self):
            msg = ""

            if 400 <= self.status_code < 500:
                msg = f"{self.status_code} Client Error for url: {self.url}"

            elif 500 <= self.status_code < 600:
                msg = f"{self.status_code} Server Error for url: {self.url}"

            if msg:
                raise requests.HTTPError(msg, response=self)

        def iter_content(self, chunk_size):
            yield self.content

        def json(self):
            return json.loads(self.content)

    def mock(func, url, **kwargs):
        hashable = url
        params = kwargs.get("params", {})

        if any(params):
            hashable += "?"

            for key in sorted(params.keys()):
                hashable += "%s=%s&" % (
                    quote(str(key)),
                    quote(str(params[key]))
                )

            hashable = hashable[:-1]

        if headers := kwargs.get("headers", {}):
            hashable += " headers="
            for key in sorted(headers.keys()):
                hashable += "%s=%s&" % (
                    quote(str(key.lower())),
                    quote(str(headers[key]))
                )

        basename = "%s_%s_%s.json" % (
            context,
            func.__name__,
            md5(hashable.encode("utf-8")).hexdigest()
        )

        parts = [os.path.dirname(__file__)]

        if app:
            parts.extend(app.split("."))

        parts.append("fixtures")
        os.makedirs(os.path.join(*parts), exist_ok=True)
        parts.append(basename)
        filename = os.path.join(*parts)

        if not os.path.exists(filename):
            response = func(url, **kwargs)
            data = {
                "headers": dict(response.headers),
                "status_code": response.status_code,
                "body": b64encode(response.content).decode("utf-8"),
                "url": response.request.url,
                "method": response.request.method
            }

            with open(filename, "w") as f:
                json.dump(data, f, indent=4)

        with open(filename, "r") as f:
            data = json.load(f)

        return Response(**data)

    def mock_head(url, **kwargs):
        return mock(requests_head, url, **kwargs)

    def mock_get(url, **kwargs):
        return mock(requests_get, url, **kwargs)

    def mock_post(url, **kwargs):
        return mock(requests_post, url, **kwargs)

    def func(fn):
        fn = patch("requests.head", mock_head)(fn)
        fn = patch("requests.get", mock_get)(fn)
        fn = patch("requests.post", mock_post)(fn)
        return fn

    return func
