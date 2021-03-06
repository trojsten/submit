from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from submit.models import BaseTask


@python_2_unicode_compatible
class Task(BaseTask):
    """
    General task data not related to testing are defined here.
    """
    slug = models.SlugField(primary_key=True,
                            help_text='Must be unique among all tasks, serves as part of URL.<br />'
                                      'By default, task.slug is also used as a name of inputs folder at judge.<br />'
                                      'Must only contain characters "a-zA-Z0-9_-".')
    visible = models.BooleanField()
    deadline = models.DateTimeField()
    max_points = models.IntegerField()

    def get_absolute_url(self):
        return reverse('task_statement', kwargs=dict(task_slug=self.slug))

    def __str__(self):
        return u'{} ({})'.format(self.name, self.slug)
