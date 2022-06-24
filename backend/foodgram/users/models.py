from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscribe(models.Model):
    subscribing_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribitions',
        verbose_name='Подписчик'
    )
    user_to_subscribe = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор'
    )

    class Meta:

        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        constraints = [
            models.UniqueConstraint(
                fields=['subscribing_user', 'user_to_subscribe'],
                name='unique_subscribe'
            )
        ]
