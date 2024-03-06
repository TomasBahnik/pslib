from singleton import SingletonNew, SingletonConstr, Singleton3


def test_singleton():
    s1 = SingletonNew(1)
    s2 = SingletonNew(2)
    assert s1 is s2
    assert id(s1) == id(s2)
    assert s1 == s2
    assert s1.x == s2.x
    print(s1.x, s2.x)

    s3 = SingletonConstr.get_instance()
    s4 = SingletonConstr.get_instance()
    assert s3 is s4
    assert id(s3) == id(s4)
    assert s3 == s4

    s4 = Singleton3(111)
    assert s4.y == 4444
    assert s4.x == 111
    assert s4.z == 111
