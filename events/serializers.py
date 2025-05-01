from rest_framework import serializers
from .models import Event
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import csv
from .models import CheckIn
from .models import EventRegistration
from rest_framework.fields import DateTimeField
from users.models import User 

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'location', 'date', 'time', 'mode']




class EventRegistrationSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(write_only=True)  

    class Meta:
        model = EventRegistration
        fields = ['event_id']

    def validate(self, data):
        user = self.context['request'].user
        event_id = data['event_id']

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise serializers.ValidationError("Event not found.")

       
        if EventRegistration.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("You have already registered for this event.")

        data['event'] = event 
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        event = validated_data['event']
        return EventRegistration.objects.create(user=user, event=event)


class CheckInSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    user_student_id = serializers.CharField(source='user.studentID', read_only=True)
    check_in_time = DateTimeField(format="%Y-%m-%d %H:%M:%S")  

    class Meta:
        model = CheckIn
        fields = ['user_full_name', 'user_student_id', 'event', 'check_in_time']


class CheckInExportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id, *args, **kwargs):
        
        if request.user.role != 'host':
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        try:
            event = Event.objects.get(id=event_id)
            if event.host != request.user:
                return Response({"detail": "You do not have permission to access this event's data."}, status=status.HTTP_403_FORBIDDEN)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        checkins = CheckIn.objects.filter(event=event)

        
        return self.export_to_csv(checkins)

    def export_to_csv(self, checkins):
       
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="checkins.csv"'
        writer = csv.writer(response)
        writer.writerow(['Student ID', 'Full Name', 'Event', 'Check-in Time'])

        for checkin in checkins:
            writer.writerow([checkin.user.studentID, checkin.user.full_name, checkin.event.title, checkin.check_in_time])

        return response
