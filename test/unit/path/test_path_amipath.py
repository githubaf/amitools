import pytest
from amitools.path.amipath import *


class TestMgr(object):
    assigns = ("a", "b", "c")
    volumes = ("root", "work", "system")

    def is_prefix_name(self, name):
        return name in self.assigns or name in self.volumes

    def is_volume_name(self, name):
        return name in self.volumes

    def is_assign_name(self, name):
        return name in self.assigns

    def contains_multi_assigns(self, name):
        if name == "a":
            return True
        elif name in self.assigns:
            return False
        else:
            return None


class TestEnv(object):

    def get_cur_dir(self):
        return AmiPath("foo:bar")

    def get_mgr(self):
        return TestMgr()


def test_amipath_abs_rel():
    # cur dir "" is default and assumed to be local
    p = AmiPath()
    assert p.is_local()
    assert not p.is_absolute()
    assert not p.is_parent_local()
    assert not p.is_prefix_local()
    # abs
    p = AmiPath("foo:bar")
    assert not p.is_local()
    assert p.is_absolute()
    assert not p.is_parent_local()
    assert not p.is_prefix_local()
    # local
    p = AmiPath("foo/bar")
    assert p.is_local()
    assert not p.is_absolute()
    assert not p.is_parent_local()
    assert not p.is_prefix_local()
    # special local
    p = AmiPath(":bla")
    assert p.is_local()
    assert not p.is_absolute()
    assert not p.is_parent_local()
    assert p.is_prefix_local()
    # parent local
    p = AmiPath("/bla")
    assert p.is_local()
    assert not p.is_absolute()
    assert p.is_parent_local()
    assert not p.is_prefix_local()


def test_amipath_prefix_postfix():
    p = AmiPath()
    assert p.prefix() is None
    assert p.postfix() == ""
    assert p.postfix(True) == ""
    assert AmiPath.build(p.prefix(), p.postfix()) == p
    p = AmiPath("foo:bar/")
    assert p.prefix() == "foo"
    assert p.postfix() == "bar"
    assert p.postfix(True) == "bar"
    assert AmiPath.build(p.prefix(), p.postfix()) == p
    p = AmiPath("foo/bar/")
    assert p.prefix() is None
    assert p.postfix() == "foo/bar"
    assert p.postfix(True) == "foo/bar"
    assert AmiPath.build(p.prefix(), p.postfix()) == p
    p = AmiPath(":bla")
    assert p.prefix() is None
    assert p.postfix() == ":bla"
    assert p.postfix(True) == "bla"
    assert AmiPath.build(p.prefix(), p.postfix()) == p
    p = AmiPath("/bla")
    assert p.prefix() is None
    assert p.postfix() == "/bla"
    assert p.postfix(True) == "bla"
    assert AmiPath.build(p.prefix(), p.postfix()) == p
    p = AmiPath("/")
    assert p.prefix() is None
    assert p.postfix() == "/"
    assert p.postfix(True) == ""
    assert AmiPath.build(p.prefix(), p.postfix()) == p


def test_amipath_valid_syntax():
    assert AmiPath().is_syntax_valid()
    assert AmiPath("foo:bar/").is_syntax_valid()
    assert AmiPath("foo/bar/").is_syntax_valid()
    assert AmiPath(":bla").is_syntax_valid()
    assert AmiPath("/bla").is_syntax_valid()
    # invalid
    assert not AmiPath("//").is_syntax_valid()
    assert not AmiPath(":/").is_syntax_valid()
    assert not AmiPath("bla/foo:").is_syntax_valid()
    assert not AmiPath("bla:foo:").is_syntax_valid()


