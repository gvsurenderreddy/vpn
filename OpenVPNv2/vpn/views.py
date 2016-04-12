from django.shortcuts import render
from django.http.response import  HttpResponse, Http404, HttpResponseRedirect
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect
from vpn.models import General, Revoke,PathsVPN
from forms import CommentForm,ContactForm,GenerateCertUsr, RevokeCertUsr, M
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect
from django.template.context_processors import csrf
from django.template import RequestContext
from vpn.services import generate_certs,revoke_certs, stats_certs

# Create your views here.
def test(request):
    view = "basic_one"
    html = "<html><body>This is %s view</html></body>" % view
    return HttpResponse(html)

def status_vpn(request):
    print request.FILES
    x=General.objects.all()
    print x
    return render_to_response('status_vpn.html', {'general': General.objects.all()})

def home_page1(request):
    return render_to_response('index.html')

def home_page2(request):
    view = 'home page OpenVPN'
    return render_to_response('testchart.html')

@csrf_protect
def tabs(request,vpn_id=1):
    path = PathsVPN.objects.get(pathsvpn_general_id=vpn_id)
    name_vpn = General.objects.get(id=vpn_id)
    form = RevokeCertUsr()
    gform = GenerateCertUsr(initial={'location_certificate' : '/etc/openvpn/',
                                     'send_email_certificate': 'oleh.hrebchuk@eleks.com'})
    print request.POST
    if request.method == 'POST':
        gform = GenerateCertUsr(request.POST)
        form = RevokeCertUsr(request.POST)
        if gform.is_valid():
            data = gform.cleaned_data
            print data
            generate_certs(data,path)
        elif form.is_valid():
            data = form.cleaned_data
            revoke_certs(data,path)
            revoke_certs(data,path)
    if request.POST.get('Refresh') == 'Refresh':
                print 'true'
                stats_certs(path,vpn_id)
    context = {
		"form": form,
        "gform": gform,
        "sform": Revoke.objects.filter(certs_general_id=vpn_id),
        "name_vpn": name_vpn,
	}
    return TemplateResponse(request, 'tabs_user_mnt.html', context)

def managment_vpn(request, vpn_id=1):
    comment_form =  CommentForm
    #contact_form = ContactForm(initial={'contact_name':'Hi here'})
    args = {}
    args.update(csrf(request))
    args['vpn'] = General.objects.get(id=vpn_id)
    args['form'] = comment_form
    #args['form'] = contact_form
    return render_to_response('test.html', args)

def list_vpn(request, vpn_id=1):
    args = {}
    args['form'] = General.objects.all()
    return render_to_response('list_vpns.html',args)

@csrf_protect
def create_cert_usr(request):
    print request.POST
    if request.method == 'POST':
        form = GenerateCertUsr(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print data
            generate_certs(data)
            return HttpResponseRedirect('/cert/')
    else:
        form = GenerateCertUsr(initial={'location_cert' : '/etc/openvpn/'})
    context = {
		"form": form,
	}
    return render_to_response('genera_cert.html', RequestContext(request,context))

@csrf_protect
def revoke_cert_usr(request):
    form = RevokeCertUsr(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            data = form.cleaned_data
            revoke_certs(data)
            return HttpResponseRedirect('/revoke/')
    else:
        form = RevokeCertUsr(initial={'location_cert' : '/etc/openvpn/'})
    context = {
		"form": form,
	}
    return render_to_response('revoke_cert.html', RequestContext(request,context))

@csrf_protect
def status_cert(request):
    print request.body
    if request.POST.get('Refresh') == 'Refresh':
        stats_certs()
    context = {
		"form": Revoke.objects.all(),
	}
    return render_to_response('status_cert.html', RequestContext(request,context))

def dropdown(request):
    print request.body
    print request.GET
    if request.GET.get('Action') == 'Action':
        return HttpResponseRedirect('/home/')
    return HttpResponseRedirect('/home/')

def addcomment(request, vpn_id):
    print request.POST
    print vpn_id
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.certs_general = General.objects.get(id=vpn_id)
            z=form.cleaned_data
            print z.keys()
            form.save()
            return redirect('/manage/vpn/%s' % vpn_id)
    form = M()
    return render(request, 'test.html', {form:form})

def addtest(request):
    print request.POST
    form = CommentForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():

            return redirect('/manage/vpn/1')
    else:
        form = ContactForm

    return render(request, 'test.html', {form:form})

def contact(request):
    print request.POST

    form_class = ContactForm
    return render(request, 'contact.html', {
        'form': form_class,
    })