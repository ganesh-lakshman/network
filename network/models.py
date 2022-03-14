from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False,
                                       blank=True)

    def count_followers(self):
        return self.followers.count()

    def count_following(self):
        return User.objects.filter(followers=self).count()


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="User")
    post = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True, editable=False)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"post{self.id}"

    def serialize(self):
        return {
            "post_id": self.id,
            "user": self.user,
            "post": self.post,
            "timestamp": self.datetime.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likedpost")

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="likedby")

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} liked {self.post}"

    def serialize(self):
        return {
            "post": self.post,
            "user": self.user
        }

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'], name="unique_like"),
        ]


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="commentor")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, related_name="commentedpost")
    comment = models.TextField()

    def __str__(self):
        return f"{self.user} comented {self.comment} on post {self.post}"

    def serialize(self):
        return {
            "user_id": self.user,
            "post_id": self.post,
            "comment": self.comment
        }
