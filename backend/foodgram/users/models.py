from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Subscribe(models.Model):
    subscribing_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribitions'
    )
    user_to_subscribe = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscribing_user', 'user_to_subscribe'],
                name='unique_subscribe'
            )
        ]
