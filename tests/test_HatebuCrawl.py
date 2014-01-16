#!/usr/bin python
# -*- coding: utf-8 -*-

def pytest_generate_tests(metafunc):
    """
    Parametrizing test methods through per-class configuration
    http://pytest.org/latest-ja/example/parametrize.html#id5
    """
    try:
        funcarglist = metafunc.cls.params[metafunc.function.__name__]
    except AttributeError:
        return
    argnames = list(funcarglist[0])
    metafunc.parametrize(
        argnames,
        [[funcargs[name] for name in argnames] for funcargs in funcarglist]
    )

class HatebuCrawlTest(object):
    def test_getFavorites(self):
        from HatebuCrawl import HatebuCrawl
        hc = HatebuCrawl("wata88")
        assert hc.test_getFavorites() == ""