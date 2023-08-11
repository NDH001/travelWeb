from django.urls import reverse_lazy
from django.http import JsonResponse


def ajax_check_login(view_func):
    def wrapper(*args, **kwargs):
        # set self.user = request.user
        args[0].user = args[1].user
        # print(args[1].user)
        # check if request.user is authenticated
        if args[1].user.is_anonymous:
            # Redirect the user to the login page
            login_url = reverse_lazy("userdata:login")
            return JsonResponse({"message": "login_required", "login_url": login_url})

        # User is logged in, proceed to the view function
        return view_func(*args, **kwargs)

    return wrapper
