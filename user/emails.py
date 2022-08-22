import random

from django.conf import settings
from django.core.mail import send_mail


def send_otp_via_email(email):
    subject = "Account Verification Email"
    otp = random.randint(100000, 999999)
    message = f"Your verification code is {otp}"
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    # user_obj = User.objects.get(email=email)
    # otp_obj = Verification_Code.objects.create(user=user_obj)
    # otp_obj.otp = otp
    # otp_obj.expiry = datetime.datetime.now() + datetime.timedelta(minutes=15)
    # otp_obj.save()
    # print(otp_obj)
    return otp
