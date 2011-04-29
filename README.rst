------
Django SQS
------

Django SQS provides you with a generic interface to view your Amazon SQS queues.

Setup 
~~~~~~~~
  Boto library for accessing Amazon Web Services is required.

  1. Add `django_sqs' to your Python path
  2. Add `django_sqs' to INSTALLED_APPS setting
  3. Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
  4. Optionally set SQS_REGION and SQS_ENDPOINT to use queues
     from different regions
  5. Add something like `(r'^admin/sqs', include('django_sqs.urls')),'
     into your urls.py