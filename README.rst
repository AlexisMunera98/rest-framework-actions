=======================
Rest framework actions
=======================

Restframework actions is a DRF app extension to give you more control over the actions of
ModelViewSet.

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