from django import forms
from .models import Profile, Sector
import sys

ALPHABET = (
    ('АБВГДЕ','A-E',),
    ('ЁЖЗИЙ', 'Ё-Й',),
    ('ЗИЙК', 'З-К', ),
    ('ЛМНОП', 'Л-П',),
    ( 'РСТУ','Р-У',),
    ('ФХЦЧШ', 'Ф-Ш',),
    ('ЩЫЭЮЯ', 'Щ-Я',),
)

def build_sectors_list():
	choices = [('all', 'Все отделы')]
	sectors = Sector.objects.all()
	for i in sectors:
		choices.append((i.pk, i.name))
	return choices

class ProfileAdminForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('name', 'lastname', 'middlename', 'birthdate', 'email', 'phone','start_work_date', 'end_work_date', 'position', 'sector' )


class ProfileFilterForm(forms.Form):
	def __init__(self, *args, **kwargs):
		choices = [('all', 'Все отделы')]
		sectors = Sector.objects.all()
		for i in sectors:
			choices.append((i.pk, i.name))
		self.fields['sector'].choices=choices

	available = forms.BooleanField(label = 'Работают в компании', required=False, \
		widget=forms.CheckboxInput(attrs={'name':'available', 'value':'1','style':'selector_element',}))
	sector = forms.ChoiceField(label='Отдел', required=False, \
			widget=forms.Select(attrs={'name':'sector', 'style':'selector_element',}))