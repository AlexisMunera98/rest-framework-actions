from django.db.models import QuerySet
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings


class CreateActionMixin(mixins.CreateModelMixin):
    """
    Create a model instance.
    """
    create_serializer_class = None
    output_create_serializer_class = None

    def get_create_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        assert self.create_serializer_class is not None, (
                "'%s' should either include a `create_serializer_class` attribute,"
                "or `output_create_serializer_class` if you want use different serializer for input and output"
                "or override the `get_create_serializer()` method."
                % self.__class__.__name__
        )
        serializer = self.create_serializer_class
        if kwargs.pop('output_serializer', False):
            serializer = self.output_create_serializer_class if self.output_create_serializer_class is not None else self.create_serializer_class
        kwargs['context'] = self.get_serializer_context()
        return serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_create_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer = self.get_create_serializer(instance, output_serializer=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListActionMixin(mixins.ListModelMixin):
    list_queryset = None
    list_serializer_class = None

    def get_list_serializer(self, *args, **kwargs):
        assert self.list_serializer_class is not None, (
                "'%s' should either include a `list_serializer_class` attribute"
                % self.__class__.__name__
        )
        kwargs['context'] = self.get_serializer_context()
        return self.list_serializer_class(*args, **kwargs)

    def get_list_queryset(self):
        assert self.list_queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_list_queryset()` method."
                % self.__class__.__name__
        )
        queryset = self.list_queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_list_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_list_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_list_serializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveActionMixin(mixins.RetrieveModelMixin):
    retrieve_serializer_class = None

    def get_retrieve_serializer(self, *args, **kwargs):
        assert self.retrieve_serializer_class is not None, (
                "'%s' should either include a `retrieve_serializer_class` attribute, "
                "or override the `get_retrieve_serializer()` method."
                % self.__class__.__name__
        )
        kwargs['context'] = self.get_serializer_context()
        return self.retrieve_serializer_class(*args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_retrieve_serializer(instance)
        return Response(serializer.data)


class UpdateActionMixin(mixins.UpdateModelMixin):
    """
    Update a model instance.
    """

    update_serializer_class = None
    output_update_serializer_class = None

    def get_update_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        assert self.update_serializer_class is not None, (
                "'%s' should either include a `update_serializer_class` attribute,"
                "or `output_update_serializer_class` if you want use different serializer for input and output"
                "or override the `get_update_serializer()` method."
                % self.__class__.__name__
        )
        serializer = self.update_serializer_class
        if kwargs.pop('output_serializer', False):
            serializer = self.output_update_serializer_class if self.output_update_serializer_class is not None else self.update_serializer_class
        kwargs['context'] = self.get_serializer_context()
        return serializer(*args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_update_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        serializer = self.get_update_serializer(instance, output_serializer=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
