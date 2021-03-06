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
    developer = models.CharField(max_length=50)
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

    def bad_vote(self):
        self.net_votes = self.net_votes - 1
        self.save()
    
    def good_vote(self):
        self.net_votes = self.net_votes + 1
        self.save()


class Comment(models.Model):
    words = models.TextField(blank=True, max_length=140)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Vote(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    value = models.IntegerField(
        choices=VOTE_VALUES
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Photo(models.Model):
    url = models.CharField(max_length=200)
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for app_id: {self.app_id} @{self.url}"