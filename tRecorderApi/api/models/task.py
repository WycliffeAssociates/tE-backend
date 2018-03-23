class Task(object):
    def __init__(self, **kwargs):
        for field in (
                'id',
                'name',
                'current',
                'total',
                'progress',
                'title',
                'message',
                'details',
                'status',
                'started_at',
                'updated_at',
                'finished_at'):
            setattr(self, field, kwargs.get(field, None))
