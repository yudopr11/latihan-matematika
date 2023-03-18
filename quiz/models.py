from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField


def validate_year(value):
    try:
        int(value)
        return value
    except:
        raise ValidationError("Masukkan tahun dengan angka.")
    
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

SOURCE_CHOICES = (
    ('snbt','SNBT'),
    ('utbk', 'UTBK')
)

TYPE_CHOICES = (
    ('pilihan-ganda','Pilihan Ganda'),
    ('tabel-benar-salah', 'Tabel Benar Salah')
)

EXPLANATION_TYPE_CHOICES = (
    ('text','Teks'),
    ('youtube', 'Youtube')
)

SUBJECT_CHOICES = (
    ('penalaran-matematika','Penalaran Matematika'),
    ('pengetahuan-kuantitatif', 'Pengetahuan Kuantitatif')
)

class BankSoal(models.Model):
    question = RichTextField()
    choices = models.TextField()
    answer = models.TextField()
    explanation = RichTextField(default=None, blank=True, null=True)
    explanation_type = models.CharField(max_length = 20, default=None, blank=True, null=True, choices=EXPLANATION_TYPE_CHOICES)
    type = models.CharField(max_length = 20, choices=TYPE_CHOICES, default='pilihan-ganda')
    subject = models.CharField(max_length = 100, choices=SUBJECT_CHOICES, default=None, blank=True, null=True, db_index=True)
    source = models.CharField(max_length = 10, choices=SOURCE_CHOICES, default='snbt', db_index=True)
    year = models.CharField(max_length = 4, validators =[validate_year], db_index=True)
    status = models.IntegerField(choices=STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        if self.question[:100].endswith("."):
            snippet = self.question
        else:
            snippet = self.question[:100]+"..."
        return f"{self.pk}: {snippet}"