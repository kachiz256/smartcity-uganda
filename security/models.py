from django.db import models
import uuid


class SecurityIncidentReport(models.Model):

    # Incident types
    TYPE_THEFT = "theft"
    TYPE_BURGLARY = "burglary"
    TYPE_ASSAULT = "assault"
    TYPE_SUSPICIOUS_ACTIVITY = "suspicious_activity"
    TYPE_MISSING_PERSON = "missing_person"
    TYPE_VANDALISM = "vandalism"
    TYPE_PUBLIC_DISORDER = "public_disorder"
    TYPE_OTHER = "other"

    INCIDENT_TYPE_CHOICES = [
        (TYPE_THEFT, "Theft"),
        (TYPE_BURGLARY, "Burglary"),
        (TYPE_ASSAULT, "Assault"),
        (TYPE_SUSPICIOUS_ACTIVITY, "Suspicious Activity"),
        (TYPE_MISSING_PERSON, "Missing Person"),
        (TYPE_VANDALISM, "Vandalism"),
        (TYPE_PUBLIC_DISORDER, "Public Disorder"),
        (TYPE_OTHER, "Other"),
    ]

    # Report statuses
    STATUS_REPORTED = "reported"
    STATUS_RECEIVED = "received"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_RESOLVED = "resolved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_REPORTED, "Reported"),
        (STATUS_RECEIVED, "Received"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_RESOLVED, "Resolved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    citizen_name = models.CharField(max_length=200)

    phone_number = models.CharField(max_length=30)

    email = models.EmailField(
        blank=True
    )

    district = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=255
    )
        # Private incident GPS coordinates.
    # Do not display these directly on public citizen pages.
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )
    incident_type = models.CharField(
        max_length=40,
        choices=INCIDENT_TYPE_CHOICES
    )

    description = models.TextField()

    reference_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_REPORTED
    )

    attachment = models.FileField(
        upload_to="security/incidents/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        if not self.reference_number:
            self.reference_number = (
                f"SEC-{uuid.uuid4().hex[:8].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_number} - {self.get_incident_type_display()}"
    
class EmergencySafetyInformation(models.Model):

    CATEGORY_EMERGENCY_CONTACT = "emergency_contact"
    CATEGORY_POLICE = "police"
    CATEGORY_FIRE = "fire"
    CATEGORY_MEDICAL = "medical"
    CATEGORY_DISASTER = "disaster"
    CATEGORY_PREPAREDNESS = "preparedness"
    CATEGORY_GENERAL_SAFETY = "general_safety"
    CATEGORY_OTHER = "other"

    CATEGORY_CHOICES = [
        (CATEGORY_EMERGENCY_CONTACT, "Emergency Contact"),
        (CATEGORY_POLICE, "Police & Security"),
        (CATEGORY_FIRE, "Fire & Rescue"),
        (CATEGORY_MEDICAL, "Medical Emergency"),
        (CATEGORY_DISASTER, "Disaster & Emergency"),
        (CATEGORY_PREPAREDNESS, "Emergency Preparedness"),
        (CATEGORY_GENERAL_SAFETY, "General Safety"),
        (CATEGORY_OTHER, "Other"),
    ]

    title = models.CharField(
        max_length=250
    )

    category = models.CharField(
        max_length=40,
        choices=CATEGORY_CHOICES
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    summary = models.CharField(
        max_length=500,
        blank=True
    )

    information = models.TextField()

    emergency_number = models.CharField(
        max_length=100,
        blank=True
    )

    contact_name = models.CharField(
        max_length=200,
        blank=True
    )

    contact_organization = models.CharField(
        max_length=250,
        blank=True
    )

    address = models.CharField(
        max_length=255,
        blank=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-is_featured",
            "-created_at",
        ]

    def __str__(self):
        return self.title
class CommunitySafetyProgramme(models.Model):

    TYPE_COMMUNITY_POLICING = "community_policing"
    TYPE_CRIME_PREVENTION = "crime_prevention"
    TYPE_NEIGHBOURHOOD_SAFETY = "neighbourhood_safety"
    TYPE_YOUTH_SAFETY = "youth_safety"
    TYPE_PUBLIC_AWARENESS = "public_awareness"
    TYPE_EMERGENCY_PREPAREDNESS = "emergency_preparedness"
    TYPE_OTHER = "other"

    PROGRAMME_TYPE_CHOICES = [
        (TYPE_COMMUNITY_POLICING, "Community Policing"),
        (TYPE_CRIME_PREVENTION, "Crime Prevention"),
        (TYPE_NEIGHBOURHOOD_SAFETY, "Neighbourhood Safety"),
        (TYPE_YOUTH_SAFETY, "Youth Safety"),
        (TYPE_PUBLIC_AWARENESS, "Public Awareness"),
        (TYPE_EMERGENCY_PREPAREDNESS, "Emergency Preparedness"),
        (TYPE_OTHER, "Other"),
    ]

    STATUS_PLANNED = "planned"
    STATUS_ACTIVE = "active"
    STATUS_COMPLETED = "completed"
    STATUS_SUSPENDED = "suspended"

    STATUS_CHOICES = [
        (STATUS_PLANNED, "Planned"),
        (STATUS_ACTIVE, "Active"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_SUSPENDED, "Suspended"),
    ]

    title = models.CharField(
        max_length=250
    )

    programme_type = models.CharField(
        max_length=50,
        choices=PROGRAMME_TYPE_CHOICES
    )

    district = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=255,
        blank=True
    )

    summary = models.CharField(
        max_length=500,
        blank=True
    )

    description = models.TextField()

    objectives = models.TextField(
        blank=True
    )

    participating_organization = models.CharField(
        max_length=250,
        blank=True
    )

    contact_information = models.CharField(
        max_length=255,
        blank=True
    )

    start_date = models.DateField(
        blank=True,
        null=True
    )

    end_date = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_PLANNED
    )

    image = models.ImageField(
        upload_to="security/programmes/",
        blank=True,
        null=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-is_featured",
            "-created_at",
        ]

    def __str__(self):
        return self.title
    
class SecurityAdvisory(models.Model):

    TYPE_SECURITY_WARNING = "security_warning"
    TYPE_PUBLIC_SAFETY = "public_safety"
    TYPE_CRIME_ALERT = "crime_alert"
    TYPE_EMERGENCY_ALERT = "emergency_alert"
    TYPE_TRAFFIC_SAFETY = "traffic_safety"
    TYPE_COMMUNITY_ALERT = "community_alert"
    TYPE_MISSING_PERSON = "missing_person"
    TYPE_OTHER = "other"

    ADVISORY_TYPE_CHOICES = [
        (TYPE_SECURITY_WARNING, "Security Warning"),
        (TYPE_PUBLIC_SAFETY, "Public Safety Alert"),
        (TYPE_CRIME_ALERT, "Crime Alert"),
        (TYPE_EMERGENCY_ALERT, "Emergency Alert"),
        (TYPE_TRAFFIC_SAFETY, "Traffic Safety Alert"),
        (TYPE_COMMUNITY_ALERT, "Community Alert"),
        (TYPE_MISSING_PERSON, "Missing Person Alert"),
        (TYPE_OTHER, "Other"),
    ]

    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    PRIORITY_CRITICAL = "critical"

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
        (PRIORITY_CRITICAL, "Critical"),
    ]

    title = models.CharField(max_length=250)
    advisory_type = models.CharField(
        max_length=40,
        choices=ADVISORY_TYPE_CHOICES
    )
    district = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)

    summary = models.CharField(max_length=500, blank=True)
    message = models.TextField()

    recommended_action = models.TextField(blank=True)

    issuing_organization = models.CharField(
        max_length=250,
        blank=True
    )

    contact_information = models.CharField(
        max_length=255,
        blank=True
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM
    )

    image = models.ImageField(
        upload_to="security/advisories/",
        blank=True,
        null=True
    )

    start_date = models.DateTimeField(
        blank=True,
        null=True
    )

    end_date = models.DateTimeField(
        blank=True,
        null=True
    )

    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return self.title
    
    
