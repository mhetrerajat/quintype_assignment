"""
    This module serializes the SQLAlchemy resultset. Resultset is the collection
    of rows which are return for particular query.
"""
from sqlalchemy.inspection import inspect


class Serializer(object):
    """
        Serializer does serialization of SQLALchemy resultset.

        Note:
            Do not include the `self` parameter in the ``Args`` section.
    """

    def serialize(self):
        """
            It serializes single object.

            Example:
                Suppose query is written to find car with particular id.
                The query will written instance of Car class mapped with data
                from car table. That object is serialized with this method
                into json.

        """
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(data_list):
        """
            It serializes collection of objects.
            Example:
            Suppose query is written to find car who has pink color.
            The result set will be collection of instances of Car class
            mapped with data from car table who has pink color.
            That collection is serilized with this static method.

            Args:
            data_list (list) : List/Collection of objects.
        """
        return [item.serialize() for item in data_list]
