from django.http import JsonResponse
from django.views.decorators.http import require_GET

from autonumber.ui.models import Name, Repository


@require_GET
def autocomplete_names(request):
    term = request.GET.get("term", "").lower()
    results = (
        Name.objects.filter(initials__startswith=term)
        .order_by("initials")
        .values_list("initials", flat=True)
    )
    return JsonResponse(list(results), safe=False)


@require_GET
def autocomplete_repositories(request):
    term = request.GET.get("term", "").lower()
    results = (
        Repository.objects.filter(name__startswith=term)
        .order_by("name")
        .values_list("name", flat=True)
    )
    return JsonResponse(list(results), safe=False)
