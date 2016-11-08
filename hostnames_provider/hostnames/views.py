'''
        @file views.py
        @lastmod 8/11/2016
'''

#Importacoes
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

import csv, pdb, json

from .models import Host
from .forms import *
from .serializers import HostSerializer

from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO


# Area de criacao de views

#Metodo padrao para erro
def showError(request,mensagem):
	c = RequestContext (request, {
			'mensagem' : mensagem
		})
		
	templateError = loader.get_template('hostnames/error.html')

	return HttpResponse(templateError.render(c))

#Renderiza o conteudo de um HttpResponse em JSONResponse
class JSONResponse(HttpResponse):
    '''
    HttpResponse que renderiza o conteudo em formato JSON
    '''
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def host_list(request, format=None):
    '''
    Lista todos os hosts, ou devolve um host especifico
    '''
    if request.method == 'GET':
        hosts = Host.objects.all()
        serializer = HostSerializer(hosts, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
def host_detail_ipaddress(request, ip, format=None):
    '''
    Retorna um JSON com o IP requisitado
    '''
    if request.method == 'GET':
        try:
            host = Host.objects.filter(ip_address__icontains = ip)
        except Host.DoesNotExist:
            return error
        serializer = HostSerializer(data = host,many=True)
	serializer.is_valid()
	content = JSONRenderer().render(serializer.data)

	return JSONResponse(serializer.data) if (len(serializer.data) != 0) else showError(request,'ERRO: IP INEXISTENTE!')

@csrf_exempt
def host_detail_macaddress(request, mac, format=None):
    '''
    Retorna um JSON com o MAC requisitado
    '''
    
    if request.method == 'GET':
        try:
            host = Host.objects.filter(mac_address__icontains = mac)
	   
        except Host.DoesNotExist:
            return error
      	serializer = HostSerializer(data = host,many=True)
	serializer.is_valid()
	content = JSONRenderer().render(serializer.data)

        return JSONResponse(serializer.data) if (len(serializer.data) != 0) else showError(request,'ERRO: MAC INEXISTENTE!')

@csrf_exempt
def host_detail_pesquisar(request, pesquisa):
    '''
    Retorna um JSON com o resultado da pesquisa (Geral ou Especifica)
    '''
    if request.method == 'GET':
        try:
	    if (pesquisa != None):
                if(len(pesquisa) == 1):
                    host = Host.objects.filter(Q(hostname__icontains = pesquisa[0]) | Q(mac_address__icontains = pesquisa[0]) | Q(ip_address__icontains = pesquisa[0]))
            	else:
                    host = Host.objects.filter(hostname__icontains = pesquisa[0],mac_address__icontains = pesquisa[1],ip_address__icontains = pesquisa[2])
	    else:
		host = Host.objects.all()
        except Host.DoesNotExist:
            return error
        serializer = HostSerializer(data = host,many=True)
	serializer.is_valid()
	content = JSONRenderer().render(serializer.data)
	return content        



def hostname(request):
    if request.method == 'GET':
        #instancia objeto do tipo HostForm contendo os dados do form recebido pelo GET
        form = HostForm(request.GET)
         
        #testa se o form e valido
        if form.is_valid():
            #obtem os dados recebidos no form
            mac = form.cleaned_data['mac']
            ip = form.cleaned_data['ip']
            
            #prepara um objeto do tipo Host para ser enviado por GET
            h = Host.objects.get(ip_address=ip, mac_address=mac)

            #envia
            return HttpResponse(h.hostname)
        else:
            #envia o proprio form
            return HttpResponse(form)

#View do delete
def delete(request):
    '''
    View da Exclusao de Host: Deleta um ou mais Hosts pelo ID
    '''
    #formalidades de seguranca
    c = {}
    c.update(csrf(request))

    
    if request.method == 'POST':
        #instancia um objeto DeleteForm contendo o request passado por POST
        form = DeleteForm(request.POST)

        #testa se o form e valido
        if form.is_valid():
            # pega a(s) id(s) do(s) host(s) a ser(em) excluido(s)
            id = form.cleaned_data['id']
            # separa os hosts pela virgula e armazena em um array (em caso de dois ou mais hosts)
            idSplit = id.split(',')
            
            # itera o array de hosts
            for i in idSplit:
                # deleta host por host
                h = Host.objects.filter(id=i).delete()

            #retorna redirecionamento para a pagina de listagem
            return HttpResponseRedirect("/list")
        else:
            return HttpResponseRedirect("/create")

#View da tela de erro
def error(request):
    if (request.method == 'POST'): # redirecionamento padrao
        template = loader.get_template('hostnames/error.html')
        c = RequestContext (request, {})
        return HttpResponse(template.render(c))
    if (request.method == 'GET'):
        template = loader.get_template('hostnames/error.html')
        c = RequestContext (request, {})        
        return HttpResponse(template.render(c))

#View do index
def index(request):
    '''
    View da Tela de Index: Redireciona para a Pagina de Insercao de Host, caso o Usuario esteja logado.
    Caso contrario, carrega o Template do Index
    '''
    if (isUserAutenticated(request)):
        return HttpResponseRedirect("/create")
    else:
        template = loader.get_template('hostnames/index.html')

        c = RequestContext (request, {})        
        return HttpResponse(template.render(c))

#View do perfil
def options(request):
    template = loader.get_template('hostnames/opcoes.html')
    c = RequestContext (request, {})        
    return HttpResponse(template.render(c))

#View do perfil
def profile(request):
    template = loader.get_template('hostnames/perfil.html')
    c = RequestContext (request, {})        
    return HttpResponse(template.render(c))
        
#View da ajuda
def help(request):
    template = loader.get_template('hostnames/ajuda.html')
    c = RequestContext (request, {})        
    return HttpResponse(template.render(c))

#View da tela de login (nao mais utilizado)
def login(request):    
    if (request.method == 'GET'): # redirecionamento padrao

        #carrega o template da tela de login
        template = loader.get_template('registration/login.html')

        #carrega o contexto    
        c = RequestContext (request, {})

        #retorna o template a ser renderizado
        return HttpResponse(template.render(c))

    if (request.method == 'POST'): 
        #formalidades de seguranca        
        c = {}
        c.update(csrf(request))

        #recebe o form
        form = LoginForm(request.POST)

        #redireciona caso esteja autenticado
        if isUserAutenticated(form) is not None:
            #redireciona para o template da list
            return HttpResponseRedirect("/list")
        else:
            #redireciona para o template do index
            return HttpResponseRedirect("/")

#funcao para verificar se usuario esta autenticado
def isUserAutenticated(request):
    #testa autenticacao do usuario (verifica se ele esta logado ou nao)        
    answer = True if request.user.is_authenticated() else False
    return answer

#processa a operacao de logout
def logout(request):
    """
    Desconecta o usuario e envia mensagem
    """
    logout(request)
    #obtem um redirecionamento por GET para o index
    redirect_to = request.REQUEST.get('/', '')

    if redirect_to:
        netloc = urlparse.urlparse(redirect_to)[1]
        # Checagem de seguranca -- nao permite o redirecionamento para um host diferente.
        if not (netloc and netloc != request.get_host()):
            return HttpResponseRedirect(redirect_to)

#View da tela de create
@login_required
def create(request):
    if (request.method == 'GET'): # redirecionamento padrao

        #carrega template
        template = loader.get_template('hostnames/create.html')

        #solicita contexto
        c = RequestContext (request, {})

        #responde
        return HttpResponse(template.render(c))
    if (request.method == 'POST'):
        #formalidades de seguranca
        c = RequestContext (request, {})
        c.update(csrf(request))

        #recebe os dados do form
        form = CreateForm(request.POST)

        #testa se o form foi e valido
        if (form.is_valid()):
            
            #captura os dados de cada campo do form
            hostForm = form.cleaned_data['hostname']
       	    macForm  = form.cleaned_data['mac']
            ipForm   = form.cleaned_data['ip']

            #testa duplicidade de ip
	    hosts = Host.objects.all().filter(ip_address__icontains = ipForm)
            
	    if(len(hosts) > 0):
	    	c = RequestContext (request, {
			'mensagem' : 'ERRO: IP JA EXISTENTE NO BANCO DE DADOS!'
		})
		
		templateError = loader.get_template('hostnames/error.html')
		return showError(request,'ERRO: IP JA EXISTENTE NO BANCO DE DADOS!')
	    else:
		#instancia um objeto do tipo Host contendo os dados do form
            	h = Host(hostname=hostForm,mac_address=macForm,ip_address=ipForm)
            	#salva o objeto no banco de dados
            	h.save()
  
            	#devolve um redirecionamento para a pagina de listagem
            	return HttpResponseRedirect("/list")
        else:
            c = RequestContext (request, {
			'mensagem' : 'ERRO: IP FORA DO PADRAO!'
	    })
	
	    templateError = loader.get_template('hostnames/error.html')
	    return showError(request,'ERRO: IP FORA DO PADRAO!')

#View da tela de upload csv
def upload(request):
    #formalidades de seguranca
    c = {}
    c.update(csrf(request))

    #instancia um objeto do time UploadFileForm que recebe o request passado por POST e o arquivo
    form = UploadFileForm(request.POST, request.FILES)

    #testa se o form e valido
    if form.is_valid():
        #obtem o arquivo passado na requisicao
        filename = request.FILES['file']

        #itera no arquivo csv 
        with open(filename.name, 'r') as csvfile:
            #separa os dados utilizando o delimitador | e cria um array os contendo em spamreader                
            spamreader = csv.reader(csvfile, delimiter='|')

            #variavel de controle da quantidade de execucoes do loop
            n = 0

            #para cada elemento em spamreader armazene seu conteudo em row
            for row in spamreader:
                #incrementa n ate obter a quantidade total de linhas
                n = n + 1
            #retorna o ponteiro para o inicio do arquivo
            csvfile.seek(0)

            #percorre spamreader buscando os dados desejados
            for (h,m,i) in spamreader:
                #cria um objeto do tipo Host contendo os dados obtidos
                h = Host(hostname = h, mac_address = m, ip_address = i)

                #salva no banco de dados o objeto com os dados obtidos
                h.save()

                #decrementa o contador da quantidade de execucoes
                n = n - 1

                #caso ja tenha feito todos, entao pare
                if(n == 1):
                    break

        #redireciona para a pagina de listagem
        return HttpResponseRedirect("/list")
    else:
        #redireciona para a pagina de listagem
        return HttpResponseRedirect("/list")

#View da tela de upload
def download(request):
        # Cria o objeto Http Response com o cabecalho de CSV apropriado.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="hostnames.csv"'

        # Pega todos os hosts do banco de dadosz
        hosts = Host.objects.all()
        writer = csv.writer(response)

        # Percorre todos os hosts
        for h in hosts:
            # Escreve uma linha no arquivo .csv de acordo com o padrao
            # <<hostname|mac|ip>>
            writer.writerow([
                smart_str(h.hostname+"|"+h.mac_address+"|"+h.ip_address),
            ])
        # Retorna a resposta em formato de arquivo, possibilitando o download
        return response

#View da tela de update
@login_required
def update(request):
    if (request.method == 'GET'): # redirecionamento padrao
        #resgata o ip passado por GET
        ip = request.GET['ip']
        #carrega o template da tela de update
        template = loader.get_template('hostnames/update.html')

        #passa no contexto o ip do host desejado        
        c = RequestContext(request, {
            'host' : Host.objects.get(ip_address=ip),
        })

        #responde com o template e o renderiza
        return HttpResponse(template.render(c))

    if (request.method == 'POST'):
        #formalidades de seguranca 
        c = {}
        c.update(csrf(request))

        #instacia um objeto EditForm contendo os dados de atualizacao
        form = EditForm(request.POST)

        #testa se o form e valido
        if form.is_valid():
            #instancia um objeto do tipo Host que contem o id passado no form
            h = Host.objects.get(id=form.cleaned_data['id'])
            #seta o valor de hostname com o valor passado no form
            h.hostname = form.cleaned_data['hostname']
            #seta o valor de mac_adress com o valor passado no form
            h.mac_address = form.cleaned_data['mac']
            #seta o valor do ip_adress com o valor passado no form
            h.ip_address = form.cleaned_data['ip']
            #salva no banco de dados o objeto atualizado
            h.save()

            #redireciona para a pagina de listagem
            return HttpResponseRedirect("/list")
        else:
            return HttpResponseRedirect("/list")

#View da tela de retrieve
@login_required
def retrieve(request):
    #captura o ip passado por GET
    ip = request.GET['ip']
    #carrega o template do retrieve
    template = loader.get_template('hostnames/retrieve.html')
    
    #requisita o contexto passando um objeto host contendo o ip        
    c = RequestContext(request, {
        'host' : Host.objects.get(ip_address=ip),
    })

    #responde com o template renderizado
    return HttpResponse(template.render(c))

#View da pagina de listagem
@login_required
def list(request):
    host_list = Host.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(host_list, 10)
    try:
        hosts = paginator.page(page)
    except PageNotAnInteger:
        hosts = paginator.page(1)
    except EmptyPage:
        hosts = paginator.page(paginator.num_pages)

    #carrega o template da list
    template = loader.get_template('hostnames/list.html')
    
    #solicita um contexto contendo todos os objetos do tipo Host
    c = RequestContext(request, {
        'hosts' : hosts
    })

    #responde com o template renderizado
    return HttpResponse(template.render(c))

# Ordena os campos da pesquisa de acordo com a ordem - Hostname, Mac, Ip
def ordenaPesquisa(pesquisa):
	pesquisaOrdenada = ['','','']
	if (pesquisa != None):
		for i in pesquisa:
			if ("hostname" in i):
				pesquisaOrdenada[0] = i
			if ("mac" in i):
				pesquisaOrdenada[1] = i
			if ("ip" in i):
				pesquisaOrdenada[2] = i
		pesquisaOrdenada = separaDados(pesquisaOrdenada)
	else:
		pesquisaOrdenada = None
	
	return pesquisaOrdenada

# Cria um Array 
def separaDados(pesquisa):
	listaDados = ['','','']
	if(pesquisa[0] is not ''):
		listaDados[0] = pesquisa[0][9:]
	if(pesquisa[1] is not ''):
		listaDados[1] = pesquisa[1][4:]
	if(pesquisa[2] is not ''):
		listaDados[2] = pesquisa[2][3:]
	return listaDados

# View do Resultado da Pesquisa
def pesquisar(request):
     if request.method == 'GET':
        #carrega o template da list
	pesquisa = request.GET['pesquisa']
	
	pesquisaSplit = pesquisa.split(";")

	if(';' not in pesquisa and '=' not in pesquisa):
		if(len(pesquisa) == 1):
			pesquisa2 = None
		else:
			pesquisa2 = [pesquisa]
	else:
		pesquisa2 = ordenaPesquisa(pesquisaSplit)
	content = host_detail_pesquisar(request, pesquisa2)
	stream = BytesIO(content)
	data = JSONParser().parse(stream)

	serializer = HostSerializer(data=data)

	serializer.is_valid()

	template = loader.get_template('hostnames/pesquisar.html')
    	page = request.GET.get('page', 1)
	
    	paginator = Paginator(data, 10)
    	try:
        	hosts = paginator.page(page)	
	except PageNotAnInteger:
        	hosts = paginator.page(1)
    	except EmptyPage:
        	hosts = paginator.page(paginator.num_pages)

	c = RequestContext (request, {
            'hosts' : hosts,
            'pesquisa': pesquisa
        })

        #responde com o template renderizado
        return HttpResponse(template.render(c))   

class HostList(generics.ListCreateAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class HostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
