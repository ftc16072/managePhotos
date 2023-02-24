from django.http import HttpResponse


def upload(request):
  return HttpResponse("Photo Upload")


def search(request):
  return HttpResponse("Photo Search")