

from django.core import serializers
from django.core.serializers.base import Serializer


class VersionSerializer(Serializer):

    '''Class which has responsibility for loading values from fields

    .. code-block:: python

        class MyModel(Model):

            ignore_fields = ['created']
            version_serializer = VersionSerializer

    '''

    def get_ignored_fields(self, obj, field):
        '''just example returns merged user ignored fields and defaults'''
        return getattr(obj, 'ignore_fields', [])

    def handle_field(self, obj, field):
        '''handle custom directions'''

        if field.name in self.get_ignored_fields(obj, field):
            self._current.pop(field.name, None)
            return

        super(VersionSerializer, self).handle_field(obj, field)

    @classmethod
    def create_serializer(cls, format):
        '''create instance of serializer from two classes'''

        try:
            FormatSerializerCls = serializers.get_serializer(format)
        except serializers.SerializerDoesNotExist:
            raise Exception("Unknown serialization format: %s" % format)

        SerializerCls = type('GitVersionSerializer', (
            cls, FormatSerializerCls), {})

        return SerializerCls()
