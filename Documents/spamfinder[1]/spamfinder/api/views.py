import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import ClientUser, PhoneNumber, Contact
from .serializers import ContactSerializer, PhoneNumberSerializer, UserSerializer, SpamReportSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Case, When, Value, IntegerField

@csrf_exempt
def index(request):
    return HttpResponse("API testing route.")

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data['name']
            phone = data['phone']
            email = data.get('email')
            password = data['password']

            if ClientUser.objects.filter(phone=phone).exists():
                return JsonResponse({'error': 'Phone number already registered'}, status=400)

            # Create a ClientUser object. 
            user = ClientUser(name=name, phone=phone, email=email, password=make_password(password))
            user.save()

            # Check if PhoneNumber already exists, if yes, then use it, if no create otherwise
            pnumber = PhoneNumber.objects.filter(number=phone).first()
            if pnumber is None:
                phone_number = PhoneNumber(number=phone)
                phone_number.save()
                pnumber = phone_number

            # Save the contact.
            contact = Contact(name=name, user=user, phone_number=pnumber, is_registered=True)
            contact.save()

            return JsonResponse({'message': 'User registered successfully'}, status=201)
        except KeyError:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone = data['phone']
            password = data['password']

            user = authenticate(request, phone=phone, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@login_required
def protected_route(request):
    return JsonResponse({'access': 'success'}, status=200)

# ----------------------------------- SEARCH --------------------------------------

@csrf_exempt
@login_required
def search_by_name(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data["name"]
        if not name:
            return JsonResponse({"error": "Name parameter is required"}, status=400)

        # First list the results where name starts with the string.
        # Then the ones which match the string in middle.
        contacts = Contact.objects.annotate(
            starts_with=Case(
                When(name__istartswith=name, then=Value(1)),
                When(name__icontains=name, then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).filter(
            Q(name__istartswith=name) | Q(name__icontains=name)
        ).order_by('starts_with', 'name')
        results = {
            "contacts": [ContactSerializer.serialize(contact) for contact in contacts]
        }
        return JsonResponse(results)



@csrf_exempt
@login_required
def search_by_phone_number(request):
    if request.method == "POST":
        data = json.loads(request.body)
        phone_number = data["phone_number"]

        results = {}

        # Check if phone number has contact which is registered.
        phone_number_obj = PhoneNumber.objects.get(number=phone_number)
        if phone_number_obj is not None:
            contact = phone_number_obj.contacts.filter(is_registered=True).first()
            if contact is not None:
                results = {
                    'Contact' : [ContactSerializer.serialize(contact)]
                }
                return JsonResponse({
                    "message": "User already registered",
                    "data": results,
                    "spam_count": phone_number_obj.report_count
                })

        if not phone_number:
            return JsonResponse({"error": "Phone number parameter is required"}, status=400)

        # Return all possible contacts related to that number
        phone_number_obj = PhoneNumber.objects.filter(number=phone_number).first()
        if not phone_number_obj:
            return JsonResponse({"error": "Phone number not found"}, status=404)
        contacts = phone_number_obj.contacts.all()
        results = {
            "contacts": [ContactSerializer.serialize(contact) for contact in contacts],
            "spam_count": phone_number_obj.report_count
        }
        return JsonResponse(results)

@login_required
@csrf_exempt
def report_spam(request):
    if(request.method == "POST"):
        data = json.loads(request.body)
        phone_number = data["phone_number"]
        spam_target = PhoneNumber.objects.get(number=phone_number)
        if spam_target is not None:
            count = spam_target.report_count
            spam_target.report_count = count + 1
            spam_target.save()
            return JsonResponse({"message": "Spam reported successfully"})
        else:
            return JsonResponse({"message": "This user does not exist"})
        