from django.views.generic import View
from django.template.response import TemplateResponse
from import_export.formats import base_formats
from import_export.resources import modelresource_factory
from import_export.forms  import ImportForm, ConfirmImportForm
from import_export.results import RowResult
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from assocr.admin import MemberResource
from assocr.models import Association, UF, Member, Receipts
from assocr.PySepaDD import PySepaDD
import os.path
import tempfile
import datetime

class MembersExport(View):

    def get(self, *args, **kwargs ):
        association = Association.objects.get(id=self.kwargs['association_id'])
        ufs = UF.objects.filter(association=association)
        dataset = MemberResource().export(Member.objects.all().filter(uf=ufs))
        print dataset
        response = HttpResponse(dataset.xls, content_type="xls")
        response['Content-Disposition'] = 'attachment; filename=LlistatSocis_' + association.name +'.xls'
        return response


  
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

class GenerateXmlSEPAExport(View):

    def get(self, *args, **kwargs ):       
        assoc = Association.objects.get(id=self.kwargs['association_id'])
        config = {"name": assoc.name,
              "IBAN": self.calc_iban(str(assoc.currentaccount)),
              "BIC": "BANKNL2A",
              "creditor_id": "000000",
              "currency": "EUR"
              }
        psdd = PySepaDD(config)           
        ufs = UF.objects.filter(association=assoc,state=True,currentaccount__gt=0).exclude(currentaccount=0.0)
        for uf in ufs:
            r = Receipts.objects.get(uf=uf, year=datetime.datetime.now().year)
            for mem in Member.objects.filter(uf=uf):
                name = mem.firstsurname + ' ' + mem.secondsurname 
            payment = {"name": name,
                "IBAN": self.calc_iban(str(uf.currentaccount)),
                "BIC": "BANKNL2A",
                "amount": 30,
                "type": "RCUR",
                "collection_date": datetime.date.today(),
                "mandate_id": str(uf.id),
                "mandate_date": datetime.date.today(),
                "description": "Quota"
               }
            psdd.add_payment(payment)  
            r.state = 1
            r.save()   
        
        data_dict = {}
              
        response = HttpResponse(psdd.export(), content_type="text/xml")
        response['Content-Disposition'] = 'attachment; filename=LlistatRebuts_' + assoc.name +'.xml'
        return response
    
    def mod97(self, digit_string):
    #Modulo 97 for huge numbers given as digit strings.
    #This function is a prototype for a JavaScript implementation.
    #In Python this can be done much easier: long(digit_string) % 97.
    
        m = 0
        for d in digit_string:
            m = (m * 10 + int(d)) % 97
        return m
    
    #calculo del formato iban de una cuenta bancaria
    def calc_iban(self, acc_number):
        iban = "ES" + "00" + acc_number
        code     = iban[:2]
        checksum = iban[2:4]
        bban     = iban[4:]
        digits = ""
        for ch in bban.upper():
            if ch.isdigit():
                digits += ch
            else:
                digits += str(ord(ch) - ord("A") + 10)
        for ch in code:
            digits += str(ord(ch) - ord("A") + 10)
        digits += checksum
        checksum = 98 - self.mod97(digits)
        checksum = (str(checksum)).zfill(2)
        return "ES" + checksum + acc_number