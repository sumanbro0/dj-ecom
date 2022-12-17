from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.models import Profile
from products.models import Product
from vendor.models import VerifyImage

# Create your views here.
def verify(request, username):
    try:
        usr = Profile.objects.get(user__username=username)
    except Exception as e:
        print(e)
        messages.warning(request, "you are not logged in")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    if request.FILES:
        try:
            front = request.FILES.get("front")
            back = request.FILES.get("back")
            verify_image = VerifyImage(profile=usr, front=front, back=back)
            verify_image.save()
            messages.success(
                request,
                "your files have been submitted.we will verify and upgrade you to vendor soon.this process can take upto 2 days..",
            )
            return redirect("profile")
        except Exception as e:
            print(e)
            messages.warning(request, "process failed! please try again later")
            return redirect("profile")
    return render(request, "vendor/verify.html")
