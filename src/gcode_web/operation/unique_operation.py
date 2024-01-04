class UniqueOperation:
    # TODO: Rename to "OperationModel"

    _ID = 0

    def __init__(self, operation):
        self._id = UniqueOperation._ID
        UniqueOperation._ID += 1
        self._operation = operation

    id = property(fget=lambda self: self._id)
    operation = property(fget=lambda self: self._operation)
