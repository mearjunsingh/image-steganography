from django.shortcuts import render

handler400 = "handler400"
handler403 = "handler403"
handler404 = "handler404"
handler500 = "handler500"


def handler400(request, exception=None):
    ctx = {
        "error_code": 400,
        "error_msg": "400 error",
    }
    return render(request, "error.html", ctx)


def handler403(request, exception=None):
    ctx = {
        "error_code": 400,
        "error_msg": "400 error",
    }
    return render(request, "error.html", ctx)


def handler404(request, exception=None):
    ctx = {
        "error_code": 404,
        "error_msg": "Page not found.",
    }
    return render(request, "error.html", ctx)


def handler500(request, exception=None):
    ctx = {
        "error_code": 500,
        "error_msg": "Something happened. Could complete your action.",
    }
    return render(request, "error.html", ctx)
