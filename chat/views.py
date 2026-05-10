from django.shortcuts import render

from .models import ChatSession



def chat_room(request):
    customer_name = request.GET.get('name' , 'Guest')
    
    session = ChatSession.objects.create(customer_name=customer_name)
    
    return render(request, 'chat/index.html', {'session_id': session.id})
