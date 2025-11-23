from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm, BookSearchForm


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book created successfully.")
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully.")
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, "Book deleted successfully.")
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def search_books(request):
    query = ''
    results = []
    if request.method == 'GET':
        form = BookSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Book.objects.filter(title__icontains=query)
    else:
        form = BookSearchForm()

    return render(request, 'bookshelf/book_list.html', {
        'form': form,
        'books': results,  # renamed from 'results' for template consistency
        'query': query,
    })