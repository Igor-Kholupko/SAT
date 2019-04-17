from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from chat.models import Message


class Chat(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat.html'

    def setup(self, request, *args, **kwargs):
        request.receiver = request.GET['receiver']
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        chat_history = Message.get_chat_history(self.request.user, self.request.receiver)
        return super().get_context_data(**kwargs, **{'chat_history': chat_history})


class ChatsList(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chats_list.html'

    def get_context_data(self, **kwargs):
        chats_list = Message.get_chats(self.request.user)
        unread_list = Message.get_unread_chats(self.request.user)
        return super().get_context_data(**kwargs, **{'chats_list': chats_list, 'unread_list': unread_list})
