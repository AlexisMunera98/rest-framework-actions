[![PyPI version](https://badge.fury.io/py/rest-framework-actions.svg)](https://badge.fury.io/py/rest-framework-actions)
[![Python version](https://img.shields.io/pypi/pyversions/rest-framework-actions)](https://img.shields.io/pypi/pyversions/rest-framework-actions)
[![Django version](https://img.shields.io/pypi/djversions/rest-framework-actions)](https://img.shields.io/pypi/djversions/rest-framework-actions)
[![License](https://img.shields.io/pypi/l/rest-framework-actions)](https://img.shields.io/pypi/l/rest-framework-actions)

# Rest Framework Actions

[Django Rest Framework](https://www.django-rest-framework.org/) provides some cool generic classes like ModelViewSet to
create services using a defined serializer and model but sometimes you want to change the serializer class or queryset
used in each action or method.
**rest-framework-actions** is a DRF app extension to give you more control over the actions of ModelViewSet. You can
specify a serializer class to each action like list, retrieve, update.

* Source
  Code: [https://github.com/AlexisMunera98/rest-framework-actions](https://github.com/AlexisMunera98/rest-framework-actions)
* PyPI: [https://pypi.org/project/rest-framework-actions/](https://pypi.org/project/rest-framework-actions/)
* License: MIT

## Installation

1. Install using  `pip`
   ```shell
   pip install rest-framework-actions
   ```
2. Add "rest_framework_actions" to your INSTALLED_APPS setting like this:
    ```python
    INSTALLED_APPS = [
        ...
        'rest_framework_actions,
    ]
   ```

   **Note:** Please be sure add after "rest_framework"


3. Then simply import the mixin or viewset into any views.py in which you'd want to use it:
   ```python
   from rest_framework_actions.mixins import ListActionMixin, RetrieveActionMixin, CreateActionMixin, UpdateActionMixin
   from rest_framework_actions.viewsets import ActionsModelViewSet
   ```

   **Note:** This package is built on top of Django Rest Framework's generic views and serializers, so it presupposes
   that Django Rest Framework is installed and added to your project as well.

# How to use

## Given the following scenario:

   ```python
   # models.py
from django.db import models

class Choice(models.Model):
    title = models.CharField(max_length=160)
    description = models.TextField()
    like_votes = models.IntegerField()
    dislike_votes = models.IntegerField()
    expire_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


# serializers.py
from rest_framework import serializers

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


# views.py
from rest_framework import viewsets

class ChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()
   ```

## You have a simple CRUD service over `Choice` model with this behavior:

- Choice list: localhost:8000/choices/
   ```json
   [
      {
       "id": 1,
       "title": "Develop with Django",
       "description": "Do you like develop apps with django?",
       "like_votes": 6353,
       "dislike_votes": 234,
       "expire_at": "2021-05-28T04:29:33Z",
       "created_at": "2021-01-11T04:29:38.387891Z"
      },
      ...
  ]
   ```

- Choice detail: localhost:8000/choices/1/
  ```json
  {
    "id": 1,
    "title": "Develop with Django",
    "description": "Do you like develop apps with django?",
    "like_votes": 6353,
    "dislike_votes": 234,
    "expire_at": "2021-05-28T04:29:33Z",
    "created_at": "2021-01-11T04:29:38.387891Z"
  }
  ```

## But you want to serialize in different ways in each method. How could you get it?

Change your `ModelViewSet` views to `ActionsModelViewSet` in this way:

```python
# serializers.py
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class ListChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('title', 'like_votes', 'dislike_votes')


# views.py
from rest_framework_actions.viewsets import ActionsModelViewSet

class ChoiceViewSet(ActionsModelViewSet):
    list_serializer_class = ListChoiceSerializer
    serializer_class = ChoiceSerializer  # All unspecified actions will use this as default

    list_queryset = Choice.objects.exclude(expire_at__lte=timezone.now())  # Even you can use different queryset to list
    queryset = Choice.objects.all()

```

and ***voilà***:

- `Choice list:` [localhost:8000/choices/](localhost:8000/choices/)
   ```json
   [
    {
        "title": "Develop with Django",
        "like_votes": 6353,
        "dislike_votes": 234
    }
    ...
  ]
   ```

- `Choice detail:` [localhost:8000/choices/1/](localhost:8000/choices/1/)
  ```json
  {
    "id": 1,
    "title": "Develop with Django",
    "description": "Do you like develop apps with django?",
    "like_votes": 6353,
    "dislike_votes": 234,
    "expire_at": "2021-05-28T04:29:33Z",
    "created_at": "2021-01-11T04:29:38.387891Z"
  }
  ```


