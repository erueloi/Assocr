from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from assocr.forms import AssociationForm, UFForm, MemberForm
from assocr.models import Association, UF, Member, MemberResource

from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from import_export.formats import base_formats
from import_export.resources import modelresource_factory
from import_export.forms  import ImportForm, ConfirmImportForm
from import_export.results import RowResult
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.urlresolvers import reverse
import os.path

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
        context_dict['totalmembers'] = Member.objects.all().filter(uf=ufs).count
                  
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

class MembersExport(View):

    def get(self, *args, **kwargs ):
        association = Association.objects.get(id=self.kwargs['association_id'])
        ufs = UF.objects.filter(association=association)
        dataset = MemberResource().export(Member.objects.all().filter(uf=ufs))
        response = HttpResponse(dataset.xls, content_type="xls")
        response['Content-Disposition'] = 'attachment; filename=LlistatSocis_' + association.name +'.xls'
        return response

import tempfile
  
class MemberImport(View):
    model = Member
    from_encoding = "utf-8"  

    #: import / export formats
    DEFAULT_FORMATS = (
        base_formats.CSV,
        base_formats.XLS,
        base_formats.TSV,
        base_formats.ODS,
        base_formats.JSON,
        base_formats.YAML,
        base_formats.HTML,
    )
    formats = DEFAULT_FORMATS
    #: template for import view
    import_template_name = 'members/import.html'
    resource_class = MemberResource

    def get_import_formats(self):
        """
        Returns available import formats.
        """
        return [f for f in self.formats if f().can_import()]

    def get_resource_class(self):
        if not self.resource_class:
            return modelresource_factory(self.model)
        else:
            return self.resource_class

    def get_import_resource_class(self):
        """
        Returns ResourceClass to use for import.
        """
        return self.get_resource_class()

    def get(self, *args, **kwargs ):
        '''
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        '''
        resource = self.get_import_resource_class()()

        context = {}
        association = Association.objects.get(id=self.kwargs['association_id'])
        context['association'] = association
        import_formats = self.get_import_formats()
        form = ImportForm(import_formats,
                          self.request.POST or None,
                          self.request.FILES or None)

        if self.request.POST and form.is_valid():
            input_format = import_formats[
                int(form.cleaned_data['input_format'])
            ]()
            import_file = form.cleaned_data['import_file']
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
                for chunk in import_file.chunks():
                    uploaded_file.write(chunk)

            # then read the file, using the proper format-specific mode
            with open(uploaded_file.name,
                      input_format.get_read_mode()) as uploaded_import_file:
                # warning, big files may exceed memory
                data = uploaded_import_file.read()
                if not input_format.is_binary() and self.from_encoding:
                    data = force_text(data, self.from_encoding)
                dataset = input_format.create_dataset(data)
                result = resource.import_data(dataset, dry_run=True,
                                              raise_errors=False)

            context['result'] = result

            if not result.has_errors():
                context['confirm_form'] = ConfirmImportForm(initial={
                    'import_file_name': os.path.basename(uploaded_file.name),
                    'input_format': form.cleaned_data['input_format'],
                })

        context['form'] = form
        context['opts'] = self.model._meta
        context['fields'] = [f.column_name for f in resource.get_fields()]

        return TemplateResponse(self.request, [self.import_template_name], context)


    def post(self, *args, **kwargs ):
        '''
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        '''
        resource = self.get_import_resource_class()()

        context = {}
        association = Association.objects.get(id=self.kwargs['association_id'])
        context['association'] = association
        
        import_formats = self.get_import_formats()
        form = ImportForm(import_formats,
                          self.request.POST or None,
                          self.request.FILES or None)

        if self.request.POST and form.is_valid():
            input_format = import_formats[
                int(form.cleaned_data['input_format'])
            ]()
            import_file = form.cleaned_data['import_file']
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
                for chunk in import_file.chunks():
                    uploaded_file.write(chunk)

            # then read the file, using the proper format-specific mode
            with open(uploaded_file.name,
                      input_format.get_read_mode()) as uploaded_import_file:
                # warning, big files may exceed memory
                data = uploaded_import_file.read()
                if not input_format.is_binary() and self.from_encoding:
                    data = force_text(data, self.from_encoding)
                dataset = input_format.create_dataset(data)
                result = resource.import_data(dataset, dry_run=True,
                                              raise_errors=False)

            context['result'] = result

            if not result.has_errors():
                context['confirm_form'] = ConfirmImportForm(initial={
                    'import_file_name': os.path.basename(uploaded_file.name),
                    'input_format': form.cleaned_data['input_format'],
                })

        context['form'] = form
        context['opts'] = self.model._meta
        context['fields'] = [f.column_name for f in resource.get_fields()]

        return TemplateResponse(self.request, [self.import_template_name], context)

class MemberProcessImport(View):
    model = Member
    from_encoding = "utf-8"

    #: import / export formats
    DEFAULT_FORMATS = (
        base_formats.CSV,
        base_formats.XLS,
        base_formats.TSV,
        base_formats.ODS,
        base_formats.JSON,
        base_formats.YAML,
        base_formats.HTML,
    )
    formats = DEFAULT_FORMATS
    #: template for import view
    import_template_name = 'members/import.html'
    resource_class = MemberResource

    def get_import_formats(self):
        """
        Returns available import formats.
        """
        return [f for f in self.formats if f().can_import()]

    def get_resource_class(self):
        if not self.resource_class:
            return modelresource_factory(self.model)
        else:
            return self.resource_class

    def get_import_resource_class(self):
        """
        Returns ResourceClass to use for import.
        """
        return self.get_resource_class()

    def post(self, *args, **kwargs ):
        '''
        Perform the actual import action (after the user has confirmed he
        wishes to import)
        '''
        association = Association.objects.get(id=self.kwargs['association_id'])
        opts = self.model._meta
        resource = self.get_import_resource_class()()

        confirm_form = ConfirmImportForm(self.request.POST)
        if confirm_form.is_valid():
            import_formats = self.get_import_formats()
            input_format = import_formats[
                int(confirm_form.cleaned_data['input_format'])
            ]()
            import_file_name = os.path.join(
                tempfile.gettempdir(),
                confirm_form.cleaned_data['import_file_name']
            )
            import_file = open(import_file_name, input_format.get_read_mode())
            data = import_file.read()
            if not input_format.is_binary() and self.from_encoding:
                data = force_text(data, self.from_encoding)
            dataset = input_format.create_dataset(data)
            
            result = resource.import_data(dataset, dry_run=False,
                                 raise_errors=True)

            # Add imported objects to LogEntry
            ADDITION = 1
            CHANGE = 2
            DELETION = 3
            logentry_map = {
                RowResult.IMPORT_TYPE_NEW: ADDITION,
                RowResult.IMPORT_TYPE_UPDATE: CHANGE,
                RowResult.IMPORT_TYPE_DELETE: DELETION,
            }
            content_type_id=ContentType.objects.get_for_model(self.model).pk
            '''
            for row in result:
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=content_type_id,
                    object_id=row.object_id,
                    object_repr=row.object_repr,
                    action_flag=logentry_map[row.import_type],
                    change_message="%s through import_export" % row.import_type,
                )
            '''
            success_message = _('Import finished')
            messages.success(self.request, success_message)
            import_file.close()
                
            id = association.id  
            url = reverse('assocr.views.association', args=(id,))
            return HttpResponseRedirect(url)
