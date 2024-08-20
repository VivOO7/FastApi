from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from .models import ClientUser, PhoneNumber, Contact
import json

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')  
        self.valid_payload = {
            'name': 'John Doe',
            'phone': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'securepassword'
        }
        self.duplicate_phone_payload = {
            'name': 'Jane Doe',
            'phone': '1234567890',  # Same phone number as valid_payload
            'email': 'jane.doe@example.com',
            'password': 'anotherpassword'
        }

    def test_register_valid_data(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ClientUser.objects.count(), 1)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(PhoneNumber.objects.count(), 1)
        self.assertJSONEqual(
            response.content,
            {'message': 'User registered successfully'}
        )

    def test_register_duplicate_phone(self):
        # Create an initial user
        self.client.post(
            self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        # Attempt to register another user with the same phone number
        response = self.client.post(
            self.url,
            data=json.dumps(self.duplicate_phone_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {'error': 'Phone number already registered'}
        )

    def test_register_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {'error': 'Invalid request method'}
        )

    def test_register_invalid_data(self):
        invalid_payload = {
            'name': 'Invalid User',
            # Missing phone and password fields
            'email': 'invalid.user@example.com'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {'error': 'Invalid data'}
        )



class ProtectedRouteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('protected_route')
        self.user = ClientUser.objects.create_user(
            name='John Doe',
            phone='1234567890',
            email='john.doe@example.com',
            password='securepassword'
        )
        self.client.login(phone='1234567890', password='securepassword')

    def test_protected_route_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'access': 'success'})



class SearchByNameViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('search_by_name')
        self.user = ClientUser.objects.create_user(
            name='John Doe',
            phone='1234567890',
            email='john.doe@example.com',
            password='securepassword'
        )
        self.client.login(phone='1234567890', password='securepassword')
        self.contact = Contact.objects.create(
            name='Jane Doe',
            user=self.user,
            phone_number=PhoneNumber.objects.create(number='1234567890'),
            is_registered=True
        )

    def test_search_by_name(self):
        response = self.client.post(
            self.url,
            data=json.dumps({'name': 'Jane'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('contacts', response.json())


class SearchByPhoneNumberViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('search_by_phone_number')
        self.user = ClientUser.objects.create_user(
            name='John Doe',
            phone='1234567890',
            email='john.doe@example.com',
            password='securepassword'
        )
        self.client.login(phone='1234567890', password='securepassword')
        self.phone_number = PhoneNumber.objects.create(number='1234567890')
        self.contact = Contact.objects.create(
            name='Jane Doe',
            user=self.user,
            phone_number=self.phone_number,
            is_registered=True
        )

    def test_search_by_phone_number(self):
        response = self.client.post(
            self.url,
            data=json.dumps({'phone_number': '1234567890'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'User already registered')
        self.assertIn('data', response_data)
        self.assertIn('Contact', response_data['data'])
        self.assertEqual(response_data['data']['Contact'][0]['name'], 'Jane Doe')
        self.assertIn('spam_count', response_data)


class ReportSpamViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('report_spam')
        self.user = ClientUser.objects.create_user(
            name='John Doe',
            phone='1234567890',
            email='john.doe@example.com',
            password='securepassword'
        )
        self.client.login(phone='1234567890', password='securepassword')
        self.phone_number = PhoneNumber.objects.create(number='1234567890')

    def test_report_spam(self):
        response = self.client.post(
            self.url,
            data=json.dumps({'phone_number': '1234567890'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Spam reported successfully'})
        self.phone_number.refresh_from_db()
        self.assertEqual(self.phone_number.report_count, 1)
