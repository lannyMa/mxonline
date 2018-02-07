from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from organization.models import CourseOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class OrgView(View):  # 课程机构列表页
    def get(self, request):
        all_orgs = CourseOrg.objects.all()  # 所有课程机构

        all_citys = CityDict.objects.all()  # 所有城市列表

        # 取出筛选城市
        city_id = request.GET.get("city", "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 取出筛选培训机构
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        org_nums = all_orgs.count()  # 多少家课程机构
        # 分页模块
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # all_orgs = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            "all_orgs": orgs,
            "all_citys": all_citys,
            'org_count': org_nums,
            'city_id': city_id,
            'category': category,
        })
