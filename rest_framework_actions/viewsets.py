from rest_framework import mixins as rest_mixins
from rest_framework.viewsets import GenericViewSet

from .mixins import ListActionMixin, CreateActionMixin, RetrieveActionMixin, UpdateActionMixin


class ActionsModelViewSet(
    CreateActionMixin,
    RetrieveActionMixin,
    UpdateActionMixin,
    rest_mixins.DestroyModelMixin,
    ListActionMixin,
    GenericViewSet
):
    pass
