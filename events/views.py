import csv
import qrcode
from io import BytesIO, StringIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event, EventRegistration, CheckIn
from .serializers import EventSerializer, EventRegistrationSerializer, CheckInSerializer

from users.models import User



class EventRegistrationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = EventRegistrationSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        event = Event.objects.get(id=event_id)

        
        if self.request.user.role != 'host':
            raise PermissionDenied("You do not have permission to view registrations.")

        
        return EventRegistration.objects.filter(event=event)




class EventCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.role != 'host': 
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        
        serializer = EventRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
           
            registration = serializer.save()  
            
           
            event = registration.event
            user = request.user

            
            qr_code_file = self.generate_qr_code(user.studentID, event.title)

            
            self.send_registration_email(user, event, qr_code_file)

            return Response({"message": "Registration successful and email sent."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_qr_code(self, student_id, event_title):
        
        qr_data = f"Student ID: {student_id}\nEvent: {event_title}"
        qr = qrcode.make(qr_data)
        
       
        qr_image = BytesIO()
        qr.save(qr_image, format='PNG')
        qr_image.seek(0)
        
        
        return InMemoryUploadedFile(qr_image, None, 'qr_code.png', 'image/png', qr_image.tell(), None)

    def send_registration_email(self, user, event, qr_code_file):
       
        subject = 'Registration Confirmation for Event'
        
        
        email_body = render_to_string('registration_confirmation_email.html', {
            'full_name': user.full_name,
            'event': event,
        })
        
       
        email = EmailMultiAlternatives(
            subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        
        
        email.attach('qr_code.png', qr_code_file.read(), 'image/png')

        
        email.content_subtype = "html"
        email.mixed_subtype = "related"
        email.attach_alternative(email_body, "text/html")

    
        try:
            email.send()
        except Exception as e:
            print(f"Error sending email: {e}")


class EventRegistrationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  
    serializer_class = EventRegistrationSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        event = Event.objects.get(id=event_id)

      
        if self.request.user.role != 'host':
            raise PermissionDenied("You do not have permission to view registrations.")

       
        return EventRegistration.objects.filter(event=event)
    



from django.contrib.auth import get_user_model

class CheckInView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        student_id = request.data.get('studentID')
        event_id = request.data.get('event_id')

        if request.user.role == 'host':
            is_host = True
        elif request.user.role == 'student':
            is_host = False
            if student_id != str(request.user.studentID):
                return Response({"detail": "You can only check-in yourself."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        try:
            event = Event.objects.get(id=event_id)
            user = get_user_model().objects.get(studentID=student_id)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        except get_user_model().DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if CheckIn.objects.filter(user=user, event=event).exists():
            return Response({"detail": "User already checked in for this event"}, status=status.HTTP_400_BAD_REQUEST)

        check_in = CheckIn.objects.create(user=user, event=event)
        serializer = CheckInSerializer(check_in)

        return Response(serializer.data, status=status.HTTP_201_CREATED)





class CheckInExportView(APIView):

    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
       
        if request.user.role != 'host':
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

      
        event_id = request.data.get('event_id')

        if not event_id:
            return Response({"detail": "Event ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        checkins = CheckIn.objects.filter(event=event)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{event.title}_checkins.csv"'

        writer = csv.writer(response)
        writer.writerow(['Student ID', 'Full Name', 'Event', 'Check-in Time'])  

        for checkin in checkins:
            writer.writerow([checkin.user.studentID, checkin.user.full_name, event.title, checkin.check_in_time.strftime("%Y-%m-%d %H:%M:%S")
])

        return response


class EventCheckInSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id, *args, **kwargs):
       
        if request.user.role != 'host':
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

       
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        
        checkins = CheckIn.objects.filter(event=event)

      
        total_checkins = checkins.count()
        total_registered = event.eventregistration_set.count()

        summary = {
            'event_title': event.title,
            'total_checkins': total_checkins,
            'total_registered': total_registered,
            'checkin_percentage': (total_checkins / total_registered * 100) if total_registered > 0 else 0
        }

        return Response(summary)
