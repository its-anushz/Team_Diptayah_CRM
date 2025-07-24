from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                return redirect("home")
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.exception(f"Error in unauthenticated_user decorator: {e}")
            return HttpResponse("An unexpected error occurred.", status=500)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            try:
                # Allow superuser bypass
                if request.user.is_superuser:
                    return view_func(request, *args, **kwargs)

                groups = []
                if request.user.groups.exists():
                    groups = [g.name for g in request.user.groups.all()]
                    print("DEBUG: User groups are", groups)

                if any(group in allowed_roles for group in groups):
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied("You are not authorized to view this page.")
            except PermissionDenied as e:
                logger.warning(f"PermissionDenied in allowed_users: {e}")
                return HttpResponse(str(e), status=403)
            except KeyError as e:
                logger.error(f"KeyError in allowed_users: {e}")
                return HttpResponse("A permission configuration error occurred.", status=500)
            except Exception as e:
                logger.exception(f"Unexpected error in allowed_users: {e}")
                return HttpResponse("An unexpected error occurred.", status=500)
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            groups = []
            if request.user.groups.exists():
                groups = [g.name for g in request.user.groups.all()]
                print("DEBUG: User groups are", groups)

            if "customer" in groups:
                return redirect("user")
            elif "admin" in groups:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied("You are not authorized to view this page.")
        except PermissionDenied as e:
            logger.warning(f"PermissionDenied in admin_only: {e}")
            return HttpResponse(str(e), status=403)
        except KeyError as e:
            logger.error(f"KeyError in admin_only: {e}")
            return HttpResponse("A permission configuration error occurred.", status=500)
        except Exception as e:
            logger.exception(f"Unexpected error in admin_only: {e}")
            return HttpResponse("An unexpected error occurred.", status=500)
    return wrapper_function
