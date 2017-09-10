from django.shortcuts import render
from .models import *
from .forms import ALPHABET, ProfileFilterForm

from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

class ProfileInfo(View):
    def get(self,request,pk):
        current_profile = Profile.objects.get(pk=pk)
        return render(request, 'profile_info.html', {'profile':current_profile})

class ProfilesFilter(View):
    def get(self,request):
        selector_list = {}
        count = 1
        template_name='profiles_filter.html'

        for i in ALPHABET:
            selector_list.update({count:{i[1]:i[0]}})
            count+=1
            # Приходится упорядочивать по цифрам, иначе в шаблоне буквенные группы идут
            # вперемешку (З-К, А-Е, Р-У, Ё-И и т.д.). Другого решения проблемы, с которым 
            # можно сохранить порядок и перенести оба значения,
            # я не придумал. Буду рад, если поправите.
        profiles_list = Profile.objects.all()
        profiles_list = get_queryset(request, profiles_list)

        form = ProfileFilterForm
        return render(request, template_name, {'profiles_list':profiles_list, 'selector_list':selector_list,'form':form})

    def post(self,request):
        selector_list = {}
        count = 1
        template_name='profiles_filter.html'

        for i in ALPHABET:
            selector_list.update({count:{i[1]:i[0]}})
            count+=1
        post_data = request.POST

        allowed_filter = ''

        for i in post_data:
            if 'selector' in i:
                allowed_filter+=post_data[i] #Составляем список разрешенных первых букв фамилии
        
        profiles_list = Profile.objects.all()

        allowed_pks = []
        for i in profiles_list:
            if i.lastname[0] in allowed_filter: #Составляем список pk анкет, проходящих фильтр
                allowed_pks.append(i.pk)

        available_filter = Q()
        if request.POST.get('available') == '1': #Фильтр на случай, если нужны только текущие работники
            available_filter = Q(end_work_date=None)

        sector_filter = Q()
        if request.POST.get('sector') != 'all': #Фильтр по отделам
            sector_filter = Q(sector__pk=request.POST.get('sector'))

        profiles = Profile.objects.filter(~available_filter, sector_filter, pk__in=allowed_pks)

        profiles_list = get_queryset(request, profiles)


        empty_result = False
        if len(profiles)==0: #На случай, если не будет подходящих анкет, будет отображаться оповещение
            empty_result = True


        form = ProfileFilterForm() 
        return render(request, template_name, {'profiles_list':profiles_list, 'selector_list':selector_list,'empty_result':empty_result, 'form':form})



#Пагинация
def get_queryset(request, profiles_list):
    Profile.objects.all()
    paginator = Paginator(profiles_list,30)
    page = request.GET.get('page')
    try:
        profiles_list= paginator.page(page)
    except PageNotAnInteger:
        profiles_list = paginator.page(1)
    except EmptyPage:
        profiles_list = paginator.page(paginator.num_pages)
    return profiles_list