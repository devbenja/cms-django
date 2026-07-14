"""
Custom user model for the CMS.
We extend AbstractUser and add a 'role' field instead of using Django Groups,
because we have only two fixed roles (admin, editor) and Groups is overkill.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    ADMIN = 'admin', 'Administrador'
    EDITOR = 'editor', 'Editor'


class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EDITOR,
        help_text='Administrador tiene control total. Editor puede crear y editar contenido pero no gestiona usuarios.',
    )

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        full = self.get_full_name()
        return full if full else self.username

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_superuser

    @property
    def is_editor(self):
        return self.role == Role.EDITOR
