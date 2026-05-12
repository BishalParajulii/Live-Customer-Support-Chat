from django.db import models


class ChatSession(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('waiting', 'Waiting'),
        ('closed', 'Closed'),
    ]
    
    customer_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.customer_name} - {self.status}"
    
    
class ChatMessage(models.Model):
    SENDER_CHOICES = [
        ('customer', 'Customer'),
        ('agent', 'Agent'),
    ]
    
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender} - {self.content[:20]}..."
    

class Rating(models.Model):
    session = models.OneToOneField(ChatSession, on_delete=models.CASCADE)
    score = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"session {self.session.id} - rating {self.score}"