# api/serializers.py
class PhoneNumberSerializer:
    @staticmethod
    def serialize(phone_number):
        return {
            "id": phone_number.id,
            "number": phone_number.number,
        }

class ContactSerializer:
    @staticmethod
    def serialize(contact):
        return {
           
            "name": contact.name,
            
        }

class UserSerializer:
    @staticmethod
    def serialize(user):
        return {
            "name": user.name,
            "phone_number": user.phone,
        }

    @staticmethod
    def contact_serialize(user):
        return {
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone,
        }

class SpamReportSerializer:
    @staticmethod
    def serialize(spam_report):
        return {
            "phone_number": spam_report.phone_number,
            "report_count": spam_report.report_count,
        }
