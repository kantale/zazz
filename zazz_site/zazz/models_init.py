from django.db import models

# Create your models here.


class Samples(models.Model):

    class Meta:
            indexes = [
                models.Index(
                    fields=['Chromosome', 'Position', 'Reference', 'Alternative'],
                    name='sample_idx',
                ),
            ]

    Chromosome = models.CharField(max_length = 5)
    Position = models.IntegerField()
    Reference = models.CharField(max_length = 255)
    Alternative = models.CharField(max_length = 255)


