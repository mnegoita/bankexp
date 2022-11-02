from django.views.generic import FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import now
from django.utils.encoding import force_str
from django.conf import settings

from import_export.formats import base_formats
from import_export.resources import modelresource_factory
from import_export.tmp_storages import TempFolderStorage

import os

from .forms import ImportForm, ConfirmImportForm, ExportForm




TMP_STORAGE_CLASS = getattr(settings, 'IMPORT_EXPORT_TMP_STORAGE_CLASS', TempFolderStorage)

DEFAULT_FORMATS = (
    base_formats.CSV,
    base_formats.XLS,
    base_formats.TSV,
    base_formats.ODS,
    base_formats.JSON,
    base_formats.YAML,
    base_formats.HTML,
)


class TransactionImportView(FormView):
    """ 
    Combines django.views.generic.FormView with
    import_export.admin.ImportExportMixin to reproduce, in a CBV, the
    Django admin import integration from Django-import-export.

    This view is specifically used for Transactions Import
    """
    import_resource_class = None
    resource_class = None
    form_class = ImportForm
    confirm_form_class = ConfirmImportForm
    model = None
    formats = DEFAULT_FORMATS
    from_encoding = "utf-8"
    tmp_storage_class = None
    success_url = None
    confirm = False # serve .as_view(confirm=True) at a different URL to perform the import
    account = None

    
    def get(self, request, *args, **kwargs):
        form = self.get_form()
        resource = self.get_import_resource_class()()

        return self.render_to_response(self.get_context_data(
            form=form,
            fields=[f.column_name for f in resource.get_fields()],
        ))

    def get_form_kwargs(self, import_formats=True):
        kwargs = super().get_form_kwargs()

        if import_formats is True:
            kwargs['import_formats'] = self.get_import_formats()

        return kwargs

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        if form_class is self.form_class:
            import_formats = True
        else:
            import_formats = False
        return form_class(**self.get_form_kwargs(import_formats=import_formats))

    def post(self, request, *args, **kwargs):

        if self.confirm is True:
            confirm_form = self.get_form(form_class=self.confirm_form_class)
            if confirm_form.is_valid():
                return self.process_import(confirm_form)
        return super().post(request, *args, **kwargs)

    def get_import_formats(self):
        """
        Returns available import formats.
        """
        return [f for f in self.formats if f().can_import()]

    def create_dataset(self, input_format, data):
        """ 
        Separate, so that this is hookable for extra logic.
        """

        dataset = input_format.create_dataset(data)
        return dataset

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

    def get_tmp_storage_class(self):
        if self.tmp_storage_class is None:
            return TMP_STORAGE_CLASS
        else:
            return self.tmp_storage_class


    def remove_blanks(self, data):
        # Remove empty lines
        return os.linesep.join([s for s in data.splitlines() if s.strip()])

    def form_valid(self, form):
        """ 
        This bit reproduces ImportMixin.import_action

        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        """

        TransactionImportView.account = self.request.POST['acc_choice'] 

        resource = self.get_import_resource_class()()
        context = {}
        import_formats = self.get_import_formats()
        input_format = import_formats[
            int(form.cleaned_data['input_format'])
        ]()
        import_file = form.cleaned_data['import_file']
        # first always write the uploaded file to disk as it may be a
        # memory file or else based on settings upload handlers
        tmp_storage = self.get_tmp_storage_class()()
        data = bytes()
        for chunk in import_file.chunks():
            data += chunk

        tmp_storage.save(data, input_format.get_read_mode())

        # then read the file, using the proper format-specific mode
        # warning, big files may exceed memory
        data = tmp_storage.read(input_format.get_read_mode())
        if not input_format.is_binary() and self.from_encoding:
            data = force_str(data, self.from_encoding)

        # Clean empty lines
        data = self.remove_blanks(data)

        dataset = self.create_dataset(input_format, data)

        result = resource.import_data(dataset, dry_run=True,
                                      raise_errors=False,
                                      file_name=import_file.name,
                                      user=self.request.user)
        context['result'] = result

        if not result.has_errors():
                        
            context['confirm_form'] = self.confirm_form_class(initial={
                'import_file_name': tmp_storage.name,
                'original_file_name': import_file.name,
                'input_format': form.cleaned_data['input_format'],
            })
        return self.render_to_response(self.get_context_data(
            form=form,
            fields=[f.column_name for f in resource.get_fields()],
            **context))


    def process_import(self, confirm_form):
        """ 
        This bit reproduces ImportMixin.process_import
        """

        resource = self.get_import_resource_class()()
        import_formats = self.get_import_formats()
        input_format = import_formats[
            int(confirm_form.cleaned_data['input_format'])
        ]()
        tmp_storage = self.get_tmp_storage_class()(
            name=confirm_form.cleaned_data['import_file_name'])
        data = tmp_storage.read(input_format.get_read_mode())
        if not input_format.is_binary() and self.from_encoding:
            data = force_str(data, self.from_encoding)
        
        # Clean empty lines
        data = self.remove_blanks(data)

        dataset = self.create_dataset(input_format, data)

        resource.import_data(
            dataset, dry_run=False, raise_errors=True,
            file_name=confirm_form.cleaned_data['original_file_name'],
            user=self.request.user)
        
        tmp_storage.remove()

        return HttpResponseRedirect(self.get_success_url())



