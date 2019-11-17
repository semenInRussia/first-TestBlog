from django.shortcuts import redirect
from django.shortcuts import reverse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import MyArticles
from .models import Tag
from .models import Coments
from django.contrib.auth.models import User

from django.template.loader import render_to_string

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout

from .forms import ArticleForm
from .forms import TagForm
from .forms import UserForm
from .forms import LoginUserForm

from datetime import datetime
from pprint import pprint
from django.utils.text import slugify
from time import time

from django.views import View

from django.db.models import Q

from django.http import HttpResponse
from django.core.exceptions import PermissionDenied


# Create your views here.
class createcomment(View):
    def get(self, request, slug):
        pass
    def post(self, request, slug):
        article = MyArticles.objects.get(
            slug=slug,
        )
        if request.POST.get('commentbody'):
            Coments.objects.create(
                article=article,
                author=request.user,
                text=request.POST.get('commentbody')
            )
        return redirect(reverse('main:detail', kwargs={'slug':slug}))       
def get_slug(w):
    if not isinstance(w, str):
        return None
    alfa = {
        'а':'a', "б":'b', 'в':'v', "г":'g', "д":'d',
        "е":'e', "ё":'yo', "ж":'j', "з":'z', "и":'i',
        "к":'k', "л":'l', "м":'m', "н":'n', "о":'o', "п":'p',
        "р":'r', "с":'s', "т":'t', "ф":'f', "х":'h', "ц":'c',
        "ч":"ch", "ш":'sh', "щ":'sh', "ы":'i', "э":'e',
        "ю":'yu', "я":'ya'
    }
    res = ''
    for i in w.lower():
        if i in alfa:
            res += alfa[i]
        else:
            res += i
    return slugify(res)
def index(request):
    return render(request, 'main/index.html')

def contacts(request):
    return render(request, 'main/contacts.html')

def articles(request):
    listarticles = MyArticles.objects.all()
    return render(request, 'articles/index.html', context={
        'articles':listarticles,
        'is_list':True,
    })
def detail(request, slug):
    print(slug)
    ob = MyArticles.objects.get(slug=slug)
    return render(request, 'articles/detail.html',context={
        'article':ob,
        'coments': Coments.objects.filter(article=ob),
        'model': ob,
        "usl":ob.author.pk==request.user.pk,
        'is_articles':True,
    })

def post_create(request):
    d = {
            'tag':request.POST.get('tag'),
            'name':request.POST.get('name'),
            'text':request.POST.get('text'),
            'author': request.user,
            'date': datetime.today (),
            'slug':get_slug(request.POST.get('name')),
            'color': request.POST.get('color'),
    }


    boundform = ArticleForm(d)
    if boundform.is_valid():
        new_post = boundform.cleaned_data
        nd = {
            'text':new_post['text'],
            'tag':new_post['tag'],
            'name':new_post['name'],
            'slug':get_slug(new_post['name']),
            'author':request.user,
            'color': new_post['color'],
        }
        ma = MyArticles(**nd)
        ma.save()
        return redirect(reverse('main:detail', kwargs={'slug':nd['slug']}))
    if request.POST:
        return render(request, 'articles/createpage.html', context={
            'form': ArticleForm(d)
        })
    return render(request, 'articles/createpage.html', context={
            'form': ArticleForm()
        })

class update(View):
    def get(self, request, slug):
        obj = MyArticles.objects.get(slug=slug)
        condition2 = not request.user.is_staff
        condition = not obj.author.pk==request.user.pk
        print(condition) 
        print(condition2) 
        if  condition2 and condition:
            raise PermissionDenied
        
        
        
        form = ArticleForm(instance=obj)
        return render(request, 'articles/update.html', context={
            'form':form,
            'model':obj,
        })
    def post(self, request, slug):
        obj = MyArticles.objects.get(slug=slug)
        condition2 = not request.user.is_staff
        condition = not obj.author.pk==request.user.pk
        if  condition2 and  condition:
            raise PermissionDenied
        d = {'slug':get_slug(request.POST.get('name')),
            'name':request.POST.get('name'),
            'tag':request.POST.get('tag'),
            'color': request.POST.get('color'),
            'text':request.POST.get('text'),
            'author':obj.author,
            'data': datetime.today(),}
        bform = ArticleForm(d, instance=obj)
        if bform.is_valid():
            nd = {
                'slug':get_slug(bform.cleaned_data['name']),
                'name':bform.cleaned_data['name'],
                'tag':bform.cleaned_data['tag'],
                'text':bform.cleaned_data['text'],
                'author':obj.author,
                'data': obj.data,
            }
            new_post = bform.save()
            return redirect(reverse("main:detail",kwargs={
		'slug':new_post.slug
	    }))
        return render(request, 'articles/update.html', context={
            'form': bform,
            'model': obj,
        })
    

def delete(request, slug):
    ob = MyArticles.objects.get(slug=slug)
    condition = not ob.author.pk==request.user.pk
    condition2 = not request.user.is_staff
    if condition2 and condition:
        raise PermissionDenied
    ob.delete()
    return redirect(reverse('main:articles'))
