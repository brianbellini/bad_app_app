from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

VOTE_VALUES = {
    (1, 'GOOD'),
    ((-1), 'BAD')
}

TAGS = (
    ('As', 'Astronauts'),
    ('Bo', 'Books'),
    ('Bu', 'Business'),
    ('Cr', 'Crime'),
    ('Dr', 'Drugs'),
    ('Ed', 'Education'),
    ('En', 'Entertainment'),
    ('Fi', 'Finance'),
    ('Fo', 'Food & Drink'),
    ('He', 'Health & Fitness'),
    ('Je', 'Jesus'),
    ('Ki', 'Kids'),
    ('Li', 'Lifestyle'),
    ('Ma', 'Magazines & Newspapers'),
    ('Me', 'Medical'),
    ('Mu', 'Music'),
    ('Na', 'Navigation'),
    ('Ne', 'News'),
    ('Ns', 'NSFW'),
    ('Ph', 'Photo & Video'),
    ('Pr', 'Productivity'),
    ('Re', 'Reference'),
    ('Sh', 'Shopping'),
    ('So', 'Social Networking'),
    ('Sp', 'Sports'),
    ('Tr', 'Travel'),
    ('Ut', 'Utilities'),
    ('We', 'Weather'),
    ('Ot', 'Other'),
)

# Create your models here.

class App(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True)
    slogan = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    tag = models.CharField(
        max_length=2,
        choices=TAGS,
        default=TAGS[-1][0]
        )
    net_votes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'app_id': self.id})
    
    # def get_net_votes(self):
    #     all_votes = Vote.objects.filter(app=self.id)
    #     net = 0
    #     for vote in all_votes:
    #         net += vote.value

class Comment(models.Model):
    words = models.TextField(blank=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Vote(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    value = models.IntegerField(
        choices=VOTE_VALUES
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)