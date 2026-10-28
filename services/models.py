from django.db import models


class GovernmentService(models.Model):

    CATEGORY_CHOICES = [
        ("health", "Health Services"),
        ("education", "Education"),
        ("agriculture", "Agriculture"),
        ("water", "Water & Environment"),
        ("public_works", "Public Works & Transport"),
        ("energy", " Energy  & Mineral Development"),
        
       
        ("security", "Security"),
        ("urban_planning", "Lands, Housing & Urban Planning"),
        
       
        
    ]

    name = models.CharField(max_length=200)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    short_description = models.CharField(
        max_length=300
    )

    description = models.TextField()

    icon = models.CharField(
        max_length=100,
        default="bi-grid"
    )

    estimated_days = models.PositiveIntegerField(
        default=5
    )

    required_information = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):

    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("received", "Received"),
        ("in_progress", "In Progress"),
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("rejected", "Rejected"),
    ]

    service = models.ForeignKey(
        GovernmentService,
        on_delete=models.CASCADE,
        related_name="requests"
    )

    citizen_name = models.CharField(
        max_length=200
    )

    citizen_phone = models.CharField(
        max_length=30,
        blank=True
    )

    citizen_district = models.CharField(
        max_length=100,
        blank=True
    )

    description = models.TextField()

    reference_number = models.CharField(
        max_length=50,
        unique=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="submitted"
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.reference_number} - {self.service.name}"