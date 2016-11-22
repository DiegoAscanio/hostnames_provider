'''
        @file forms.py
        @lastmod 8/11/2016
'''

# Importacoes
from django import forms

# Area de criacao de forms

#Form de Login (nao utilizado no momento)
class LoginForm(forms.Form):
    user = forms.CharField(label='user')
    password = forms.CharField(label='password')

#Form de Upload de Arquivo .csv
class UploadFileForm(forms.Form):
    '''
    Classe de Upload de Arquivo: Usada na validacao de um Formulario de Upload
    '''
    file = forms.FileField(label='file')

#Form de Criacao de Host
class CreateForm(forms.Form):
    '''
    Classe de Criacao de Host: Usada na validacao de um Host a ser adicionado
    '''
    hostname = forms.CharField(label='hostname')
    mac = forms.CharField(label='mac', max_length=17)
    ip = forms.CharField(label='ip', max_length=15)

#Form de Visualizacao de Host
class RetrieveForm(forms.Form):
    hostname = forms.CharField(label='hostname')
    mac = forms.CharField(label='mac', max_length=17)
    ip = forms.CharField(label='ip', max_length=15)

#Form de Edicao de Host
class EditForm(forms.Form):
    '''
    Classe de Edicao de Host: Usada na validacao de um Host a ser atualizado
    '''
    id = forms.CharField(label='id')
    hostname = forms.CharField(label='hostname')
    mac = forms.CharField(label='mac', max_length=17)
    ip = forms.CharField(label='ip', max_length=15)

#Form de Exclusao de Host
class DeleteForm(forms.Form):
    '''
    Classe de Exclusao de Host: Usada na validacao de um Host a ser excluido
    '''
    ip = forms.CharField(label='ip_address')

#Form do Contato
class ContactForm(forms.Form):
    first_name = forms.CharField(label='first_name')
    last_name = forms.CharField(label='last_name')
    email = forms.EmailField(label='email')
    phone = forms.CharField(label='phone')
    comment = forms.CharField(label='comment')
