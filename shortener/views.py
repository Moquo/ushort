from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Url
import random
import string
from django.utils import timezone
import re
from django.conf import settings

# Generate a random string
def random_string(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([random.choice(chars) for x in range(length)])

# Short a url
def short_url(url_to_short):
    # Check if url already exists
    url_id = random_string(8)
    stop = False
    while not stop:
        # Are there any urls
        if not Url.objects.all():
            stop = True

        # Loop over every Url and then check it
        # TODO: Use filter
        for x in Url.objects.all():
            if x.url_id == url_id:
                url_id = random_string(8)
            else:
                stop = True

    # Add url ot database
    shorten_url = Url(url_id=random_string(8), orig_url=url_to_short, created_at=timezone.now())
    shorten_url.save()

    # Return the shorten url
    return shorten_url

def is_url(str):
    # Valid regexes
    url_regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # Return if str matches
    return re.match(url_regex, str) is not None

# Index page
def index(request):
    # Check if a url was sent through a post request
    error = None
    success = None
    if request.method == "POST" and request.POST["url"]:
        url_to_short = request.POST["url"]
        # Check if url_to_short is a valid url
        # TODO: Fix error: If url is empty, no result is printed out
        if not is_url(url_to_short) or url_to_short.strip() == "":
            error = "The entered url is invalid!"
        else:
            shorten_url = short_url(url_to_short)
            success = {
                "orig_url": shorten_url.orig_url,
                "short_url": settings.SERVER_URL + reverse("shortener:redirectUrl", args=[shorten_url.url_id])
            }

    return render(request, "shortener/index.html", {
        "error": error,
        "success": success
    })

# Redirect a user to an url
def redirectUrl(request, url_id):
    # Get the url
    url = get_object_or_404(Url, url_id=url_id)

    # Add 1 to clicks
    url.clicks += 1
    url.save()

    # Redirect
    return redirect(url.orig_url)

# Render the textbox to enter the url_id
def viewUrl(request):
    # Render
    return render(request, "shortener/viewUrl.html", {
        "url_scheme": settings.SERVER_URL + reverse("shortener:redirectUrl", args=["THIS_IS_THE_PART_WHICH_IS_CALLED_THE_URL_ID"]),
        "url_scheme_example": settings.SERVER_URL + reverse("shortener:redirectUrl", args=["abcdefgh"]),
        "base_url": settings.SERVER_URL
    })

# Show url information
def viewUrlInfo(request, url_id):
    # Get the url
    url = get_object_or_404(Url, url_id=url_id)

    # Render the url info page
    return render(request, "shortener/viewUrlInfo.html", {
        "url": url,
        "base_url": settings.SERVER_URL
    })