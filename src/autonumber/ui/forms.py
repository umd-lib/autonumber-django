from django import forms

from autonumber.ui.models import AutoNumber, CollectionArea


class CollectionAreaForm(forms.ModelForm):
  class Meta:
    model = CollectionArea
    fields = ['name']

  def clean_name(self):
    # name was forced to be lowercase in Rails
    name = self.cleaned_data['name'].lower()
    return name


class BatchForm(forms.Form):
  quantity = forms.IntegerField(min_value=1, required=True)
  entry_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
  collection_area = forms.ModelChoiceField(
    # The queryset tells the dropdown what options to display
    queryset=CollectionArea.objects.all(),
    required=True,
  )

  def clean_name_initials(self):
    data = self.cleaned_data.get('name')
    if data:
      return data.strip().lower()
    return data

  def clean_collection_area_name(self):
    data = self.cleaned_data.get('collection_area')
    if data:
      return data.strip().lower()
    return data


class AutoNumberForm(forms.ModelForm):
  class Meta:
    model = AutoNumber
    fields = ['entry_date', 'collection_area']

    widgets = {
      'entry_date': forms.DateInput(attrs={'type': 'date'}),
    }
