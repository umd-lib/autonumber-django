from django import forms

from autonumber.ui.models import AutoNumber, CollectingArea


class CollectingAreaForm(forms.ModelForm):
  class Meta:
    model = CollectingArea
    fields = ['name']

  def clean_name(self):
    # name was forced to be lowercase in Rails
    name = self.cleaned_data['name'].lower()
    return name


class BatchForm(forms.Form):
  quantity = forms.IntegerField(min_value=1, required=True)
  entry_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
  collecting_area = forms.ModelChoiceField(
    # The queryset tells the dropdown what options to display
    queryset=CollectingArea.objects.all(),
    required=True,
  )

  def clean_name_initials(self):
    data = self.cleaned_data.get('name')
    if data:
      return data.strip().lower()
    return data

  def clean_collecting_area_name(self):
    data = self.cleaned_data.get('collecting_area')
    if data:
      return data.strip().lower()
    return data


class AutoNumberForm(forms.ModelForm):
  class Meta:
    model = AutoNumber
    fields = ['entry_date', 'collecting_area']

    widgets = {
      'entry_date': forms.DateInput(attrs={'type': 'date'}),
    }
