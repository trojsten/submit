# TODO: Tests independent on example
import json
import datetime

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from submit.models import SubmitReceiver

from example.tasks.models import Task


def user_cant_post_submit(receiver, user):
    return False


class ExternalSubmitTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='jozko', first_name='Jozko', last_name='Mrkvicka', password='pass'
        )
        self.task = Task.objects.create(name='Task task', slug='task', visible=True, max_points=10,
                                        deadline=timezone.now() + datetime.timedelta(weeks=2), )
        self.receiver_accepting = SubmitReceiver.objects.create(task=self.task, allow_external_submits=True)

    def _post_external_submit(self, data):
        url = reverse('external_submit')
        return self.client.post(
            url, json.dumps(data),
            content_type='application/json'
        )

    def test_submit_ok(self):
        self.assertEqual(self.receiver_accepting.submit_set.count(), 0)

        response = self._post_external_submit({
            'token': self.receiver_accepting.token,
            'user': self.user.pk,
            'score': 10,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.receiver_accepting.submit_set.count(), 1)
        self.assertEqual(self.receiver_accepting.submit_set.first().review_set.count(), 1)

    def test_submit_invalid_token(self):
        response = self._post_external_submit({
            'token': 'I am hacker',
            'user': self.user.pk,
            'score': 10,
        })
        self.assertEqual(response.status_code, 400)

    def test_submit_invalid_user(self):
        response = self._post_external_submit({
            'token': self.receiver_accepting.token,
            'user': 0,
            'score': 10,
        })
        self.assertEqual(response.status_code, 400)

    def test_submit_missing_parameters(self):
        response = self._post_external_submit({})
        self.assertEqual(response.status_code, 400)

        response = self._post_external_submit({
            'token': self.receiver_accepting.token,
        })
        self.assertEqual(response.status_code, 400)

        response = self._post_external_submit({
            'token': self.receiver_accepting.token,
            'user': self.user.pk,
        })
        self.assertEqual(response.status_code, 400)

    def test_external_submit_invalid_method(self):
        url = reverse('external_submit')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_submit_not_allowed(self):
        self.receiver_non_accepting = SubmitReceiver.objects.create(task=self.task, allow_external_submits=False)
        response = self._post_external_submit({
            'token': self.receiver_non_accepting.token,
            'user': self.user.pk,
            'score': 10,
        })
        self.assertEqual(response.status_code, 403)

    def test_user_not_allowed_to_submit(self):
        self.task.visible = False
        self.task.save()

        response = self._post_external_submit({
            'token': self.receiver_accepting.token,
            'user': self.user.pk,
            'score': 10,
        })
        self.assertEqual(response.status_code, 403)
