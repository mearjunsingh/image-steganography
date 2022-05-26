from django.shortcuts import render

handler400 = "handler400"
handler403 = "handler403"
handler404 = "handler404"
handler500 = "handler500"


def handler400(request, exception=None):
    pass


def handler403(request, exception=None):
    pass


def handler404(request, exception=None):
    pass


def handler500(request, exception=None):
    pass
