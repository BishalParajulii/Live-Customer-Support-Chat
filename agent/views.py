from django.shortcuts import render

# Create your views here.
def agent_join(request, session_id):
    return render(request, 'agent/agent.html', {
                  'session_id': session_id,
                  'sender_type': 'agent',
                  })