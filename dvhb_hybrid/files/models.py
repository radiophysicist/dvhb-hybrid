import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..models import UpdatedMixin
from .storages import image_storage


class Image(UpdatedMixin, models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='images',
        verbose_name=_('Автор'))
    uuid = models.UUIDField(_('UUID'), primary_key=True)
    image = models.ImageField(storage=image_storage)
    mime_type = models.CharField(_('тип содежимого'), max_length=99)
    meta = JSONField(_('мета-информация'), default={})

    class Meta:
        verbose_name = _('изображение')
        verbose_name_plural = _('Изображения')
        ordering = ('-created_at',)

    def __str__(self):
        return self.image.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.uuid:
            uid = uuid.uuid4()
            self.uuid = uid
            self.image.name = image_storage.get_available_name(
                self.image.name, uuid=uid)

        super(Image, self).save(force_insert=force_insert,
                                force_update=force_update,
                                using=using,
                                update_fields=update_fields)