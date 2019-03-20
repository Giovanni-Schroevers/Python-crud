from django.http import HttpResponse, JsonResponse
from .models import User, Role
from django.views.decorators.csrf import csrf_exempt
import json
import hashlib


def users(request):
    try:
        data = User.objects.values()
    except Exception as e:
        return JsonResponse({"Code": "500", "Message": "Internal server error, " + str(e)}, status=500)

    if not data:
        return JsonResponse({"Code": "404", "Message": "No users found"}, status=404)
    return JsonResponse({"data": list(data)}, safe=False)


def get_user(request, id):
    try:
        data = User.objects.filter(id=id).values()
    except Exception as e:
        return JsonResponse({"Code": "500", "Response": "Internal server error, " + str(e)}, status=500)

    if not data:
        return JsonResponse({"Code": "404", "Response": "User {0} not found".format(id)}, status=404)
    return JsonResponse(list(data), safe=False)


@csrf_exempt
def new_user(request):
    data = json.loads(request.body)

    try:
        user = User()
        if not data["firstname"]:
            return JsonResponse({"Code": "400", "Response": "Bad request, missing firstname value"}, status=400)
        if not data["lastname"]:
            return JsonResponse({"Code": "400", "Response": "Bad request, missing lastname value"}, status=400)
        if not data["email"]:
            return JsonResponse({"Code": "400", "Response": "Bad request, missing email value"}, status=400)
        if not data["password"]:
            return JsonResponse({"Code": "400", "Response": "Bad request, missing password value"}, status=400)

        user.firstname = data["firstname"]
        user.lastname = data["lastname"]
        user.email = data["email"]
        user.password = hashlib.sha512(data["password"].encode('utf-8')).hexdigest()
        if data["role"]:
            user.role = Role.objects.filter(id=data["role"]).get()
        user.save()
    except Exception as e:
        return JsonResponse({"Code": "500", "Response": "Internal server error, " + str(e)}, status=500)

    return JsonResponse({"id": user.id}, status=201, safe=False)


@csrf_exempt
def update_user(request, id):
    data = json.loads(request.body)

    try:
        if User.objects.filter(id=id).count() > 0:
            user = User.objects.filter(id=id).get()
            if "firstname" in data:
                user.firstname = data["firstname"]
            if "lastname" in data:
                user.lastname = data["lastname"]
            if "email" in data:
                user.email = data["email"]
            if "password" in data:
                user.password = hashlib.sha512(data["password"].encode('utf-8')).hexdigest()
            if "role" in data:
                user.role = Role.objects.filter(id=data["role"]).get()
            if "banned" in data:
                user.banned = data["banned"]
            user.save()
        else:
            return JsonResponse({"Code": "404", "Response": "User {0} not found".format(id)}, status=404)
    except Exception as e:
        return JsonResponse({"Code": "500", "Response": "Internal server error, " + str(e)}, status=500)

    return JsonResponse({"Code": "200", "Response": "User {0} updated".format(id)}, status=200)


def delete_user(request, id):

    try:
        if User.objects.filter(id=id).count() > 0:
            User.objects.filter(id=id).delete()
        else:
            return JsonResponse({"Code": "404", "Response": "User {0} not found".format(id)}, status=404)
    except Exception as e:
        return JsonResponse({"Code": "500", "Response": "Internal server error, " + str(e)}, status=500)

    return JsonResponse({"Code": "200", "Response": "User {0} deleted".format(id)}, status=200)


def get_role(request, id):
    try:
        data = Role.objects.filter(id=id).values()
    except Exception as e:
        return JsonResponse({"Code": "500", "Response": "Internal server error, " + str(e)}, status=500)

    if not data:
        return JsonResponse({"Code": "404", "Response": "Role {0} not found".format(id)}, status=404)

    return JsonResponse(list(data), safe=False)


def handler404(request, *arg, **argv):
    return JsonResponse({"Code": "404", "Response": "Route not found"}, status=404)


def handler500(request, *arg, **argv):
    return JsonResponse({"Code": "500", "Response": "Internal server error"}, status=500)
