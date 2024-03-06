from threading import Lock


class SingletonNew:
    _instance = None
    y = 4444

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with Lock():
                # double-checked locking
                if not cls._instance:
                    # in python 3.x super() add default arguments
                    # cls._instance = super(Singleton, cls).__new__(cls)
                    # cannot call cls() - infinite recursion
                    # object.__new__() takes exactly one argument (the type to instantiate)
                    cls._instance = super().__new__(cls)
        return cls._instance

    # TypeError: SingletonNew.__new__() takes 1 positional argument but 2 were given
    def __init__(self, x):
        self.x = x


class Singleton3(SingletonNew):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with Lock():
                if not cls._instance:
                    cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, z):
        super().__init__(z)
        self.z = z


class SingletonConstr:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            with Lock():
                if not cls._instance:
                    # creates new instance - no args for SingletonConstr
                    cls._instance = cls()
        return cls._instance
