from django.db import models
import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField('Название',max_length=200, help_text="Введите жанр книги (напр. Фантастика, Детектив, Роман)")
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField('Описание',max_length=1000, help_text="Введите описание книги")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 символов <a href="https://www.isbn-international.org/content/what-isbn">ISBN номер</a>')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр для книги")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolut_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Жанр'
    author.short_description = 'Автор'

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Угикальный номер для издания")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'В печати'),
        ('o', 'Отсутствует'),
        ('a', 'Доступна'),
        ('r', 'Зарезервированно'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text="Доступность книг")

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)

class Author(models.Model):
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия',max_length=100)
    date_of_birth = models.DateField('Родился',null=True, blank=True)
    date_of_death = models.DateField('Умер', blank=True, null=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):

        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):

        return '{0}, {1}'.format(self.last_name, self.first_name)

class Language(models.Model):
    name = models.CharField('Язык',max_length=200, help_text="Введите язык на котором написанна книга")
    
    def __str__(self):
        return self.name