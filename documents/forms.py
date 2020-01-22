from django import forms

from .models import Document, DocumentType
from materials.models import Material, Batch

class MaterialNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class MaterialCodeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.code

class DocumentForm(forms.Form):
    document_type = forms.ModelChoiceField(
        queryset=DocumentType.objects.all(),
        empty_label=None)
    batch_code = forms.CharField(max_length=100, required=False)
    material_id = forms.CharField(required=True, widget=forms.HiddenInput())
    file_id = forms.CharField(required=True, widget=forms.HiddenInput())

    def clean(self):
        cd = super(DocumentForm, self).clean()
        document_type = DocumentType.objects.get(pk=cd['document_type'].id)
        if document_type.level == 'batch':
            if 'batch_code' not in cd or cd['batch_code'] == None or \
                cd['batch_code'] == '':
                self.add_error('batch_code', 'Please enter a batch code.')
        return cd