class MissingPersonCommunityNotice(models.Model):

    TYPE_MISSING_PERSON = "missing_person"
    TYPE_FOUND_PERSON = "found_person"
    TYPE_COMMUNITY_NOTICE = "community_notice"
    TYPE_PUBLIC_NOTICE = "public_notice"
    TYPE_IDENTIFICATION_REQUEST = "identification_request"
    TYPE_OTHER = "other"

    NOTICE_TYPE_CHOICES = [
        (TYPE_MISSING_PERSON, "Missing Person"),
        (TYPE_FOUND_PERSON, "Found Person"),
        (TYPE_COMMUNITY_NOTICE, "Community Notice"),
        (TYPE_PUBLIC_NOTICE, "Public Notice"),
        (TYPE_IDENTIFICATION_REQUEST, "Identification Request"),
        (TYPE_OTHER, "Other"),
    ]

    STATUS_ACTIVE = "active"
    STATUS_RESOLVED = "resolved"
    STATUS_CLOSED = "closed"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_RESOLVED, "Resolved"),
        (STATUS_CLOSED, "Closed"),
    ]

    title = models.CharField(max_length=250)

    notice_type = models.CharField(
        max_length=40,
        choices=NOTICE_TYPE_CHOICES
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    location = models.CharField(
        max_length=255,
        blank=True
    )

    summary = models.CharField(
        max_length=500,
        blank=True
    )

    description = models.TextField()

    person_name = models.CharField(
        max_length=200,
        blank=True
    )

    age = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=50,
        blank=True
    )

    physical_description = models.TextField(
        blank=True
    )

    last_seen_location = models.CharField(
        max_length=255,
        blank=True
    )

    last_seen_date = models.DateTimeField(
        blank=True,
        null=True
    )

    contact_information = models.CharField(
        max_length=255,
        blank=True
    )

    issuing_organization = models.CharField(
        max_length=250,
        blank=True
    )

    image = models.ImageField(
        upload_to="security/notices/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-is_featured",
            "-created_at"
        ]

    def __str__(self):
        return self.title
    
