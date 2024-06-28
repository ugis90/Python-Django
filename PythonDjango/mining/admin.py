from django.contrib import admin
from .models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "advertiser_name",
        "publication_date",
        "submission_deadline",
        "bvpz_code",
    )
    search_fields = ("title", "advertiser_name", "bvpz_code")
    list_filter = ("publication_date", "submission_deadline")


# Alternatively, if you prefer not using the decorator
# admin.site.register(Advertisement, AdvertisementAdmin)
