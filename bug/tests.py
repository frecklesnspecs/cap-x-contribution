import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Bug


class BugModelTests(TestCase):
    def test_was_reported_recently_with_future_bug(self):
        """
        was_reported_recently() returns False for bugs whose report_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_bug = Bug(report_date=time)
        self.assertIs(future_bug.was_reported_recently(), False)

    def test_was_reported_recently_with_old_bug(self):
        """
        was_reported_recently() returns False for bugs whose report_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_bug = Bug(report_date=time)
        self.assertIs(old_bug.was_reported_recently(), False)

    def test_was_reported_recently_with_recent_bug(self):
        """
        was_reported_recently() returns True for bugs whose report_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_bug = Bug(report_date=time)
        self.assertIs(recent_bug.was_reported_recently(), True)

    def test_validate_description_field(self):
        """
        description returns False for bugs whose description
        field is empty.
        """
        blank_bug = Bug(description="", bug_type="ERROR", report_date=timezone.now(), status="TO DO")
        self.assertRaises(ValidationError, blank_bug.full_clean)


def create_bug(description, days):
    """
    Create a bug with the given `description` and reported the
    given number of `days` offset to now (negative for bugs reported
    in the past, positive for bugs that have yet to be reported).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Bug.objects.create(description=description, bug_type="ERROR", report_date=time, status="TO DO")


class BugIndexViewTests(TestCase):
    def test_no_bugs(self):
        """
        If no bugs exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("bug:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No bugs are available.")
        self.assertQuerySetEqual(response.context["bug_list"], [])

    def test_past_bug(self):
        """
        Bugs with a report_date in the past are displayed on the
        index page.
        """
        bug = create_bug(description="Past bug.", days=-30)
        response = self.client.get(reverse("bug:index"))
        self.assertQuerySetEqual(
            response.context["bug_list"],
            [bug],
        )

    def test_future_bug(self):
        """
        Bugs with a report_date in the future aren't displayed on
        the index page.
        """
        create_bug(description="Future bug.", days=30)
        response = self.client.get(reverse("bug:index"))
        self.assertContains(response, "No bugs are available.")
        self.assertQuerySetEqual(response.context["bug_list"], [])

    def test_future_bug_and_past_bug(self):
        """
        Even if both past and future bugs exist, only past bugs
        are displayed.
        """
        bug = create_bug(description="Past bug.", days=-30)
        create_bug(description="Future bug.", days=30)
        response = self.client.get(reverse("bug:index"))
        self.assertQuerySetEqual(
            response.context["bug_list"],
            [bug],
        )

    def test_two_past_bugs(self):
        """
        The bug index page may display multiple bugs.
        """
        bug1 = create_bug(description="Past bug 1.", days=-30)
        bug2 = create_bug(description="Past bug 2.", days=-5)
        response = self.client.get(reverse("bug:index"))
        self.assertQuerySetEqual(
            response.context["bug_list"],
            [bug2, bug1],
        )


class BugDetailViewTests(TestCase):
    def test_future_bug(self):
        """
        The detail view of a bug with a report_date in the future
        returns a 404 not found.
        """
        future_bug = create_bug(description="Future Bug.", days=5)
        url = reverse("bug:info", args=(future_bug.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_bug(self):
        """
        The detail view of a bug with a report_date in the past
        displays the bug's text.
        """
        past_bug = create_bug(description="Past Bug.", days=-5)
        url = reverse("bug:info", args=(past_bug.id,))
        response = self.client.get(url)
        self.assertContains(response, past_bug.description)
