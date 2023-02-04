from django.db import models
from django.core import serializers


class AdminSettings(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(AdminSettings, self).save(*args, **kwargs)
        serialized_settings = serializers.serialize('json', [self, ])
        # print(type(serialized_settings), serialized_settings)
        with open('config.txt', 'w') as file:
            file.write(serialized_settings)

    @classmethod
    def load(cls):
        try:
            # return cls.objects.get()

            with open('config.txt', 'r') as file:
                serialized_settings = file.read()
            settings = next(serializers.deserialize('json', serialized_settings)).object
            return settings

        except cls.DoesNotExist:
            return cls()
