
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from officer.models import (
    CitizenRequest,
    RequestReply,
    RequestStatusHistory,
)
from .forms import CitizenRequestForm


@login_required
def my_requests(request):
    citizen_requests = (
        CitizenRequest.objects
        .filter(citizen=request.user)
        .order_by("-created_at")
    )

    return render(
        request,
        "requests/my_requests.html",
        {"requests": citizen_requests},
    )


@login_required
def create_request(request):
    if request.method == "POST":
        form = CitizenRequestForm(request.POST)

        if form.is_valid():
            citizen_request = form.save(commit=False)
            citizen_request.citizen = request.user
            citizen_request.status = CitizenRequest.Status.PENDING
            citizen_request.save()

            return redirect(
                "requests:request_detail",
                request_id=citizen_request.pk,
            )
    else:
        form = CitizenRequestForm()

    return render(
        request,
        "requests/create_request.html",
        {"form": form},
    )


@login_required
def request_detail(request, request_id):
    citizen_request = get_object_or_404(
        CitizenRequest.objects.select_related(
            "citizen",
            "assigned_officer",
        ).prefetch_related("replies", "status_history"),
        pk=request_id,
        citizen=request.user,
    )

    return render(
        request,
        "requests/request_detail.html",
        {
            "request": citizen_request,
            "replies": citizen_request.replies.all(),
            "status_history": citizen_request.status_history.all(),
        },
    )
