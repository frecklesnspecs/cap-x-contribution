from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from .models import Bug


def index(request):
    bug_list = Bug.objects.order_by("-report_date")
    context = {"bug_list": bug_list}
    return render(request, "bug/index.html", context)


def info(request, bug_id):
    bug = get_object_or_404(Bug, pk=bug_id)
    return render(request, "bug/info.html", {"bug": bug})


def new(request):
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

   