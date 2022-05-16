from rest_framework.viewsets import ViewSetMixin


class SerializerViewSetMixin(ViewSetMixin):
    def get_serializer_class(self):
        if hasattr(self, 'serializers'):
            try:
                return self.serializers[self.action]
            except (KeyError, AttributeError):
                return self.serializers['default']