def test_amipath_valid_prefix_volume_assign():
    mgr = TestMgr()
    # prefix
    assert AmiPath("a:", mgr=mgr).is_prefix_valid()
    assert AmiPath("root:", mgr=mgr).is_prefix_valid()
    assert not AmiPath("foo:", mgr=mgr).is_prefix_valid()
    with pytest.raises(AmiPathError):
        AmiPath("rel").is_prefix_valid()
    # volume
    assert not AmiPath("a:", mgr=mgr).is_volume_path()
    assert AmiPath("root:", mgr=mgr).is_volume_path()
    assert not AmiPath("foo:", mgr=mgr).is_volume_path()
    with pytest.raises(AmiPathError):
        AmiPath("rel").is_volume_path()
    # assign
    assert AmiPath("a:", mgr=mgr).is_assign_path()
    assert not AmiPath("root:", mgr=mgr).is_assign_path()
    assert not AmiPath("foo:", mgr=mgr).is_assign_path()
    with pytest.raises(AmiPathError):
        AmiPath("rel").is_assign_path()
    # valid
    assert AmiPath("a:", mgr=mgr).is_valid()
    assert AmiPath("root:", mgr=mgr).is_valid()
    assert not AmiPath("foo:", mgr=mgr).is_valid()
    assert AmiPath("rel").is_valid()


def test_amipath_multi_assigns():
    mgr = TestMgr()
    assert AmiPath("a:", mgr=mgr).is_multi_assign_path()
    assert not AmiPath("b:", mgr=mgr).is_multi_assign_path()
    with pytest.raises(AmiPathError):
        AmiPath("rel", mgr=mgr).is_multi_assign_path()
    with pytest.raises(AmiPathError):
        AmiPath("root:", mgr=mgr).is_multi_assign_path()


def test_amipath_strip_last_name():
    assert AmiPath("foo/bar").strip_last_name() == AmiPath("foo")
    assert AmiPath("foo:bar/baz").strip_last_name() == AmiPath("foo:bar")
    assert AmiPath("foo:bar").strip_last_name() == AmiPath("foo:")
    assert AmiPath("foo:").strip_last_name() is None
    assert AmiPath("/bar").strip_last_name() == AmiPath("/")
    assert AmiPath("/bar/").strip_last_name() == AmiPath("/")
    assert AmiPath("/").strip_last_name() is None
    assert AmiPath(":").strip_last_name() is None
    assert AmiPath(":bar").strip_last_name() == AmiPath(":")
    assert AmiPath("bar").strip_last_name() == AmiPath()


def test_amipath_get_names():
    assert AmiPath("foo/bar").get_names() == ['foo', 'bar']
    assert AmiPath("foo:bar/baz").get_names() == ['bar', 'baz']
    assert AmiPath("foo:bar").get_names() == ['bar']
    assert AmiPath("foo:").get_names() == []
    assert AmiPath("/bar").get_names() == ['bar']
    assert AmiPath("/bar/").get_names() == ['bar']
    assert AmiPath("/").get_names() == []
    assert AmiPath(":").get_names() == []
    assert AmiPath(":bar").get_names() == ['bar']
    assert AmiPath("bar").get_names() == ['bar']
    # with special name
    assert AmiPath("foo/bar").get_names(True) == ['foo', 'bar']
    assert AmiPath("foo:bar/baz").get_names(True) == ['bar', 'baz']
    assert AmiPath("foo:bar").get_names(True) == ['bar']
    assert AmiPath("foo:").get_names(True) == []
    assert AmiPath("/bar").get_names(True) == ['/', 'bar']
    assert AmiPath("/bar/").get_names(True) == ['/', 'bar']
    assert AmiPath("/").get_names(True) == ['/']
    assert AmiPath(":").get_names(True) == [':']
    assert AmiPath(":bar").get_names(True) == [':', 'bar']
    assert AmiPath("bar").get_names(True) == ['bar']


def test_amipath_join_abs():
    # abs join abs
    assert AmiPath("foo:bar").join(AmiPath("baz:boo")) == AmiPath("baz:boo")
    # abs join parent local
    assert AmiPath("foo:bar").join(AmiPath("/baz")) == AmiPath("foo:baz")
    assert AmiPath("foo:bar/boo").join(AmiPath("/baz")
                                       ) == AmiPath("foo:bar/baz")
    assert AmiPath("foo:bar/boo").join(AmiPath("/")) == AmiPath("foo:bar")
    with pytest.raises(AmiPathError):
        print(AmiPath("foo:").join(AmiPath("/baz")))
    # abs join prefix local
    assert AmiPath("foo:bar").join(AmiPath(":baz")) == AmiPath("foo:baz")
    assert AmiPath("foo:bar/boo").join(AmiPath(":baz")) == AmiPath("foo:baz")
    assert AmiPath("foo:bar").join(AmiPath(":")) == AmiPath("foo:")
    # abs join local
    assert AmiPath("foo:").join(AmiPath()) == AmiPath("foo:")
    assert AmiPath("foo:").join(AmiPath("bar")) == AmiPath("foo:bar")
    assert AmiPath("foo:baz").join(AmiPath("bar")) == AmiPath("foo:baz/bar")


