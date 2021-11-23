from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import Group
from django.template.response import TemplateResponse
from django.db.models import Count
from django.contrib.auth.models import User

from .models import Leave


class LeaveRequest(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if is_superuser:
            disabled_fields |= {
                'leave_text', 'leave_taken_date', 'user'
            }

        else:
            disabled_fields |= {
                'leave_approved_status', 'user'
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form

    def save_model(self, request, obj, form, change):
        if not change:
            # the object is being created, so set the user
            obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(LeaveRequest, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('all/', self.admin_site.admin_view(self.my_view, cacheable=True))
        ]
        return my_urls + urls

    def my_view(self, request):
        my_data = Leave.objects.all().values('user_id', 'leave_month').annotate(total=Count('user_id'))
        context = dict(
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            leave_data=my_data,
        )
        return TemplateResponse(request, "leave.html", context)

    fields = ('leave_text', 'leave_approved_status', 'leave_taken_date')
    # readonly_fields = ['leave_text', 'leave_taken_date', 'user']
    list_display = ('leave_text', 'leave_taken_date', 'leave_approved_status', 'user')
    list_filter = ('leave_taken_date',)


admin.site.register(Leave, LeaveRequest)
admin.site.unregister(Group)
