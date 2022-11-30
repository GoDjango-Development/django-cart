class Wrapper(dict):
    def __init__(self, model) -> None:
        self.__dict__ = model.__dict__.copy()
        to_delete = []
        for key in self.__dict__.keys():
            value_type = type(self.__dict__[key])
            if not (value_type is str or value_type is int or value_type is float or 
                value_type is bool
            ):
                to_delete.append(key)
        for key in to_delete:
            del self.__dict__[key]
        super().__init__(self.__dict__)
