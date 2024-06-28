from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Advertisement
from .forms import RegisterForm, LoginForm
from .scraper import scrape_website
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
import json
import logging


@ensure_csrf_cookie
def home(request):
    return render(request, "mining/home.html")


def ad_list(request):
    ads = Advertisement.objects.all()
    return render(request, "mining/ad_list.html", {"ads": ads})


@method_decorator(csrf_protect, name="dispatch")
class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "mining/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "User registered successfully"})
        else:
            print(form.errors)
        return JsonResponse({"error": form.errors}, status=400)


logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "mining/login.html", {"form": form})

    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            logger.debug("Received data: %s", data)  # Debugging statement
            username = data.get("username")
            password = data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"message": "User logged in successfully"})
            else:
                return JsonResponse(
                    {"error": "Invalid username or password"}, status=400
                )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid data"}, status=400)


class DataRetrievalView(View):
    def get(self, request):
        ads = Advertisement.objects.all().values()
        ads_list = list(ads)

        for ad in ads_list:
            if ad["publication_date"]:
                ad["publication_date"] = ad["publication_date"].strftime("%Y-%m-%d")
            if ad["submission_deadline"]:
                ad["submission_deadline"] = ad["submission_deadline"].strftime(
                    "%Y-%m-%d"
                )

        print("Advertisements:", ads_list)
        return JsonResponse(ads_list, safe=False)


class ScrapeDataView(View):
    def get(self, request):
        url = "https://cvpp.eviesiejipirkimai.lt/"
        purchase_type = request.GET.get("purchase_type", "Unknown")
        advertisement_type = request.GET.get("advertisement_type", "Unknown")
        scrape_website(url, purchase_type, advertisement_type)
        return HttpResponse("Scraping completed.")