class ImportView(FormView):
    """ Combines django.views.generic.FormView with
    import_export.admin.ImportExportMixin to reproduce, in a CBV, the
    Django admin import integration from Django-import-export.
    """
    import_resource_class = None
    resource_class = None
    form_class = ImportForm
    confirm_form_class = ConfirmImportForm
    model = None
    formats = DEFAULT_FORMATS
    from_encoding = "utf-8"
    tmp_storage_class = None
    success_url = None
    confirm = False #.as_view(confirm=True) at a different URL to perform the import

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        resource = self.get_import_resource_class()()

        return self.render_to_response(self.get_context_data(
            form=form,
            fields=[f.column_name for f in resource.get_fields()],
        ))

    def get_form_kwargs(self, import_formats=True):
        kwargs = super().get_form_kwargs()

        if import_formats is True:
            kwargs['import_formats'] = self.get_import_formats()

        return kwargs

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        if form_class is self.form_class:
            import_formats = True
        else:
            import_formats = False
        return form_class(**self.get_form_kwargs(import_formats=import_formats))

    def post(self, request, *args, **kwargs):

        if self.confirm is True:
            confirm_form = self.get_form(form_class=self.confirm_form_class)
            if confirm_form.is_valid():
                return self.process_import(confirm_form)
        return super().post(request, *args, **kwargs)

    def get_import_formats(self):
        """
        Returns available import formats.
        """
        return [f for f in self.formats if f().can_import()]

    def create_dataset(self, input_format, data):
        """ 
        Separate, so that this is hookable for extra logic.
        """

        dataset = input_format.create_dataset(data)
        return dataset


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

    def get_tmp_storage_class(self):
        if self.tmp_storage_class is None:
            return TMP_STORAGE_CLASS
        else:
            return self.tmp_storage_class


    def remove_blanks(self, data):
        # Remove empty lines
        return os.linesep.join([s for s in data.splitlines() if s.strip()])

    def form_valid(self, form):
        """ 
        This bit reproduces ImportMixin.import_action

        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        """

        resource = self.get_import_resource_class()()
        context = {}
        import_formats = self.get_import_formats()
        input_format = import_formats[
            int(form.cleaned_data['input_format'])
        ]()
        import_file = form.cleaned_data['import_file']
        # first always write the uploaded file to disk as it may be a
        # memory file or else based on settings upload handlers
        tmp_storage = self.get_tmp_storage_class()()
        data = bytes()
        for chunk in import_file.chunks():
            data += chunk

        tmp_storage.save(data, input_format.get_read_mode())

        # then read the file, using the proper format-specific mode
        # warning, big files may exceed memory
        data = tmp_storage.read(input_format.get_read_mode())
        if not input_format.is_binary() and self.from_encoding:
            data = force_str(data, self.from_encoding)

        # Clean empty lines
        data = self.remove_blanks(data)

        dataset = self.create_dataset(input_format, data)

        result = resource.import_data(dataset, dry_run=True,
                                      raise_errors=False,
                                      file_name=import_file.name,
                                      user=self.request.user)
        context['result'] = result

        if not result.has_errors():
                        
            context['confirm_form'] = self.confirm_form_class(initial={
                'import_file_name': tmp_storage.name,
                'original_file_name': import_file.name,
                'input_format': form.cleaned_data['input_format'],
            })
        return self.render_to_response(self.get_context_data(
            form=form,
            fields=[f.column_name for f in resource.get_fields()],
            **context))


    def process_import(self, confirm_form):
        """ This bit reproduces ImportMixin.process_import
        """

        resource = self.get_import_resource_class()()
        import_formats = self.get_import_formats()
        input_format = import_formats[
            int(confirm_form.cleaned_data['input_format'])
        ]()
        tmp_storage = self.get_tmp_storage_class()(
            name=confirm_form.cleaned_data['import_file_name'])
        data = tmp_storage.read(input_format.get_read_mode())
        if not input_format.is_binary() and self.from_encoding:
            data = force_str(data, self.from_encoding)
        
        # Clean empty lines
        data = self.remove_blanks(data)

        dataset = self.create_dataset(input_format, data)

        resource.import_data(
            dataset, dry_run=False, raise_errors=True,
            file_name=confirm_form.cleaned_data['original_file_name'],
            user=self.request.user)
        
        tmp_storage.remove()

        return HttpResponseRedirect(self.get_success_url())



