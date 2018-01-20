from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

# Create your views here.

def index(request):
    """
    View function for home page of site
    """
    #Generate counts of some of the main objects

    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()

    # Available books (ststus = 'a')

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors= Author.objects.count()
    num_genres = Genre.objects.count()

    return render(request, 'index.html', context={'title':'Домашняя страница','num_books':num_books,'num_authors': num_authors, 'num_instances': num_instances,'num_instances_availible':num_instances_available, 'num_genres': num_genres})

