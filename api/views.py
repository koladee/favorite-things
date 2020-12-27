from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Profile, Category, List
from .serializers import ProfileSerializer, CategorySerializer, ListSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from datetime import datetime, timezone
import random
import string
from django.db.models import Max


class HomeView(TemplateView):
    template_name = "index.html"


class ProfileEndpoint(APIView):
    # class based view for the profile endpoints and requests
    @csrf_exempt
    def get(self, request):
        if request.method == 'GET':
            # check if the get request has a query parameter(s) to know if request is to fetch for a single user or not
            if_param = request.GET.get('who')
            if if_param is not None:
                # single user request confirmed
                form = request.query_params
                if form['who'] is not None:
                    try:
                        # check if user email exist
                        data = User.objects.get(email=form['who'])
                        try:
                            # authenticate user with submitted password  and return data for single user
                            authenticate(username=data.username, password=form['pass'])
                            login(request, data)
                            resp = {'user': form['who'], 'data': {'username': data.username, 'email': data.email,
                                                                  'fname': data.first_name, 'lname': data.last_name,
                                                                  'mes': 'success'}}
                            return Response(resp)
                        except User.DoesNotExist:
                            resp = {'user': '', 'mes': 'User\'s email or password is incorrect!'}
                            return Response(resp)
                    except User.DoesNotExist:
                        resp = {'user': '', 'mes': 'User\'s email or password is incorrect!'}
                        return Response(resp)
                else:
                    resp = {'user': '', 'mes': 'Invalid request!'}
                    return Response(resp)
            else:
                # return all users as response since there is no query parameter
                profiles = Profile.objects.all()
                serializer = ProfileSerializer(profiles, many=True)
                return Response(serializer.data)
        else:
            resp = {'user': '', 'mes': 'Invalid request!'}
            return Response(resp, 400)

    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                email = form['email']
                username = form['username']
                p1 = form['password']
                p2 = form['password2']
                fname = form['fname']
                lname = form['lname']
                try:
                    # check if email address is a valid email address
                    validate_email(email)
                    try:
                        # check if user with the submitted email address already exist
                        User.objects.get(email=email)
                        resp = {
                            "msg": "Email address already exist!",
                            "done": False
                        }
                        return Response(resp)
                    except User.DoesNotExist:
                        # user with email does not exist, proceed
                        try:
                            # check if a user with the sumitted username exists
                            User.objects.get(username=username)
                            resp = {
                                "msg": "Username already exist!",
                                "done": False
                            }
                            return Response(resp)
                        except User.DoesNotExist:
                            # user with username does not exist, proceed
                            # check if submitted passwords are the same
                            if p1 == p2:
                                # create new user with the submitted credentials
                                user = User.objects.create_user(username=username, email=email, password=p1,
                                                                first_name=fname, last_name=lname)
                                user.save()
                                resp = {
                                    "msg": "New user successfully created!",
                                    "done": True
                                }
                                return Response(resp)
                            else:
                                resp = {
                                    "msg": "Passwords do not match!",
                                    "done": False
                                }
                                return Response(resp)
                except ValidationError:
                    resp = {
                        "msg": "Email address is invalid!",
                        "done": False
                    }
                    return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)

    @csrf_exempt
    def put(self, request):
        # put request to update user's details
        if request.method == 'PUT':
            form = request.data
            if form is not None:
                idd = form['id']
                email = form['email']
                fname = form['fname']
                lname = form['lname']
                try:
                    # check if user exists
                    User.objects.filter(id=idd, email=email)
                    try:
                        # update user's details
                        User.objects.filter(id=idd).update(first_name=fname, last_name=lname)
                        resp = {
                            "msg": "User's details successfully updated!",
                            "done": True
                        }
                        return Response(resp)
                    except User.DoesNotExist:
                        resp = {
                            "msg": "This category does not exit or belongs to you!",
                            "done": False
                        }
                        return Response(resp)
                except User.DoesNotExist:
                    resp = {
                        "msg": "The specified user dose not exist.",
                        "done": False
                    }
                    return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp)


