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

class IssueStatusAPI():
    queryset = models.IssueStatus.objects.all()
    serializer_class = serializers.IssueStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class IssueStatusList(
    IssueStatusAPI,
    generics.ListCreateAPIView):
    pass

class IssueStatusDetail(
    IssueStatusAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ConversationAPI():
    queryset = models.Conversation.objects.all()
    serializer_class = serializers.ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversationList(
    ConversationAPI,
    generics.ListCreateAPIView):
    pass

class ConversationDetail(
    ConversationAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ConversationChannelAPI():
    queryset = models.ConversationChannel.objects.all()
    serializer_class = serializers.ConversationChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversationChannelList(
    ConversationChannelAPI,
    generics.ListCreateAPIView):
    pass

class ConversationChannelDetail(
    ConversationChannelAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ConversationEmailAPI():
    queryset = models.ConversationEmail.objects.all()
    serializer_class = serializers.ConversationEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversationEmailList(
    ConversationEmailAPI,
    generics.ListCreateAPIView):
    pass

class ConversationEmailDetail(
    ConversationEmailAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ConversationEmailStatusAPI():
    queryset = models.ConversationEmailStatus.objects.all()
    serializer_class = serializers.ConversationEmailStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversationEmailStatusList(
    ConversationEmailStatusAPI,
    generics.ListCreateAPIView):
    pass

class ConversationEmailStatusDetail(
    ConversationEmailStatusAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass