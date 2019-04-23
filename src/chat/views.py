from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from sat.views import AjaxableResponseMixin
from chat.models import ChatGroup


class Chat(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat.html'

    def setup(self, request, *args, **kwargs):
        uuid = request.GET['uuid']
        chat_qs = ChatGroup.objects.filter(uuid=uuid)
        request.chat = chat_qs.first() if chat_qs.exists() else ChatGroup.create_chat(request.user, request.receiver)
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        chat_messages = self.request.chat.messages
        return super().get_context_data(**kwargs, **{'chat_messages': chat_messages})


Chat.view = Chat.as_view()


class ChatList(LoginRequiredMixin, AjaxableResponseMixin, TemplateView):
    template_name = 'chat/chat_list.html'

    def get_context_data(self, **kwargs):
        chat_list = ChatGroup.get_chats_by_user(self.request.user)
        return super().get_context_data(**kwargs, **{'chat_list': chat_list})

    def get_chat(self, request, *args, **kwargs):
        return Chat.view(request, *args, **kwargs)


ChatList.view = ChatList.as_view()
