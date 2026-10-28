from django.shortcuts import render
from .forms import SecurityIncidentReportForm,SecurityReportRequestForm
from .models import( SecurityIncidentReport,EmergencySafetyInformation,
                    MissingPersonCommunityNotice, SecurityFacilityContact, SecurityReportRequest,
                    CommunitySafetyProgramme,SecurityAdvisory)
from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    redirect,
    
)
from decimal import Decimal, InvalidOperation
from django.db.models import Q, Count
def home(request):

    services = [
{
    "name": "Security",
    "icon": "bi-shield-check",
    "description": (
        "Access security, emergency and community safety services."
    ),
    "color": "service-purple",
    "url": "security:home",
},
        {
        "name": "Security Services & Information",
        "icon": "bi-shield-check",
        "description": "Access public security information, crime prevention guidance and community safety information.",
        "color": "primary",
       "url": "security:incident_report",
    },
    {
        "name": "Security Incident Reporting",
        "icon": "bi-exclamation-triangle",
        "description": "Report theft, suspicious activity, vandalism, public disorder and other security incidents.",
        "color": "danger",
     "url": "security:emergency_information",
    },
    {
        "name": "Emergency & Safety Information",
        "icon": "bi-life-preserver",
        "description": "Access emergency contacts, safety guidance and emergency preparedness information.",
        "color": "warning",
        "url": "security:emergency_information",
    },
    {
        "name": "Community Safety Programmes",
        "icon": "bi-people",
        "description": "View community policing, crime prevention and other public safety programmes.",
        "color": "success",
       "url": "security:programmes",
    },
    {
        "name": "Security Advisories & Alerts",
        "icon": "bi-bell",
        "description": "View published security warnings, public safety alerts and community advisories.",
        "color": "danger",
       "url": "security:advisories",
    },
    {
        "name": "Missing Persons & Community Notices",
        "icon": "bi-person-exclamation",
        "description": "View approved missing-person notices and other important community notices.",
        "color": "info",
        "url": "security:notices",
    },
    {
        "name": "Security Facilities & Contacts",
        "icon": "bi-building",
        "description": "Find security facilities, emergency facilities and relevant public safety contacts.",
        "color": "secondary",
       "url": "security:facilities",
    },
    {
        "name": "Security Reports / Requests",
        "icon": "bi-clipboard-check",
        "description": "Submit general security-related reports and service requests.",
        "color": "dark",
        "url": "security:requests",
    },
    {
        "name": "Security & Community Safety Statistics",
        "icon": "bi-bar-chart-line",
        "description": "View citizen-facing statistics about security reports, advisories and community safety.",
        "color": "success",
       "url": "security:statistics",
    },

    ]

    context = {
        "services": services,
    }

    return render(
        request,
        "security/home.html",
        context
    )
    
def incident_report(request):
    if request.method == "POST":
        form = SecurityIncidentReportForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            latitude_value = request.POST.get("latitude", "").strip()
            longitude_value = request.POST.get("longitude", "").strip()

            latitude = None
            longitude = None

            # Both coordinates must be supplied together.
            if bool(latitude_value) != bool(longitude_value):
                form.add_error(
                    None,
                    "Please select a valid incident location on the map, "
                    "or clear the map pin and submit without GPS coordinates."
                )
            elif latitude_value and longitude_value:
                try:
                    latitude = Decimal(latitude_value)
                    longitude = Decimal(longitude_value)

                    if (
                        not latitude.is_finite()
                        or not longitude.is_finite()
                        or latitude < Decimal("-90")
                        or latitude > Decimal("90")
                        or longitude < Decimal("-180")
                        or longitude > Decimal("180")
                    ):
                        raise InvalidOperation

                    # Match the model's six decimal places.
                    latitude = latitude.quantize(Decimal("0.000001"))
                    longitude = longitude.quantize(Decimal("0.000001"))

                except (InvalidOperation, ValueError):
                    form.add_error(
                        None,
                        "The selected GPS location is invalid. "
                        "Please select the location again."
                    )

            if form.is_valid():
                report = form.save(commit=False)
                report.latitude = latitude
                report.longitude = longitude
                report.save()

                messages.success(
                    request,
                    "Your security incident has been reported successfully."
                )

                return redirect(
                    "security:incident_report_success",
                    report_id=report.pk
                )

    else:
        form = SecurityIncidentReportForm()

    return render(
        request,
        "security/incident_report.html",
        {"form": form}
    )


def incident_report_success(request, report_id):

    report = get_object_or_404(
        SecurityIncidentReport,
        pk=report_id
    )

    return render(
        request,
        "security/incident_report_success.html",
        {
            "report": report
        }
    )
    
def emergency_information(request):

    information = EmergencySafetyInformation.objects.filter(
        is_published=True
    )

    category = request.GET.get("category")
    district = request.GET.get("district")
    search = request.GET.get("q")

    if category:
        information = information.filter(
            category=category
        )

    if district:
        information = information.filter(
            district__icontains=district
        )

    if search:
        information = information.filter(
            Q(title__icontains=search)
            | Q(summary__icontains=search)
            | Q(information__icontains=search)
            | Q(contact_organization__icontains=search)
        )

    context = {
        "information": information,
        "categories": EmergencySafetyInformation.CATEGORY_CHOICES,
        "selected_category": category,
        "selected_district": district,
        "search_query": search,
    }

    return render(
        request,
        "security/emergency_information.html",
        context
    )
    
def programmes(request):

    programmes = CommunitySafetyProgramme.objects.filter(
        is_published=True
    )

    programme_type = request.GET.get("programme_type")
    district = request.GET.get("district")
    status = request.GET.get("status")
    search = request.GET.get("q")

    if programme_type:
        programmes = programmes.filter(
            programme_type=programme_type
        )

    if district:
        programmes = programmes.filter(
            district__icontains=district
        )

    if status:
        programmes = programmes.filter(
            status=status
        )

    if search:
        programmes = programmes.filter(
            Q(title__icontains=search)
            | Q(summary__icontains=search)
            | Q(description__icontains=search)
            | Q(district__icontains=search)
        )

    context = {
        "programmes": programmes,
        "programme_types": (
            CommunitySafetyProgramme.PROGRAMME_TYPE_CHOICES
        ),
        "statuses": (
            CommunitySafetyProgramme.STATUS_CHOICES
        ),
        "selected_type": programme_type,
        "selected_district": district,
        "selected_status": status,
        "search_query": search,
    }

    return render(
        request,
        "security/programmes.html",
        context
    )
    
def advisories(request):

    advisories = SecurityAdvisory.objects.filter(
        is_published=True
    )

    advisory_type = request.GET.get("advisory_type")
    district = request.GET.get("district")
    priority = request.GET.get("priority")
    search = request.GET.get("q")

    if advisory_type:
        advisories = advisories.filter(
            advisory_type=advisory_type
        )

    if district:
        advisories = advisories.filter(
            district__icontains=district
        )

    if priority:
        advisories = advisories.filter(
            priority=priority
        )

    if search:
        advisories = advisories.filter(
            Q(title__icontains=search)
            | Q(summary__icontains=search)
            | Q(message__icontains=search)
            | Q(district__icontains=search)
            | Q(issuing_organization__icontains=search)
        )

    context = {
        "advisories": advisories,

        "advisory_types": (
            SecurityAdvisory.ADVISORY_TYPE_CHOICES
        ),

        "priorities": (
            SecurityAdvisory.PRIORITY_CHOICES
        ),

        "selected_type": advisory_type,
        "selected_district": district,
        "selected_priority": priority,
        "search_query": search,
    }

    return render(
        request,
        "security/advisories.html",
        context
    )
    
def notices(request):

    notices = MissingPersonCommunityNotice.objects.filter(
        is_published=True
    )

    notice_type = request.GET.get("notice_type")
    district = request.GET.get("district")
    status = request.GET.get("status")
    search = request.GET.get("q")

    if notice_type:
        notices = notices.filter(
            notice_type=notice_type
        )

    if district:
        notices = notices.filter(
            district__icontains=district
        )

    if status:
        notices = notices.filter(
            status=status
        )

    if search:
        notices = notices.filter(
            Q(title__icontains=search)
            | Q(summary__icontains=search)
            | Q(description__icontains=search)
            | Q(person_name__icontains=search)
            | Q(district__icontains=search)
            | Q(location__icontains=search)
        )

    context = {
        "notices": notices,

        "notice_types": (
            MissingPersonCommunityNotice.NOTICE_TYPE_CHOICES
        ),

        "statuses": (
            MissingPersonCommunityNotice.STATUS_CHOICES
        ),

        "selected_type": notice_type,
        "selected_district": district,
        "selected_status": status,
        "search_query": search,
    }

    return render(
        request,
        "security/notices.html",
        context
    )
