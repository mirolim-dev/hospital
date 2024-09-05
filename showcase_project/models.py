from typing import Iterable
from django.db import models
from  django.core.exceptions import ValidationError

from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

from .validations import validate_image

# Create your models here.
class AboutProject(models.Model):
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="project/about")
    title = models.CharField(max_length=250)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:20]

    def clean(self) -> None:
        validate_image(self.image)
        return super().clean()
    
    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        if AboutProject.objects.filter(is_active=True).exists():
            raise ValidationError("Change all is_active status True objects to False before creating new one.")
        return super().save(force_insert, force_update, using, update_fields)
    

class Feature(models.Model):
    class Meta:
        verbose_name = "Feature"
        verbose_name_plural = "Features"
    
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="project/showcases/features", null=True, blank=True)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name[:20]
    
    def get_all_sub_features(self):
        return self.subfeature_set.select_related("feature")

    def clean(self) -> None:
        validate_image(self.image)
        return super().clean()


class SubFeature(models.Model):
    name = models.CharField(max_length=150)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="project/showcases/subfeatures", null=True, blank=True)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name[:20]
    
    def clean(self) -> None:
        validate_image(self.image)
        return super().clean()


