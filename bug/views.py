from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Bug


class IndexView(generic.ListView):
    template_name = "bug/index.html"
    context_object_name = "bug_list"

    def get_queryset(self):
        return Bug.objects.filter(report_date__lte=timezone.now()).order_by("-report_date")


class InfoView(generic.DetailView):
    model = Bug
    template_name = "bug/info.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Bug.objects.filter(report_date__lte=timezone.now())


def new(request):
    """
    The fields 'report_date' and 'status' were intentionally left out of the new bug
    registration view to minimize user error in the data. This follows the assumptions
    that admin will be setting the bug status and public users will report the bug
    in a timely manner.
    """
    return render(request, "bug/new.html", {"bug_types": Bug.BUG_TYPE})


def save(request):
   if request.POST["description"] == "":
      return render(
          request,
          "bug/new.html", {
              "error_message": "You did not describe the bug.",
              "bug_types": Bug.BUG_TYPE,
          },
      )
   else:
    b = Bug(description=request.POST["description"],
            bug_type=request.POST["BUG_TYPE"],
            report_date=timezone.now(),
            status="TO DO")
    b.save()
    return HttpResponseRedirect(reverse("bug:info", args=(b.id,)))
