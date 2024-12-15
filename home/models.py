from django.db import models
from django.db.models.signals import (
    pre_save, pre_migrate,pre_delete,pre_init,
    post_save,post_migrate,post_delete,post_init
    )
from django.dispatch import receiver

""" 
Pre-init (pre_init): Before a model instance is initialized.
Post-init (post_init): After a model instance is initialized.
Pre-save (pre_save): Before saving an instance.
Post-save (post_save): After saving an instance.
Pre-delete (pre_delete): Before deleting an instance.
Post-delete (post_delete): After deleting an instance.
Pre-migrate (pre_migrate): Before migrations are applied.
Post-migrate (post_migrate): After migrations are applied.

"""

class Student(models.Model):
    student_name = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=50,
        choices=(
            ("Male", "Male"),
            ("Female", "Female"),
        )
    )
    student_id = models.CharField(max_length=15, null=True, blank=True)

# @receiver(post_save,sender=Student)  
# def save_student(sender, instance , created, **kwargs):
#     if created:
#         instance.student_id = f"STU-000{instance.id}"
#         instance.save()

#======  another way ============


@receiver(pre_save, sender=Student)
@receiver(post_save, sender=Student)
@receiver(pre_delete, sender=Student)
@receiver(post_delete, sender=Student)
@receiver(pre_init, sender=Student)
@receiver(post_init, sender=Student)
@receiver(pre_migrate)
@receiver(post_migrate)
def save_student(sender, instance=None, created=False, **kwargs):
    signal = kwargs.get('signal')

    if signal == pre_init:
        print("Running pre_init logic...")
        print("A Student object is being initialized.")
        print("Pre-init logic finished.")

    elif signal == post_init:
        print("Running post_init logic...")
        print(f"A Student object has been initialized - {instance}.")
        print("Post-init logic finished.")

    elif signal == pre_save:
        print("Running pre_save logic...")
        if not instance.student_name:
            raise ValueError("Student name cannot be empty.")
        print("Pre-save logic finished.")

    elif signal == post_save:
        print("Running post_save logic...")
        if created and not instance.student_id:
            instance.student_id = f"STU-000{instance.id}"
            instance.save()
            print(f"Generated student_id: {instance.student_id}")
        print("Post-save logic finished.")

    elif signal == pre_delete:
        print("Running pre_delete logic...")
        print(f"Preparing to delete Student object - {instance}.")
        print("Pre-delete logic finished.")

    elif signal == post_delete:
        print("Running post_delete logic...")
        print(f"Student object deleted - {instance}.")
        print("Post-delete logic finished.")

    elif signal == pre_migrate:
        print("Running pre_migrate logic...")
        app_config = kwargs.get('app_config')
        verbosity = kwargs.get('verbosity')
        print(f"App: {app_config.name}, Verbosity: {verbosity}")
        print("Pre-migrate logic finished.")

    elif signal == post_migrate:
        print("Running post_migrate logic...")
        app_config = kwargs.get('app_config')
        verbosity = kwargs.get('verbosity')
        print(f"App: {app_config.name}, Verbosity: {verbosity}")
        print("Post-migrate logic finished.")

    else:
        print("Unrecognized signal.")

 
""" 
while creating
    Running pre_init logic... A Student object is being initialized.
    Pre-init logic finished.
    Running post_init logic... A Student object has been initialized - <Student Object>.
    Post-init logic finished.
    Running pre_save logic... 
    Pre-save logic finished.
    Running post_save logic... Generated student_id: STU-0001
    Post-save logic finished.

while updating
    Running pre_save logic...
    Pre-save logic finished.
    Running post_save logic...
    Post-save logic finished.

while deleting
    Running pre_delete logic... Preparing to delete Student object - <Student Object>.
    Pre-delete logic finished.
    Running post_delete logic... Student object deleted - <Student Object>.
    Post-delete logic finished.

while migrating db python3 manage.py migrate
    Running pre_migrate logic... App: home, Verbosity: 1.
    Pre-migrate logic finished.
    Running post_migrate logic... App: home, Verbosity: 1.
    Post-migrate logic finished.

while fetching each data init will work each time. how many data that much it work


"""

from PIL import Image
import os
from django.conf import settings



class ImageModel(models.Model):
    original_image = models.ImageField(upload_to="images/")
    thumbnail_small = models.ImageField(upload_to="thumbnails/", null=True, blank=True)
    thumbnail_medium = models.ImageField(upload_to="thumbnails/", null=True, blank=True)
    thumbnail_large = models.ImageField(upload_to="thumbnails/", null=True, blank=True)

@receiver(post_save, sender=ImageModel)
def create_thumbnails(sender, instance, created, **kwargs):
    if created:
        sizes = {
            "thumbnail_small": (100, 100),
            "thumbnail_medium": (300, 300),
            "thumbnail_large": (600, 600),
        }
        
        for field, size in sizes.items():
            img = Image.open(instance.original_image.path)
            img.thumbnail(size, Image.Resampling.LANCZOS)
            base_name, ext = os.path.splitext(os.path.basename(instance.original_image.name))
            thumb_filename = f"{base_name}_{size[0]}x{size[1]}{ext}"
            thumb_dir = os.path.join(settings.MEDIA_ROOT, "thumbnails")
            thumb_path = os.path.join(thumb_dir, thumb_filename)
            os.makedirs(thumb_dir, exist_ok=True)
            img.save(thumb_path)
            setattr(instance, field, f"thumbnails/{thumb_filename}")
        instance.save()
            
