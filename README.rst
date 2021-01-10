=======================
Rest framework actions
=======================

Django Rest Framework provides some cool generic classes like ModelViewSet to create services using a defined serializer
and model but sometimes you want to have more control over the serializer class used in each action.
rest-framework-actions is a DRF app extension to give you more control over the actions of ModelViewSet. You can specified
a serializer class to each action like list, retrieve, update.

* Source Code: https://github.com/AlexisMunera98/rest-framework-actions
* PyPI: https://pypi.org/project/rest-framework-actions/
* License: MIT


Quick start
-----------

1. Add "rest_framework_actions" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework_actions,
    ]

   **Note:** Please be sure to added after "rest_framework"

2. Include the polls URLconf in your project urls.py like this::

    path('polls/', include('polls.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/polls/ to participate in the poll.