from threading import Lock


class SingletonNew:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            with Lock():
                if not cls._instance:
                    # in python 3.x super() add default arguments
                    # cls._instance = super(Singleton, cls).__new__(cls)
                    cls._instance = super().__new__(cls)
        return cls._instance


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