def facilities(request):

    facilities = SecurityFacilityContact.objects.filter(
        is_published=True
    )

    facility_type = request.GET.get("facility_type")
    district = request.GET.get("district")
    emergency = request.GET.get("emergency")
    search = request.GET.get("q")

    if facility_type:
        facilities = facilities.filter(
            facility_type=facility_type
        )

    if district:
        facilities = facilities.filter(
            district__icontains=district
        )

    if emergency == "yes":
        facilities = facilities.filter(
            is_emergency_facility=True
        )

    if search:
        facilities = facilities.filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(district__icontains=search)
            | Q(city__icontains=search)
            | Q(location__icontains=search)
            | Q(address__icontains=search)
            | Q(phone_number__icontains=search)
            | Q(emergency_number__icontains=search)
        )

    context = {
        "facilities": facilities,

        "facility_types": (
            SecurityFacilityContact.FACILITY_TYPE_CHOICES
        ),

        "selected_type": facility_type,
        "selected_district": district,
        "emergency_filter": emergency,
        "search_query": search,
    }

    return render(
        request,
        "security/facilities.html",
        context
    )
    
def security_request(request):

    if request.method == "POST":

        form = SecurityReportRequestForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            report = form.save()

            messages.success(
                request,
                "Your security report or request has been "
                "submitted successfully."
            )

            return redirect(
                "security:request_success",
                request_id=report.pk
            )

    else:

        form = SecurityReportRequestForm()

    return render(
        request,
        "security/request.html",
        {
            "form": form
        }
    )


def request_success(request, request_id):

    report = get_object_or_404(
        SecurityReportRequest,
        pk=request_id
    )

    return render(
        request,
        "security/request_success.html",
        {
            "report": report
        }
    )
def statistics(request):

    # ---------------------------------------------------------
    # TOTAL RECORDS
    # ---------------------------------------------------------

    incident_count = SecurityIncidentReport.objects.count()

    emergency_information_count = (
        EmergencySafetyInformation.objects
        .filter(is_published=True)
        .count()
    )

    programme_count = (
        CommunitySafetyProgramme.objects
        .filter(is_published=True)
        .count()
    )

    advisory_count = (
        SecurityAdvisory.objects
        .filter(is_published=True)
        .count()
    )

    notice_count = (
        MissingPersonCommunityNotice.objects
        .filter(is_published=True)
        .count()
    )

    facility_count = (
        SecurityFacilityContact.objects
        .filter(is_published=True)
        .count()
    )

    security_request_count = (
        SecurityReportRequest.objects.count()
    )

    # ---------------------------------------------------------
    # INCIDENT STATUS COUNTS
    # ---------------------------------------------------------

    incident_status_counts = (
        SecurityIncidentReport.objects
        .values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    # ---------------------------------------------------------
    # SECURITY REQUEST STATUS COUNTS
    # ---------------------------------------------------------

    request_status_counts = (
        SecurityReportRequest.objects
        .values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    # ---------------------------------------------------------
    # PROGRAMME STATUS COUNTS
    # ---------------------------------------------------------

    programme_status_counts = (
        CommunitySafetyProgramme.objects
        .filter(is_published=True)
        .values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    # ---------------------------------------------------------
    # ADVISORY PRIORITY COUNTS
    # ---------------------------------------------------------

    advisory_priority_counts = (
        SecurityAdvisory.objects
        .filter(is_published=True)
        .values("priority")
        .annotate(total=Count("id"))
        .order_by("priority")
    )

    # ---------------------------------------------------------
    # NOTICE STATUS COUNTS
    # ---------------------------------------------------------

    notice_status_counts = (
        MissingPersonCommunityNotice.objects
        .filter(is_published=True)
        .values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    # ---------------------------------------------------------
    # FACILITY TYPE COUNTS
    # ---------------------------------------------------------

    facility_type_counts = (
        SecurityFacilityContact.objects
        .filter(is_published=True)
        .values("facility_type")
        .annotate(total=Count("id"))
        .order_by("facility_type")
    )

    context = {
        "incident_count": incident_count,
        "emergency_information_count": emergency_information_count,
        "programme_count": programme_count,
        "advisory_count": advisory_count,
        "notice_count": notice_count,
        "facility_count": facility_count,
        "security_request_count": security_request_count,

        "incident_status_counts": incident_status_counts,
        "request_status_counts": request_status_counts,
        "programme_status_counts": programme_status_counts,
        "advisory_priority_counts": advisory_priority_counts,
        "notice_status_counts": notice_status_counts,
        "facility_type_counts": facility_type_counts,
    }

    return render(
        request,
        "security/statistics.html",
        context
    )