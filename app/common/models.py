class ModelBase(object):
    """
    An object which can be stored in the database.
    """

    _data_fields = []
    _auto_generated_attrs = []

    def _validate(self, errors):
        """Subclasses override this to offer additional validation.

        For each validation error a key with the field name and an error
        message is added to the dict.

        """
        pass

    def data(self, **options):
        """Called to serialize object to a dictionary."""
        data_fields = self._data_fields + self._auto_generated_attrs
        return {field: self[field] for field in data_fields}

    def is_valid(self):
        """Called when persisting data to ensure the format is correct."""
        self.errors = {}
        self._validate(self.errors)
#        self._validate_columns_type()
#        self._before_validate()
#        self._validate()
        return self.errors == {}

    def __setitem__(self, key, value):
        """Overloaded to cause this object to look like a data entity."""
        setattr(self, key, value)

    def __getitem__(self, key):
        """Overloaded to cause this object to look like a data entity."""
        return getattr(self, key)

    def __eq__(self, other):
        """Overloaded to cause this object to look like a data entity."""
        if not hasattr(other, 'id'):
            return False
        return isinstance(other, type(self)) and other.id == self.id

    def __ne__(self, other):
        """Overloaded to cause this object to look like a data entity."""
        return not self == other

    def __hash__(self):
        """Overloaded to cause this object to look like a data entity."""
        return self.id.__hash__()
