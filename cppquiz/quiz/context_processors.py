from django.conf import settings

def constants(request):
    return {
        'CPP_STD': settings.CPP_STD,
        'TOP_WARNING': settings.TOP_WARNING,
    }