class CategoryEndpoint(APIView):
    # Category class based view for category endpoints
    @csrf_exempt
    def get(self, request):
        # get request
        if request.method == 'GET':
            # check if request has any query parameter to know if request is to display all categories or categories for
            # a specific user
            if_param = request.GET.get('who')
            if if_param is not None:
                # request is for a specific user
                form = request.query_params
                if form['who'] is not None:
                    try:
                        # check if user exists and return all default categories and personal categories
                        ud = User.objects.get(email='admin@favorite.com').profile
                        udd = User.objects.get(email=form['who']).profile
                        cats = Category.objects.filter(user_id__in=[ud, udd]).all()
                        serializer = CategorySerializer(cats, many=True)
                        return Response(serializer.data)
                    except User.DoesNotExist:
                        resp = {'user': '', 'mes': 'User credentials not found!'}
                        return Response(resp)
                else:
                    resp = {'user': '', 'mes': 'Invalid request!'}
                    return Response(resp)
            else:
                # no specified query parameter, return all categories in the system
                cats = Category.objects.all()
                serializer = CategorySerializer(cats, many=True)
                return Response(serializer.data)
        else:
            resp = {'user': '', 'mes': 'Invalid request!'}
            return Response(resp)

    @csrf_exempt
    def post(self, request):
        # POST request to create a new category
        if request.method == 'POST':
            form = request.data
            if form is not None:
                email = form['email']
                name = form['name']
                if name is not None:
                    try:
                        # check if user exist
                        usr = User.objects.get(email=email)
                        ud = usr.profile
                        try:
                            # check if category name already exists for this user
                            Category.objects.get(name=name.lower(), user_id=ud)
                            resp = {
                                "msg": "You already have an existing category with this same name!",
                                "done": False
                            }
                            return Response(resp)
                        except Category.DoesNotExist:
                            # proceed to create category
                            cat = Category.objects.create(name=name.lower(), user_id=ud)
                            cat.save()
                            resp = {
                                "msg": "Category successfully created.",
                                "done": True
                            }
                            return Response(resp)
                    except User.DoesNotExist:
                        resp = {
                            "msg": "Invalid user credential!",
                            "done": False
                        }
                        return Response(resp)

                else:
                    resp = {
                        "msg": "Invalid user credential!",
                        "done": False
                    }
                    return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp)

    @csrf_exempt
    def put(self, request):
        # PUT request to update a category record
        if request.method == 'PUT':
            form = request.data
            if form is not None:
                idd = form['id']
                email = form['email']
                name = form['name']
                try:
                    # check if user exists
                    usr = User.objects.get(email=email)
                    ud = usr.profile.id
                    try:
                        # update record
                        Category.objects.filter(id=idd).update(name=name, user_id=ud)
                        resp = {
                            "msg": "Category successfully updated!",
                            "done": True
                        }
                        return Response(resp)
                    except Category.DoesNotExist:
                        resp = {
                            "msg": "This category does not exit or belongs to you!",
                            "done": False
                        }
                        return Response(resp)
                except User.DoesNotExist:
                    resp = {
                        "msg": "The specified user dose not exist.",
                        "done": False
                    }
                    return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp)