def test_amipath_join_local():
    # local join abs
    assert AmiPath("bar").join(AmiPath("baz:boo")) == AmiPath("baz:boo")
    # local join parent local
    assert AmiPath("bar").join(AmiPath("/baz")) == AmiPath("baz")
    assert AmiPath("bar/boo").join(AmiPath("/baz")) == AmiPath("bar/baz")
    assert AmiPath("bar/boo").join(AmiPath("/")) == AmiPath("bar")
    with pytest.raises(AmiPathError):
        print(AmiPath().join(AmiPath("/baz")))
    # local join prefix local
    assert AmiPath("bar").join(AmiPath(":baz")) == AmiPath(":baz")
    assert AmiPath("bar/boo").join(AmiPath(":baz")) == AmiPath(":baz")
    assert AmiPath("bar").join(AmiPath(":")) == AmiPath(":")
    # local join local
    assert AmiPath().join(AmiPath()) == AmiPath()
    assert AmiPath().join(AmiPath("bar")) == AmiPath("bar")
    assert AmiPath("baz").join(AmiPath("bar")) == AmiPath("baz/bar")
    assert AmiPath("foo/baz").join(AmiPath("bar")) == AmiPath("foo/baz/bar")


def test_amipath_join_parent_local():
    # parent local join abs
    assert AmiPath("/bar").join(AmiPath("baz:boo")) == AmiPath("baz:boo")
    # parent local join parent local
    with pytest.raises(AmiPathError):
        AmiPath("/bar").join(AmiPath("/baz"))
    # parent local join prefix local
    assert AmiPath("/bar").join(AmiPath(":baz")) == AmiPath(":baz")
    assert AmiPath("/bar/boo").join(AmiPath(":baz")) == AmiPath(":baz")
    assert AmiPath("/bar").join(AmiPath(":")) == AmiPath(":")
    # parent local join local
    assert AmiPath("/").join(AmiPath()) == AmiPath("/")
    assert AmiPath("/").join(AmiPath("bar")) == AmiPath("/bar")
    assert AmiPath("/baz").join(AmiPath("bar")) == AmiPath("/baz/bar")
    assert AmiPath("/foo/baz").join(AmiPath("bar")) == AmiPath("/foo/baz/bar")


def test_amipath_join_prefix_local():
    # prefix local join abs
    assert AmiPath(":bar").join(AmiPath("baz:boo")) == AmiPath("baz:boo")
    # prefix local join parent local
    with pytest.raises(AmiPathError):
        AmiPath(":").join(AmiPath("/baz"))
    assert AmiPath(":bar").join(AmiPath("/baz")) == AmiPath(":baz")
    assert AmiPath(":foo/bar").join(AmiPath("/baz")) == AmiPath(":foo/baz")
    # prefix local join prefix local
    assert AmiPath(":bar").join(AmiPath(":baz")) == AmiPath(":baz")
    assert AmiPath(":bar/boo").join(AmiPath(":baz")) == AmiPath(":baz")
    assert AmiPath(":bar").join(AmiPath(":")) == AmiPath(":")
    # prefix local join local
    assert AmiPath(":").join(AmiPath()) == AmiPath(":")
    assert AmiPath(":").join(AmiPath("bar")) == AmiPath(":bar")
    assert AmiPath(":baz").join(AmiPath("bar")) == AmiPath(":baz/bar")
    assert AmiPath(":foo/baz").join(AmiPath("bar")) == AmiPath(":foo/baz/bar")
