from boto.sqs.connection import SQSConnection
from boto.sqs import SQSRegionInfo

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response
from django.template import RequestContext

from datetime import datetime, timedelta

def superuser_only(view_func):
    """
    Limit a view to superuser only.
    """
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _inner

def parse_attributes(items):
    for q, attr in items.iteritems():
        q.name = q._name
        q.created = datetime.fromtimestamp(int(attr['CreatedTimestamp']))
        q.last_modified = datetime.fromtimestamp(int(attr['LastModifiedTimestamp']))
        q.visibility_timeout = timedelta(seconds=int(attr['VisibilityTimeout']))
        q.message_retention = timedelta(seconds=int(attr['MessageRetentionPeriod']))
        q.messages_not_visible = attr['ApproximateNumberOfMessagesNotVisible']

@superuser_only
def dashboard(request):
    """
    Graph SQS send statistics over time.
    """
    cache_key = 'vhash:django_sqs_stats'
    cached_view = cache.get(cache_key)
    
    if cached_view:
        return cached_view

    region_name = getattr(settings, 'SQS_REGION', 'us-east-1')
    endpoint_name = getattr(settings, 'SQS_ENDPOINT', 'queue.amazonaws.com')
    
    sqs_conn = SQSConnection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY,)

    if region_name and endpoint_name:
        region = SQSRegionInfo(sqs_conn, region_name, endpoint_name)
        sqs_conn = SQSConnection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, region=region)

    queues = sqs_conn.get_all_queues()

    qas = {}
    
    for queue in queues:
        qas[queue] = sqs_conn.get_queue_attributes(queue)
    
    parse_attributes(qas)

    extra_context = {
        'title': 'SQS Statistics',
        'queues': queues,
        'access_key': sqs_conn.gs_access_key_id,
    }
    
    response = render_to_response(
        'django_sqs/queue_stats.html',
        extra_context,
        context_instance=RequestContext(request))

    cache.set(cache_key, response, 60 * 1) # Cache for 1 minute
    
    return response