class ListEndpoint(APIView):
    # List class based view for list endpoints
    @csrf_exempt
    def get(self, request):
        # get request to fetch records a single user record or all records
        if request.method == 'GET':
            # check if query parameter is present in the request to indentify if request is for a sinle user
            if_param = request.GET.get('who')
            if if_param is not None:
                # single user confirmed
                form = request.query_params
                if form['who'] is not None:
                    try:
                        # check if user exist
                        udd = User.objects.get(email=form['who']).profile
                        # check if request for a single user is for a specified category or not
                        if_param2 = request.GET.get('cat')
                        if if_param2 is not None:
                            # filter request by the specified category
                            try:
                                cat = Category.objects.get(id=form['cat'])
                                try:
                                    # fetch all list with specified user and category
                                    lists = List.objects.filter(user_id=udd, cat=cat).all().order_by('-id')
                                    # return fetched data
                                    serializer = ListSerializer(lists, many=True)
                                    return Response(serializer.data)
                                except List.DoesNotExist:
                                    resp = {'user': '', 'mes': 'Oops! No record found.'}
                                    return Response(resp)
                            except Category.DoesNotExist:
                                resp = {'user': '', 'mes': 'Specified category does not exist'}
                                return Response(resp)
                        else:
                            # fetch all lists for specified user
                            try:
                                lists = List.objects.filter(user_id=udd).all().order_by('-id')
                                # return fetched data
                                serializer = ListSerializer(lists, many=True)
                                return Response(serializer.data)
                            except List.DoesNotExist:
                                resp = {'user': '', 'mes': 'Oops! No record found.'}
                                return Response(resp)
                    except User.DoesNotExist:
                        resp = {'user': '', 'mes': 'User credentials not found!'}
                        return Response(resp)
                else:
                    resp = {'user': '', 'mes': 'Invalid request!'}
                    return Response(resp)
            else:
                # no query parameter, return all lists on the system
                lists = List.objects.all()
                serializer = ListSerializer(lists, many=True)
                return Response(serializer.data)
        else:
            resp = {'user': '', 'mes': 'Invalid request!'}
            return Response(resp)

    # This is a function to perform the ranking algorithm when a new favorite list is about to be added
    @csrf_exempt
    def process(self, ob):
        # validate data
        title = ob['title']
        description = ob['description']
        try:
            category = Category.objects.get(id=ob['category'])
        except Category.DoesNotExist:
            resp = {
                "done": False,
                "msg": 'Oops! Invalid category specified.'
            }
            return resp
        ranking = ob['ranking']
        try:
            user_id = Profile.objects.get(id=ob['user_id'])
        except Profile.DoesNotExist:
            resp = {
                "done": False,
                "msg": 'Oops! Specified user does not exist'
            }
            return resp
        if title is not None:
            if int(ranking) > 0:
                if category is not None:
                    proceed = True
                    if description is not None:
                        length = len(description)
                        if length >= 1:
                            proceed = True
                        else:
                            proceed = False
                    if proceed is True:
                        # fetch all favorite list that belongs to the specified user, with specified category and same
                        # ranking to see if there will be any duplicate ranking
                        exist = List.objects.filter(ranking__gte=ranking, cat=category, user_id=user_id).all()
                        for each in exist:
                            # loops through the data
                            if int(ranking) == int(each.ranking):
                                # if ranking is equal to the submitted ranking, find the ranking with highest value
                                # under the same category and which belongs to this same user
                                rank = List.objects.filter(cat=category, user_id=user_id).all().aggregate(
                                    Max('ranking'))
                                # print(rank['ranking__max'])
                                # set the ranking of the present loop object to the maximum ranking in the same
                                # category plus 1
                                each.ranking = int(rank['ranking__max']) + 1
                            else:
                                # print(each.ranking)
                                # since they are not equal, let ranking remain
                                each.ranking = each.ranking
                            # update the ranking for the object in the loop to its new value.
                            List.objects.filter(id=each.id).update(ranking=each.ranking)
                        # generate a unique random rid of 10 characters length
                        rand = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
                        # create new object for the submitted data
                        fav = List(rid=rand, title=title, description=description, ranking=ranking, user_id=user_id,
                                   cat=category)
                        fav.save()
                        done = {
                            "done": True,
                            "msg": "Request was successfully added to your favorite list."
                        }
                        return done
                    else:
                        resp = {
                            "done": False,
                            "msg": "Description should not be empty."
                        }
                        return resp
                else:
                    resp = {
                        "done": False,
                        "msg": 'Oops!!! A category must be selected.'
                    }
                    return resp
            else:
                resp = {
                    "done": False,
                    "msg": 'Oops!!! The ranking field is required and it must be greater than zero in value.'
                }
                return resp
        else:
            resp = {
                "done": False,
                "msg": 'Oops!!! The title fields is required.'
            }
            return resp

    @csrf_exempt
    def post(self, request):
        # post request to create a new list record
        if request.method == 'POST':
            form = request.data
            if form is not None:
                email = form['email']
                title = form['title']
                des = form['des']
                cat = form['cat']
                ranking = form['ranking']
                try:
                    # check if user exists
                    usr = User.objects.get(email=email)
                    ud = usr.profile.id
                    ob = {'title': title, 'description': des, 'category': cat, 'ranking': ranking, 'user_id': ud}
                    # run the process() method aove and return reponse from it.
                    return Response(self.process(ob))
                except User.DoesNotExist:
                    resp = {
                        "msg": "User dose not exist.",
                        "done": False
                    }
                    return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp)

    @csrf_exempt
    def put(self, request):
        # put request to update list record and re-rank all lists under the submitted category
        if request.method == 'PUT':
            form = request.data
            if form is not None:
                email = form['email']
                idd = form['id']
                title = form['title']
                des = form['des']
                cat = Category.objects.get(id=form['cat'])
                ranking = form['ranking']
                try:
                    # check if user exist
                    usr = User.objects.get(email=email)
                    ud = usr.profile.id
                    try:
                        # check if specified list exist
                        item = List.objects.get(id=idd, user_id=ud)
                        ob = {'title': '', 'description': '', 'category': '', 'ranking': ''}
                        # get current timestamp
                        now = datetime.now(timezone.utc)
                        time = str(str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "T" + str(
                            now.hour) + ":" + str(now.minute)
                                   + ":" + str(now.second))
                        # do comparison of old title, desc, cat & ranking to detect any changes for log purpose
                        if item.title != title:
                            ob['title'] = "The title changed from <b>" + item.title + "</b> to <b>" + \
                                          title + "</b>(+||+)" + time + "{:||:}"
                        if item.description != des:
                            ob['description'] = "The description changed from <b>" + item.description + "</b> to <b>" +\
                                                des + "</b>(+||+)" + time + "{:||:}"
                        if item.cat != cat:
                            try:
                                cat1 = Category.objects.filter(id=item.cat).first()
                                cat2 = Category.objects.filter(id=cat).first()
                                ob['cat'] = "The category changed from <b>" + cat1.name + "</b> to <b>" + cat2.name +\
                                            "</b>(+||+)" + time + "{:||:}"
                            except Category.DoesNotExist:
                                resp = {
                                    "msg": "Invalid category specified.",
                                    "done": False
                                }
                                return Response(resp)
                        if int(item.ranking) > int(ranking) or int(item.ranking) < int(ranking):
                            ob['ranking'] = "The ranking changed from <b>" + str(item.ranking) + "</b> to <b>" + \
                                            str(ranking) + "</b>(+||+)" + time + "{:||:}"
                        if ob['title'] != "" or ob['description'] != "" or ob['category'] != "" or ob['ranking'] != "":
                            # generate new log if any changes exist
                            log = str(item.log)
                            newlog = str(log + "{:||:}" + ob['title'] + "" + ob['description'] + "" + ob['category']
                                         + "" + ob['ranking'])
                            # update records of the specified list
                            List.objects.filter(id=idd, user_id=ud).update(title=title, description=des, cat=cat,
                                                                           modified_date=datetime.now(timezone.utc),
                                                                           log=newlog, ranking=ranking)
                            # implement the ranking algorithm
                            # fetch all objects with the same category and ranking that belongs to this same user
                            exist = List.objects.filter(ranking__gte=ranking, cat=cat, user_id=item.user_id).all()
                            for each in exist:
                                # loop through fetched objects
                                if int(ranking) == int(each.ranking) and each.id != idd:
                                    # get the maximum rank under the specified category that belongs to
                                    # the specified user
                                    rank = List.objects.filter(cat=cat, user_id=item.user_id).all().aggregate(
                                        Max('ranking'))
                                    # print(rank['ranking__max'])
                                    # add the maximum rank plus 1 for any object that has the same rank
                                    each.ranking = int(rank['ranking__max']) + 1
                                else:
                                    # print(each.ranking)
                                    # let rankin remain
                                    each.ranking = each.ranking
                                # update ranking for objects in the loop
                                List.objects.filter(id=each.id).update(ranking=each.ranking)
                            resp = {"msg": 'success', 'done': True}
                            return Response(resp)
                        else:
                            resp = {"msg": 'No change was made!', 'done': False}
                            return Response(resp)
                    except List.DoesNotExist:
                        resp = {
                            "msg": "Item does not exist on your favorite list.",
                            "done": False
                        }
                        return Response(resp)
                except User.DoesNotExist:
                    resp = {
                        "msg": "User dose not exist.",
                        "done": False
                    }
                    return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            Response(resp)
