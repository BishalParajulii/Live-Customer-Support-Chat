from django.http import JsonResponse
from django.shortcuts import render , redirect

from .models import ChatSession , Rating
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json



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


@csrf_exempt
@require_POST
def submit_rating(request, session_id):
    data = json.loads(request.body)
    score = data.get('score')
    feedback = data.get('feedback', '')
    
    if not score or not (1 <= score <= 5):
        return JsonResponse({'error': 'Invalid rating score'}, status=400)
    
    session = ChatSession.objects.get(id=session_id)
    Rating.objects.create(session=session, score=score, feedback=feedback)
    
    return JsonResponse({'success': True})
