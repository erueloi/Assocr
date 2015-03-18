from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from assocr.forms import AssociationForm, UFForm, MemberForm, User_to_AssociationForm, ReceiptForm
from assocr.models import Association, UF, Member, Receipts
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def index(request):
    association_list = Association.objects.all()
    context_dict = {'associations': association_list}
    
    return render(request, 'index.html', context_dict)

@login_required
def association(request, association_id):
    context_dict = {}
    try:
        association = Association.objects.get(id=association_id)
        ufs = UF.objects.filter(association=association)  
        totalufs = ufs.count()
        totalBanc = UF.objects.filter(association=association, currentaccount__gt=0).exclude(currentaccount=0.0).count()   
        context_dict['association'] = association
        context_dict['Ufs'] = ufs 
        context_dict['totalreceipts'] = Receipts.objects.filter(uf=ufs, year=datetime.datetime.now().year).count()    
        context_dict['totalmembers'] = Member.objects.all().filter(uf=ufs).count
        context_dict['totalBanc'] = totalBanc
        context_dict['totalEfectiu'] = totalufs - totalBanc
        context_dict['percent_totalBanc'] = totalBanc * 100 / totalufs
        context_dict['percent_totalEfectiu'] = (totalufs - totalBanc) * 100 / totalufs
                  
    except Association.DoesNotExist:
        pass

    return render(request, 'association.html', context_dict)

@login_required
def add_association(request, association_id=None):
    context_dict = {}
        
    if association_id:
        editassociation = Association.objects.get(id=association_id)
        if editassociation.logotype:
            context_dict['url_image'] = editassociation.logotype.url
    else:
        editassociation = None
    
    if request.method == 'POST':
        form = AssociationForm(request.POST, request.FILES, instance=editassociation)

        if form.is_valid():
            form.save(commit=True)
            if association_id:
                messages.success(request, 'Associacio actualitzada correctament.')
                return association(request, association_id)
            else:
                messages.success(request, 'Associacio afegida correctament.')
                return index(request)            
        else:
            print form.errors
    else:
        form = AssociationForm(instance=editassociation)

    context_dict['form'] = form
    context_dict['association_id'] = association_id
    return render(request, 'add_association.html', context_dict)

@login_required
def add_uf(request, association_id, uf_id=None):

    try:
        assoc = Association.objects.get(id=association_id)
    except Association.DoesNotExist:
        assoc = None
        
    if uf_id:
        edituf = UF.objects.get(id=uf_id)
    else:
        edituf = None

    if request.method == 'POST':
        form = UFForm(request.POST, instance=edituf)
        if form.is_valid():
            if assoc:
                objUf = form.save(commit=False)
                objUf.association = assoc
                objUf.save()
                
                if uf_id:
                    messages.success(request, 'Unitat Familiar actualitzada correctament.')
                    return uf(request, association_id, uf_id)
                else:                    
                    messages.success(request, 'Unitat Familiar afegida correctament.')
                    return association(request, association_id)
        else:
            print form.errors
    else:
        form = UFForm(instance=edituf, initial={'typequote': '1'})
        
    context_dict = {'form':form, 'association': assoc, 'uf_id': uf_id}

    return render(request, 'add_uf.html', context_dict)

@login_required
def uf(request, association_id, uf_id):
    context_dict = {}
    try:
        uf = UF.objects.get(id=uf_id)
        members = Member.objects.filter(uf=uf)
        context_dict['uf'] = uf
        context_dict['idassociation'] = association_id
        context_dict['members'] = members
        context_dict['receipts'] = Receipts.objects.filter(uf=uf)
           
    except UF.DoesNotExist:
        pass

    return render(request, 'uf.html', context_dict)

@login_required
def add_member(request, association_id, uf_id, member_id=None):
    
    try:
        unif = UF.objects.get(id=uf_id)
    except UF.DoesNotExist:
        unif = None
        
    if member_id:
        editmember = Member.objects.get(id=member_id)
    else:
        editmember = None
                        
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=editmember)        
        if form.is_valid():
            if unif:
                mem = form.save(commit=False)
                mem.uf = unif
                mem.save()
                
                if member_id:
                    messages.success(request, 'Soci actualitzada correctament.')
                    return member(request, association_id, uf_id, member_id)
                else:
                    messages.success(request, 'Soci afegit correctament.')
                    return uf(request, association_id, uf_id)
        else:
            print form.errors
    else:
        form = MemberForm(instance=editmember)

    context_dict = {'form':form, 'uf': unif, 'member_id': member_id}
    
    return render(request, 'add_member.html', context_dict)

@login_required
def member(request, association_id, uf_id, member_id):
    context_dict = {}
    try:
        member = Member.objects.get(id=member_id)
        context_dict['member'] = member
           
    except UF.DoesNotExist:
        pass

    return render(request, 'member.html', context_dict)

def page_not_found(request):
    # Dict to pass to template, data could come from DB query
    values_for_template = {}
    return render(request,'404.html',values_for_template,status=404)

@login_required
def calendar(request, association_id):
    context_dict = {}
    try:
        association = Association.objects.get(id=association_id)        
        context_dict['association'] = association
                  
    except Association.DoesNotExist:
        pass

    return render(request, 'calendar.html', context_dict)

@login_required
def user_to_association(request):
    context_dict = {}
       
    if request.method == 'POST':
        form = User_to_AssociationForm(request.POST)
        associationsto = request.POST.getlist('associationsto')
        userselected = request.POST.getlist('users')
        print request
        for u in userselected:
            for assoc in associationsto:
                print assoc
                association = Association.objects.get(id=assoc)
                association.users = User.objects.filter(id=u)
                association.save()
                print 'Hola'
        
    else:
        form = User_to_AssociationForm()
        
    context_dict = {'form':form}

    return render(request, 'users_to_associations.html', context_dict)

@login_required
def get_association_user(request, user_id):
    user = User.objects.get(id=user_id)
    associations = Association.objects.filter(users=user)    
    association_dict = {}
    for association in associations:
        association_dict[association.id] = association.name + ' - ' + str(association.penyanumber)
    return JsonResponse(association_dict, safe=False)

import datetime

@login_required
def generate_receipts(request, association_id):
    
    assoc = Association.objects.get(id=association_id)
    ufs = UF.objects.filter(association=assoc)
    i= 0
    for uf in ufs:
        try:
            r = Receipts.objects.get(uf=uf, year=datetime.datetime.now().year)
        except Receipts.DoesNotExist:
            r = Receipts()
            r.uf = uf
            
        r.year = datetime.datetime.now().year
        r.state = 0        
        r.save()
        i += 1
    
    data_dict = {}
    data_dict['num_receipts'] = i
    
    success_message = 'S\'han generat ' + str(i) + ' rebuts per a l\'any ' + str(datetime.datetime.now().year) + ' correctament.'
    #messages.success(request, success_message)
    data_dict['success'] = success_message
    return JsonResponse(data_dict, safe=False)

@login_required
def add_receipt(request, association_id, uf_id, receipt_id=None):
    
    try:
        unif = UF.objects.get(id=uf_id)
    except UF.DoesNotExist:
        unif = None
        
    if receipt_id:
        editreceipt = Receipts.objects.get(id=receipt_id)
    else:
        editreceipt = None
                        
    if request.method == 'POST':
        form = ReceiptForm(request.POST, instance=editreceipt)        
        if form.is_valid():
            if unif:
                receipt = form.save(commit=False)
                receipt.uf = unif
                receipt.save()
                
                if receipt_id:
                    messages.success(request, 'Rebut actualitzat correctament.')
                    return uf(request, association_id, uf_id)
                else:
                    messages.success(request, 'Rebut afegit correctament.')
                    return uf(request, association_id, uf_id)
        else:
            print form.errors
    else:
        form = ReceiptForm(instance=editreceipt)

    context_dict = {'form':form, 'uf': unif, 'receipt_id': receipt_id}
    
    return render(request, 'add_receipt.html', context_dict)
