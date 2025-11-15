from django.db import models, transaction
from django.urls import reverse


class Name(models.Model):
  initials = models.CharField(max_length=255, unique=True)

  def __str__(self):
    return self.initials

  def get_absolute_url(self):
    return reverse('name_detail', kwargs={'pk': self.pk})


class Repository(models.Model):
  name = models.CharField(max_length=255, unique=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('repository_detail', kwargs={'pk': self.pk})


class User(models.Model):
  cas_directory_id = models.CharField(max_length=255)
  name = models.CharField(max_length=255)


class AutoNumber(models.Model):
  entry_date = models.DateField(null=True, blank=True)
  name = models.ForeignKey(Name, on_delete=models.PROTECT, related_name='auto_numbers')
  repository = models.ForeignKey(Repository, on_delete=models.PROTECT, related_name='auto_numbers')

  def save(self, *args, **kwargs):
    if self.name:
      self.name.save()

    if self.repository:
      self.repository.save()

    super().save(*args, **kwargs)

  def get_absolute_url(self):
    return reverse('autonumber_detail', kwargs={'pk': self.pk})

  @classmethod
  def create_batch(cls, quantity, parameters):
    first = last = None
    count = 0

    # DB transaction for safety
    with transaction.atomic():
      for _ in range(quantity):
        auto_number = cls.objects.create(**parameters)

        if first is None:
          first = auto_number.id

        last = auto_number.id
        count += 1

    return {'first': first, 'last': last, 'count': count}
