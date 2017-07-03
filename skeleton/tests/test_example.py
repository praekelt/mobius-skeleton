import os

from django.core import management
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test.client import Client, RequestFactory
from django.utils import timezone
from django.db.models.fields import BigIntegerField, BooleanField, CharField, \
    CommaSeparatedIntegerField, DateField, DateTimeField, DecimalField, \
    EmailField, FilePathField, FloatField, IPAddressField, IntegerField, \
    NullBooleanField, PositiveIntegerField, PositiveSmallIntegerField, \
    SlugField, SmallIntegerField, TextField, AutoField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import OneToOneField
from django.conf import settings

from jmbo.models import ModelBase, Image, ModelBaseImage
from post.models import Post


RES_DIR = os.path.join(os.path.dirname(__file__), "res")
IMAGE_PATH = os.path.join(RES_DIR, "image.jpg")


def set_image(obj):
    image = Image.objects.create(title="Title")
    image.image.save(
        os.path.basename(IMAGE_PATH),
        ContentFile(open(IMAGE_PATH, "rb").read())
    )
    mbi = ModelBaseImage.objects.create(modelbase=obj, image=image)


class TestExample(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestExample, cls).setUpClass()

        cls.request = RequestFactory()
        cls.client = Client()

        # Post-syncdb steps
        management.call_command("load_photosizes", interactive=False)

    @classmethod
    def setUpTestData(cls):
        super(TestExample, cls).setUpTestData()

        # Editor
        cls.editor = get_user_model().objects.create(
            username="editor",
            email="editor@test.com"
        )
        cls.editor.set_password("password")
        cls.editor.save()

    def test_common_urls(self):
        """High-level test to confirm common set of URLs render"""
        # todo: restore
        #urls = [
        #    (reverse("auth:login"), 200),
        #    (reverse("auth:logout"), 302),
        #    (reverse("auth:password_reset"), 200),
        #]
        urls = [
            (reverse("mote:home"), 200),
            ("/api/v1/", 200),
        ]
        for url, code in urls:
            print "Checking path %s" % url
            response = self.client.get(url)
            self.assertEqual(response.status_code, code)

    def test_detail_pages(self):
        """Create an instance of each Jmbo content type and render detail
        page"""

        modelbase_fieldnames = [f.name for f in ModelBase._meta.fields]

        for ct in ContentType.objects.all():
            model_class = ct.model_class()

            if (model_class is not None) \
                and issubclass(model_class, ModelBase):

                di = dict(
                    title=model_class.__name__,
                    description="Description",
                    state="published",
                    owner=self.editor,
                )

                # Set not null fields if possible
                skip = False
                for field in model_class._meta.fields:
                    if field.name in modelbase_fieldnames:
                        continue
                    if field.name in di:
                        continue
                    if not field.null:
                        if isinstance(field, (IntegerField, SmallIntegerField,
                            BigIntegerField, PositiveIntegerField,
                            PositiveSmallIntegerField)):
                            di[field.name] = 1
                        elif isinstance(field, (CharField, TextField)):
                            di[field.name] = "a"
                        elif isinstance(field, FloatField):
                            di[field.name] = 1.0
                        elif isinstance(field, DateField):
                            di[field.name] = timezone.now().date()
                        elif isinstance(field, DateTimeField):
                            di[field.name] = timezone.now()
                        elif isinstance(field, (BooleanField, NullBooleanField)):
                            di[field.name] = True
                        elif isinstance(field, (AutoField, ImageField,
                            OneToOneField)):
                            pass
                        else:
                            skip = True
                            break

                # Skip if issues expected
                if skip:
                    continue

                # Save. Continue on error. We did our best.
                try:
                    obj = model_class.objects.create(**di)
                except TypeError:
                    continue
                obj.sites = [1]
                set_image(obj)
                obj.save()

                # Test
                print "Checking %s detail page %s" \
                    % (model_class.__name__, obj.get_absolute_url())
                response = self.client.get(obj.get_absolute_url())
                self.assertEqual(response.status_code, 200)

