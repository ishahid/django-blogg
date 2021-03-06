from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Tag(models.Model):
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('blogg.views.tag', args=[self.slug])


class CustomQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    teaser = models.TextField()
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='posts')
    author = models.ForeignKey(User, related_name='posts')
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True, auto_now=True)
    views = models.IntegerField(default=0, editable=False)

    class Meta:
        ordering = ['-created']

    objects = CustomQuerySet.as_manager()

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('blogg.views.post', args=[self.slug])

    def increment_views(self):
        self.views += 1
        self.save()


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    content = models.TextField(max_length=1000L)
    author = models.CharField(max_length=100, default="Anonymous", null=False, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500L, null=False, blank=True)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        ordering = ['-created']

    objects = CustomQuerySet.as_manager()

    def __unicode__(self):
        return u'%s' % self.pk
