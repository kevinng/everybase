from . import models
from . import serializers
from rest_framework import generics, permissions

class IssueAPI():
    queryset = models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

class IssueList(
    IssueAPI,
    generics.ListCreateAPIView):
    pass

class IssueDetail(
    IssueAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class IssueTagAPI():
    queryset = models.IssueTag.objects.all()
    serializer_class = serializers.IssueTagSerializer
    permission_classes = [permissions.IsAuthenticated]

class IssueTagList(
    IssueTagAPI,
    generics.ListCreateAPIView):
    pass

class IssueTagDetail(
    IssueTagAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass