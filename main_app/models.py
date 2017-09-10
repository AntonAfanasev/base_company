from django.db import models

 
class Profile(models.Model):

    class Meta:
        verbose_name='профиль'
        verbose_name_plural='профили'

    name = models.CharField('Имя', max_length=50)
    lastname = models.CharField('Фамилия', max_length=50)
    middlename = models.CharField('Отчество', max_length=50)
    birthdate = models.DateField('Дата рождения')
    email = models.EmailField('Эл.почта')
    phone= models.CharField('Телефон', max_length=15)
    start_work_date = models.DateField('Дата начала работы')
    end_work_date = models.DateField('Дата окончания работы', null=True, blank=True)
    position = models.CharField('Должность', max_length=50)
    sector = models.ForeignKey('Sector', verbose_name='Отдел')
 
    def __str__(self):
        return '{} {} {}'.format(self.name,self.lastname, self.middlename)
class Sector(models.Model):
    class Meta:
        verbose_name='отдел'
        verbose_name_plural='отделы'
    
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name