class SecurityFacilityContact(models.Model):

    TYPE_POLICE = "police"
    TYPE_FIRE_RESCUE = "fire_rescue"
    TYPE_EMERGENCY = "emergency"
    TYPE_COMMUNITY_SAFETY = "community_safety"
    TYPE_SECURITY_OFFICE = "security_office"
    TYPE_DISASTER_RESPONSE = "disaster_response"
    TYPE_OTHER = "other"

    FACILITY_TYPE_CHOICES = [
        (TYPE_POLICE, "Police Facility"),
        (TYPE_FIRE_RESCUE, "Fire & Rescue Facility"),
        (TYPE_EMERGENCY, "Emergency Facility"),
        (TYPE_COMMUNITY_SAFETY, "Community Safety Facility"),
        (TYPE_SECURITY_OFFICE, "Security Office"),
        (TYPE_DISASTER_RESPONSE, "Disaster Response Facility"),
        (TYPE_OTHER, "Other Security Facility"),
    ]

    name = models.CharField(
        max_length=250
    )

    facility_type = models.CharField(
        max_length=40,
        choices=FACILITY_TYPE_CHOICES
    )

    district = models.CharField(
        max_length=100
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    location = models.CharField(
        max_length=255
    )

    address = models.CharField(
        max_length=255,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    phone_number = models.CharField(
        max_length=100,
        blank=True
    )

    emergency_number = models.CharField(
        max_length=100,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    operating_hours = models.CharField(
        max_length=255,
        blank=True
    )

    contact_person = models.CharField(
        max_length=200,
        blank=True
    )

    image = models.ImageField(
        upload_to="security/facilities/",
        blank=True,
        null=True
    )

    is_emergency_facility = models.BooleanField(
        default=False
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-is_emergency_facility",
            "-is_featured",
            "name",
        ]

    def __str__(self):
        return self.name
    
class SecurityReportRequest(models.Model):

    TYPE_GENERAL_SECURITY = "general_security"
    TYPE_INFORMATION_REQUEST = "information_request"
    TYPE_SAFETY_CONCERN = "safety_concern"
    TYPE_COMMUNITY_SECURITY = "community_security"
    TYPE_FACILITY_REQUEST = "facility_request"
    TYPE_ADVISORY_REQUEST = "advisory_request"
    TYPE_OTHER = "other"

    REQUEST_TYPE_CHOICES = [
        (TYPE_GENERAL_SECURITY, "General Security Report"),
        (TYPE_INFORMATION_REQUEST, "Security Information Request"),
        (TYPE_SAFETY_CONCERN, "Safety Concern"),
        (TYPE_COMMUNITY_SECURITY, "Community Security Request"),
        (TYPE_FACILITY_REQUEST, "Security Facility Request"),
        (TYPE_ADVISORY_REQUEST, "Security Advisory Request"),
        (TYPE_OTHER, "Other Security Request"),
    ]

    STATUS_SUBMITTED = "submitted"
    STATUS_RECEIVED = "received"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_RECEIVED, "Received"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_REJECTED, "Rejected"),
    ]

    citizen_name = models.CharField(
        max_length=200
    )

    phone_number = models.CharField(
        max_length=30
    )

    email = models.EmailField(
        blank=True
    )

    district = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=255,
        blank=True
    )

    request_type = models.CharField(
        max_length=40,
        choices=REQUEST_TYPE_CHOICES
    )

    subject = models.CharField(
        max_length=250
    )

    description = models.TextField()

    attachment = models.FileField(
        upload_to="security/requests/",
        blank=True,
        null=True
    )

    reference_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_SUBMITTED
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        if not self.reference_number:
            self.reference_number = (
                f"SRR-{uuid.uuid4().hex[:8].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_number} - {self.subject}"
    