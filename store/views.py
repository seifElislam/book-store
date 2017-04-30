from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.db.models import  Avg
from django.conf.urls import include, url


STATUS = ['Read', 'Currently Reading', 'Want to Read']



def index(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    return render(request, 'home.html', {'books': books,'authors': authors})


def goArea(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    user = User.objects.get(id=2);
    return render(request, 'myArea.html',{'books': books,'authors': authors , "user": user})

@login_required
def exit(request):

    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/store/')

def getBook(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id']);

    print(book.bookstate_set.filter(user=user).first().statues)
    return render(request, 'book.html', {'book': book})


def getBookBy(request, key):
    books = Book.objects.filter(title__contains=key)

    return render(request, 'books.html', {'books': books})


def getBooks(request):
    books = Book.objects.all()
    user = User.objects.get(id=2);
    authors = Author.objects.all()

    for i in range(len(books)):

        books[i].s= books[i].bookstate_set.filter(user=user).first()
        books[i].r= books[i].rateuserbook_set.filter(user=user).first()
        books[i].avg =books[i].rateuserbook_set.all().aggregate(Avg('rate'))
        books[i].count =len(books[i].rateuserbook_set.all())

    # return render(request, 'books.html', {'books': books, "user": user ,'authors': authors})
    return render(request, 'home.html', {'books': books, "user": user ,'authors': authors})


def getAuthor(request, author_id):
    author = Author.objects.get(id=author_id)
    hisBooks=Book.objects.filter(author=author)
    hisFollowers=len(author.followers.all())
    print(hisFollowers)
    return render(request, 'author.html', {'author': author,'hisBooks': hisBooks,'hisFollowers':hisFollowers})


def getAuthors(request):
    authors = Author.objects.all()
    user = User.objects.get(id=2);

    return render(request, 'authors.html', {'authors': authors, "user": user})


def followAuthor(request, author_id):
    user = User.objects.get(id=2);
    author = Author.objects.get(id=author_id)
    author.followers.add(user)
    author.save()
    print(author.followers.all())
    return JsonResponse({'follow':"unfollow"})


def unFollowAuthor(request, author_id):
    user = User.objects.get(id=2);
    author = Author.objects.get(id=author_id)
    author.followers.remove(user)
    author.save()
    return JsonResponse({'follow':"follow"})


def wantToRead(request, book_id, state):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=2);

    bookStatus = BookState.objects.filter(user=user,book=book)


    if bookStatus:
        b = bookStatus.first()
        b.statues = state
        b.save()
    else:
        bookStatus = BookState()
        bookStatus.book = book
        bookStatus.user = user
        bookStatus.statues = state
        bookStatus.save()


    return JsonResponse({'statue': STATUS[int(state)]})

def rate(request , book_id ,rate):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=2);
    rateBook = RateUserBook.objects.filter(user=user,book=book)

    if rateBook:
        b = rateBook.first()
        b.rate = rate
        b.save()
    else:
        rateBook = RateUserBook()
        rateBook.book = book
        rateBook.user = user
        rateBook.statues = rate
        rateBook.save()

    return JsonResponse({'rate': rate})




def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            profile.save()
            registered = True
            return HttpResponseRedirect('/store/')
        else:
            print(user_form.errors, profile_form.errors)
            return HttpResponse(user_form.errors, profile_form.errors)
            #     user_form = UserForm()
            #     profile_form = UserProfileForm()
            #
            # return render(request, "register.html",
            #               {'user_form': user_form, 'profile_form': profile_form, 'registered': registered
            #                   , 'user_errors': user_form.errors, 'avatar_error': profile_form.errors})
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, "register.html",
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(username=username, password=password)
        print("user:", user.id)
        if user:
            if user.is_active:
                auth_login(request, user)
                request.session['user_id'] = user.id
                return HttpResponseRedirect('/store/')
            else:
                return HttpResponse('Your account is disabled')
        else:
            print("Invalid login details")
            return render(request, 'login.html', {"error_msg": "Invlaid login details"})
    else:
        return render(request, 'login.html')
