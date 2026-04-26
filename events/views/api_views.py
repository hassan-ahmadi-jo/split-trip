from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .. import models, serializers

class HomeAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request: Request):
        user = request.user
        memberships = user.memberships.all().order_by('-joined_at')[:6]
        join_requests = user.join_requests.all().order_by('-requested_at')[:4]

        serializer_memberships = serializers.EventMembershipSerializer(memberships, many = True)
        serializer_join_requests = serializers.EventJoinrequestSerializer(join_requests, many = True)

        return Response({'memberships': serializer_memberships.data, 'join_requests': serializer_join_requests.data}, status = status.HTTP_200_OK)
