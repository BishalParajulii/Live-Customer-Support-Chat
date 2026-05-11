from django.shortcuts import render , redirect

from .models import ChatSession



def chat_room(request):
    customer_name = request.GET.get('name' , 'Guest')
    
    session = ChatSession.objects.create(customer_name=customer_name)
    
    return redirect('chat_join', session_id=session.id)


def chat_join(request, session_id):
    sender_type = request.GET.get('role', 'customer')
    if sender_type not in ['customer', 'agent']:
        sender_type = 'customer'

    return render(
        request,
        'chat/index.html',
        {
            'session_id': session_id,
            'sender_type': sender_type,
        },
    )
