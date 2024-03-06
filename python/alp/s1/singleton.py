from threading import Lock


class SingletonNew:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            with Lock():
                if not cls._instance:
                    # cls._instance = super(Singleton, cls).__new__(cls)
                    cls._instance = super().__new__(cls)
        return cls._instance


def test_singleton():
    s1 = SingletonNew()
    s2 = SingletonNew()
    assert s1 is s2
    assert id(s1) == id(s2)
    assert s1 == s2


if __name__ == "__main__":
    test_singleton()
