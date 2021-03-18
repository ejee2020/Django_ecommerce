from django.shortcuts import render
from .forms import *
from .models import *
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.base import View
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.


def support_create(request):
    if request.method == 'POST':
        # 입력받은 정보를 후처리
        form = SupportCreateForm(request.POST)
        if form.is_valid():
            support = form.save()
            return render(request, 'support/created.html', {'support': support})
    else:
        form = SupportCreateForm()
    return render(request, "support/support.html", {"form": form})


class SupportCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)

        form = SupportCreateForm(request.POST)
        if form.is_valid():
            support = form.save(commit=False)
            data = {
                "support_id": support.id
            }
            support.save()
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)
