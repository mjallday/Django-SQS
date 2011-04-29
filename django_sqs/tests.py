from unittest import TestCase

from django_sqs.views import parse_attributes

ATTRIBUTES_DICT = [
                   { u'ApproximateNumberOfMessagesNotVisible': u'0', 
                    u'MessageRetentionPeriod': u'345600', 
                    u'LastModifiedTimestamp': u'1303884119', 
                    u'MaximumMessageSize': u'8192', 
                    u'CreatedTimestamp': u'1303884119', 
                    u'ApproximateNumberOfMessages': u'0', 
                    u'VisibilityTimeout': u'30', 
                    u'QueueArn': u'arn:aws:sqs:ap-southeast-1:432461735093:cn-deal-announce', },
                   {u'ApproximateNumberOfMessagesNotVisible': u'0', 
                    u'MessageRetentionPeriod': u'345600', 
                    u'LastModifiedTimestamp': u'1303883653', 
                    u'MaximumMessageSize': u'8192', 
                    u'CreatedTimestamp': u'1303883653', 
                    u'ApproximateNumberOfMessages': u'1', 
                    u'VisibilityTimeout': u'30', 
                    u'QueueArn': u'arn:aws:sqs:ap-southeast-1:432461735093:cn-deal-announcedev', }
                   
]

class TestQueue(object):
    def __init__(self, n):
        self._name = n

class SQSTest(TestCase):
    def setUp(self):
        self.attributes_dict = ATTRIBUTES_DICT
        
        
    def test_parse_attributes(self):
        
        queues = [
                  TestQueue('q1'), TestQueue('q2'),                   
                  ]
        
        i = 0 
        qas = {}
        
        for queue in queues:
            qas[queue] = self.attributes_dict[i]
            
            i += 1
            
        parse_attributes(qas)
        
        for queue in queues:
            self.assertNotEqual(None, queue.created)
            self.assertTrue(queue.name in ['q1', 'q2'])
        