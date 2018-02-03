from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from organization.models import CourseOrg, CityDict


class OrgView(View):  # 课程机构列表页
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        return render(request, 'org-list.html', {
            "all_orgs": all_orgs,
            "all_citys": all_citys
        })
