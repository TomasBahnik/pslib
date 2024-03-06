from singleton import SingletonNew, SingletonConstr


def test_singleton():
    s1 = SingletonNew()
    s2 = SingletonNew()
    assert s1 is s2
    assert id(s1) == id(s2)
    assert s1 == s2

    s3 = SingletonConstr.get_instance()
    s4 = SingletonConstr.get_instance()
    assert s3 is s4
    assert id(s3) == id(s4)
    assert s3 == s4
