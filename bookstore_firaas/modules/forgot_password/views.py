import secrets

import environ
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from bookstore_firaas.modules.user.models import User
from bookstore_firaas.modules.user.serializers import UserSerializer

# reading .env file
env = environ.Env()


@permission_classes((permissions.AllowAny,))
class ForgotPasswordViews(APIView):

    def post(self, request):
        # Check username
        user = User.objects.filter(email=request.data['email']).first()
        
        if user is not None:
            new_password = secrets.token_hex(2)

            serializer = UserSerializer(user, data={
                "password": new_password
            }, partial=True)
        
            if serializer.is_valid():
                serializer.save()
                
                message = Mail(
                    from_email=env('MAIL_SENDER_NAME'),
                    to_emails=user.email,
                    subject='Online Course - Your New Password',
                    html_content="<strong>Your new password is " + new_password + "</strong>"
                )
                try:
                    sg = SendGridAPIClient(env('MAIL_KEY'))
                    response = sg.send(message)
                except Exception as e:
                    print(e)
            else:
                print(serializer.errors)

        return Response({'success': 'success', "data": "please check your email"}, status=200)
                