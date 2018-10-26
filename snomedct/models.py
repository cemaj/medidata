from django.db import models
from postgres_copy import CopyManager
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class SnomedConcept(models.Model):
    external_id = models.BigIntegerField(unique=True, primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    file_path = models.CharField(max_length=255)
    fsn_description = models.CharField(max_length=255)
    children = models.ManyToManyField('SnomedConcept', through='SnomedDescendant')
    external_fsn_description_id = models.BigIntegerField()
    objects = CopyManager()

    def __str__(self):
        return "{} - {}".format(self.external_id, self.fsn_description)

    class Meta:
        indexes = [
            models.Index(fields=['fsn_description']),
            models.Index(fields=['external_id']),
        ]

    def _get_children(self):
        return SnomedConcept.objects.filter(children__external_id=self.pk)

    def get_all_children(self, include_self=True):
        # recursive function
        all_children = []
        if include_self:
            all_children.append(self)
        for child in self._get_children():
            _all_children = child.get_all_children(include_self=True)
            if 0 < len(_all_children):
                all_children.extend(_all_children)
        return all_children

    def snomed_descendants(self):
        return SnomedConcept.objects.filter(external_ids=self.external_id)

    def snomed_descendant_readcodes(self):
        return ReadCode.objects.filter(concept_id__external_ids=self.external_id)

    def readcodes(self):
        return ReadCode.objects.filter(concept_id=self.external_id)

    def combined_readcodes(self):
        """
        Return readcodes of this snomed concept and its descendants.
        """
        return self.readcodes().union(self.snomed_descendant_readcodes())


class ReadCode(models.Model):
    ext_read_code = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    file_path = models.CharField(max_length=255)
    concept_id = models.ForeignKey(SnomedConcept, to_field='external_id', on_delete=models.CASCADE, db_column="concept_id", null=True)
    objects = CopyManager()

    def __str__(self):
        return "{} - {} - {}".format(self.id, self.concept_id.fsn_description, self.ext_read_code)

    class Meta:
        indexes = [
            models.Index(fields=['concept_id']),
        ]


class SnomedDescendant(models.Model):
    descendant_external_id = models.ForeignKey(SnomedConcept, to_field='external_id', on_delete=models.CASCADE,
                                               db_column="descendant_external_id", null=True, related_name='descendant_external_id')
    external_id = models.ForeignKey(SnomedConcept, to_field='external_id', on_delete=models.CASCADE,
                                    db_column="external_id", null=True, related_name='external_ids')
    objects = CopyManager()

    def __str__(self):
        return "{} - {} - {}".format(self.id, self.descendant_external_id.fsn_description, self.external_id)

    class Meta:
        indexes = [
            models.Index(fields=['external_id']),
        ]


class CommonSnomedConcepts(models.Model):
    common_name = models.CharField(max_length=255)
    snomed_concept_code = models.ManyToManyField(SnomedConcept)

    def __str__(self):
        return self.common_name