class ExportView(FormView):

    formats = base_formats.DEFAULT_FORMATS
    resource_class = None
    model = None
    form_class = ExportForm


    def get_resource_class(self):
        if not self.resource_class:
            return modelresource_factory(self.model)
        return self.resource_class

    def get_resource_kwargs(self, request, *args, **kwargs):
        return {}   

    def get_export_formats(self):
        """
        Returns available export formats.
        """
        return [f for f in self.formats if f().can_export()]

    def get_export_resource_class(self):
        """
        Returns ResourceClass to use for export.
        """
        return self.get_resource_class()

    def get_export_resource_kwargs(self, request, *args, **kwargs):
        return self.get_resource_kwargs(request, *args, **kwargs)

    def get_data_for_export(self, request, queryset, *args, **kwargs):
        resource_class = self.get_export_resource_class()
        return resource_class(**self.get_export_resource_kwargs(request, *args, **kwargs))\
            .export(queryset, *args, **kwargs)

    def get_export_filename(self, file_format):
        date_str = now().strftime('%Y-%m-%d')
        filename = "%s-%s.%s" % (self.model.__name__,
                                 date_str,
                                 file_format.get_extension())
        return filename

    def get_export_data(self, file_format, queryset, *args, **kwargs):
        """
        Returns file_format representation for given queryset.
        """
        data = self.get_data_for_export(self.request, queryset, *args, **kwargs)
        export_data = file_format.export_data(data)
        return export_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['formats'] = self.get_export_formats()
        return kwargs

    def form_valid(self, form):
        formats = self.get_export_formats()
        file_format = formats[
            int(form.cleaned_data['file_format'])
        ]()

        queryset = self.get_queryset()
        export_data = self.get_export_data(file_format, queryset)
        content_type = file_format.get_content_type()
        
        response = HttpResponse(export_data, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="%s"' % (
            self.get_export_filename(file_format),
        )

        return response