def tag_index(request):
    list_tags = Tag.objects.all()
    return render(request, 'teg/index.html', context={
        'list': sorted(list_tags.__iter__(), key=(lambda a: 100000-len(MyArticles.objects.filter(tag=a)))),
        'is_list_tag': True,
    })
def tag_detail(request, slug):
    print(slug)
    obj = Tag.objects.get(slug=slug)
    list_articles = MyArticles.objects.filter(tag=obj)
    return render(request, 'teg/detail.html', context={
        'tag': obj,
        'model':obj,
        'num_use': len(list_articles),
        "usl":request.user.pk==obj.author.pk,
    })
class tag_create(View):
    def get(self, request):
        form = TagForm()
        return render(request, 'teg/createpage.html', context={
            'form': form,
        })
    def post(self, request):
        data_form_tag = {
            'name': request.POST.get('name', '').title(),
            'slug': get_slug(request.POST.get('name')),
            'author': request.user,
        }
        bform = TagForm(data_form_tag)
        if bform.is_valid():
            Tag(**data_form_tag).save()
            return redirect(reverse('main:tag_detail', kwargs={
                'slug': get_slug(request.POST['name'])
            }))
        return render(request, 'teg/createpage.html', context={
            'form': bform,
        })
class tag_update(View):
    def get(self, request, slug):
        obj = Tag.objects.get(slug=slug)
        condition = obj.author.pk==request.user.pk
        if not request.user.is_staff or not condition:
            raise PermissionDenied
        form = TagForm(instance=obj)
        return render(request, 'teg/update.html', context={
            'form':form,
            'model':obj,
        })
    def post(self, request, slug):
        obj = Tag.objects.get(slug=slug)
        condition = obj.author.pk==request.user.pk
        if not request.user.is_staff or not condition:
            raise PermissionDenied
        d = {
            'slug':get_slug(request.POST.get('name')),
            'name':request.POST.get('name'),
            }
        bform = TagForm(d, instance=obj)
        if bform.is_valid():
            nd = {
                'slug':get_slug(bform.cleaned_data['name']),
                'name':bform.cleaned_data['name'],
            }
            new_post = bform.save()
            return redirect(reverse('main:tag_detail',kwargs={'slug':new_post.slug}))
        return render(request, 'teg/update.html', context={
            'form': bform,
            'model': obj,
        })
def tag_delete(request, slug):
    obj = Tag.objects.get(slug=slug)
    condition = obj.author.pk==request.user.pk
    if not request.user.is_staff or condition:
        raise PermissionDenied
    obj.delete()
    return redirect(reverse('main:tags'))

class registruser(View):
    def get(self, request):
        form = UserForm()
        return render(
            request, 'user/registr.html',context={
                'form': form,
            }
        )
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(request.POST.get("username"),
                    request.POST.get("email"),
                    request.POST.get("password"))
            print(dir(new_user))
            login(request, new_user)
        return render(
            request, 'user/registr.html',context={
                'form': form,
            }
        )

class userlogin(View):
    def get(self, request):
        form = LoginUserForm()
        return render(request, 'user/login.html',context={
            'form': form,
        })
    def post(self, request):
        form = LoginUserForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            login(request, user)
            return redirect(reverse(
                'main:kabinet', kwargs={
                    'username': username
                }
            ))

        return render(request, 'user/login.html', context={
                'form': form,
            })
def kabinet(request, username):
    user = User.objects.get(username=username)
    list_ = zip(
        MyArticles.objects.filter(author=user).__iter__(),
        Tag.objects.filter(author=user).__iter__(),
    )
    return render(request, 'user/kabinet.html', context={
        'user': user,
        'list_tag': Tag.objects.filter(author=user),
        'list_myarticles': MyArticles.objects.filter(author=user),
    })
def lagaut(request, username):
    obj = User.objects.get(username=username)
    logout(request)
    return redirect(reverse('main:index'))
def searchtag(request):
    text_user = request.GET.get('text')
    list_tags = Tag.objects.filter(name__icontains=text_user.title())
    str_template = ''''''
    for tag in list_tags:
        str_template += f"""
            <div class="alert alert-light">
              <a href='{reverse('main:detail',kwargs={'slug':tag.slug})}' class="alert-link">{tag.name}</a>
            </div>
        """
    return HttpResponse(str_template)

def articleget(request):
    text_user = request.GET.get('text')
    list_articles = MyArticles.objects.filter(
        Q(name__icontains=text_user.lower())|Q(text__icontains=text_user.lower()))
    str_template = ''''''
    for article in list_articles:
        str_template += f"""
        <div class="alert alert-{article.color}" role="alert">
                <h4>
                    <a href='{reverse('main:detail', kwargs={'slug': article.slug})}' class="alert-link">
                        {article.name}
                    </a>
                </h4>
                    Автор: {article.author.username}
                <p>{article.tag}</p>
        </div>
        """
    return HttpResponse(str_template)
    
