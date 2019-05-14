from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from sat.views import AjaxableResponseMixin, JsonResponse
from chat.models import ChatGroup, User


class Chat(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat.html'

    def setup(self, request, *args, **kwargs):
        uuid = request.GET.get('uuid', None)
        if uuid is None:
            receiver = request.GET.get('receiver', None)
            receiver = User.objects.get(id=receiver) if User.objects.filter(id=receiver).exists() and receiver else None
            request.chat = ChatGroup.get_or_create_chat(request.user, receiver) if receiver else None
        else:
            chat_qs = ChatGroup.objects.filter(uuid=uuid)
            request.chat = chat_qs.first() if chat_qs.exists() else None
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if self.request.chat is None:
            return JsonResponse("Bad Request", status=400)
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
