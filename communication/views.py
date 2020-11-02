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

class ConversationChatAPI():
    queryset = models.ConversationChat.objects.all()
    serializer_class = serializers.ConversationChatSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversationChatList(
    ConversationChatAPI,
    generics.ListCreateAPIView):
    pass

class ConversationChatDetail(
    ConversationChatAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ConversationChatStatusAPI():
    queryset = models.ConversationChatStatus.objects.all()
    serializer_class = serializers.ConversationChatStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversationChatStatusList(
    ConversationChatStatusAPI,
    generics.ListCreateAPIView):
    pass

class ConversationChatStatusDetail(
    ConversationChatStatusAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ConversationVoiceAPI():
    queryset = models.ConversationVoice.objects.all()
    serializer_class = serializers.ConversationVoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversationVoiceList(
    ConversationVoiceAPI,
    generics.ListCreateAPIView):
    pass

class ConversationVoiceDetail(
    ConversationVoiceAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ConversationVideoAPI():
    queryset = models.ConversationVideo.objects.all()
    serializer_class = serializers.ConversationVideoSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversationVideoList(
    ConversationVideoAPI,
    generics.ListCreateAPIView):
    pass

class ConversationVideoDetail(
    ConversationVideoAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ConversationVideoStatusAPI():
    queryset = models.ConversationVideoStatus.objects.all()
    serializer_class = serializers.ConversationVideoStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversationVideoStatusList(
    ConversationVideoStatusAPI,
    generics.ListCreateAPIView):
    pass

class ConversationVideoStatusDetail(
    ConversationVideoStatusAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass