from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from assocr.forms import AssociationForm, UFForm, MemberForm
from assocr.models import Association, UF, Member

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
        context_dict['association'] = association
        context_dict['Ufs'] = ufs
        totalmembers = 0
        for uf in ufs:
            members = Member.objects.filter(uf=uf)
            for member in members:
                totalmembers = totalmembers + 1
        
        context_dict['totalmembers'] = totalmembers
                  
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
                 return association(request, association_id)
            else:
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
                    return uf(request, association_id, uf_id)
                else:
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
                    return member(request, association_id, uf_id, member_id)
                else:
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
 

