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
           
    except Association.DoesNotExist:
        pass

    return render(request, 'association.html', context_dict)

@login_required
def add_association(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = AssociationForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = AssociationForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'add_association.html', {'form': form})

@login_required
def add_uf(request, association_id):

    try:
        assoc = Association.objects.get(id=association_id)
    except Association.DoesNotExist:
                assoc = None

    if request.method == 'POST':
        form = UFForm(request.POST)
        if form.is_valid():
            if assoc:
                uf = form.save(commit=False)
                uf.association = assoc
                uf.save()
                # probably better to use a redirect here.
                return association(request, association_id)
        else:
            print form.errors
    else:
        form = UFForm()

    context_dict = {'form':form, 'association': assoc}

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
def add_member(request, association_id, uf_id):
    
    try:
        unif = UF.objects.get(id=uf_id)
    except UF.DoesNotExist:
        unif = None
                    
    if request.method == 'POST':
        form = MemberForm(request.POST)

        if form.is_valid():
            if unif:
                member = form.save(commit=False)
                member.uf = unif
                member.save()
               
                return uf(request, association_id, uf_id)
        else:
            print form.errors
    else:
        form = MemberForm()

    context_dict = {'form':form, 'uf': unif}
    
    return render(request, 'add_member.html', context_dict)