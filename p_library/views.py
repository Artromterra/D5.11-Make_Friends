from p_library.forms import AuthorForm, BookForm, FriendForm, BookFormForFriend
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from p_library.models import Author, Book, Publisher, Friend
from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from django.forms import formset_factory  
from django.http.response import HttpResponseRedirect

def author_create_many(request):
	AuthorFormSet = formset_factory(AuthorForm, extra=1)
	if request.method == 'POST':
		author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
		if author_formset.is_valid():
			for author_form in author_formset:
				author_form.save()
			return HttpResponseRedirect(reverse_lazy('p_library:author_list'))
	else:
		author_formset = AuthorFormSet(prefix='authors')
	return render(request, 'manage_authors.html', {'author_formset': author_formset})

def books_authors_create_many(request):  
	AuthorFormSet = formset_factory(AuthorForm, extra=2)  
	BookFormSet = formset_factory(BookForm, extra=2)  
	if request.method == 'POST':  
		author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')  
		book_formset = BookFormSet(request.POST, request.FILES, prefix='books')  
		if author_formset.is_valid() and book_formset.is_valid():  
			for author_form in author_formset:  
				author_form.save()  
			for book_form in book_formset:  
				book_form.save()  
			return HttpResponseRedirect(reverse_lazy('p_library:author_list'))  
	else:  
		author_formset = AuthorFormSet(prefix='authors')  
		book_formset = BookFormSet(prefix='books')  
	return render(
		request,  
		'manage_books_authors.html',  
		{  
			'author_formset': author_formset,  
			'book_formset': book_formset,  
		}  
	)

def books_friends_create(request):
	FriendFormSet = formset_factory(FriendForm, extra=1)
	BookFormSet = formset_factory(BookFormForFriend, extra=1)
	if request.method == 'POST':
		friend_formset = FriendFormSet(request.POST, request.FILES, prefix='friends')
		book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
		if friend_formset.is_valid() and book_formset.is_valid():
			for friend_form in friend_formset:  
				friend_form.save()  
			for book_form in book_formset:  
				book_form.save()  
			return HttpResponseRedirect(reverse_lazy('p_library:friend_form'))
	else:
		friend_formset = FriendFormSet(prefix='friends')  
		book_formset = BookFormSet(prefix='books')
	return render(
		request, 'manage_books_friends.html',  
		{  
			'friend_formset': friend_formset,  
			'book_formset': book_formset,  
		}  
	)		
	


class AuthorEdit(CreateView):  
	model = Author  
	form_class = AuthorForm  
	success_url = reverse_lazy('p_library:author_list')  
	template_name = 'author_edit.html'

class AuthorList(ListView):  
	model = Author  
	template_name = 'author_list.html'

class FriendFormEdit(CreateView):
	model = Friend
	form_class = FriendForm
	success_url = reverse_lazy('p_library:friend_form')
	template_name = 'friend_form_edit.html'

class FriendList(ListView):
	model = Friend
	template_name = 'friend_form.html'

def index(request):
	template = loader.get_template('index.html')
	books = Book.objects.all()
	# range_ = [x for x in range(1,100)]
	biblio_data = {"title": "мою библиотеку",
				 "books": books,
				#  "range_": range_,
				 }
	return HttpResponse(template.render(biblio_data, request))

def book_increment(request):
	if request.method == 'POST':
		book_id = request.POST['id']
		if not book_id:
			return redirect('/index/')
		else:
			book = Book.objects.filter(id=book_id).first()
			if not book:
				return redirect('/index/')
			book.copy_count += 1
			book.save()
		return redirect('/index/')
	else:
		return redirect('/index/')

def book_decrement(request):
	if request.method == 'POST':
		book_id = request.POST['id']
		if not book_id:
			return redirect('/index/')
		else:
			book = Book.objects.filter(id=book_id).first()
			if not book:
				return redirect('/index/')
			if book.copy_count < 1:
				book.copy_count = 0
			else:
				book.copy_count -= 1
			book.save()
		return redirect('/index/')
	else:
		return redirect('/index/')

def publisher_new(request):
	template = loader.get_template('publisher_new.html')
	publishers = Publisher.objects.all()
	# publishers_data = {"data": {publisher.name: 
	# 					list(Book.objects.filter(publisher=publisher.id).values_list("title", flat=True))
	# 					 for publisher in publishers}}
	data = {"publishers": publishers,}
	return HttpResponse(template.render(data, request))

def friend_list(request):
	template = loader.get_template('friend_list.html')
	friends = Friend.objects.all()
	data = {"friends": friends,}
	return HttpResponse(template.render(data, request))

# Create your views here.
