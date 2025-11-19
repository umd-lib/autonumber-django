from django import forms

from autonumber.ui.models import AutoNumber, Name, Repository


class RepositoryForm(forms.ModelForm):
  class Meta:
    model = Repository
    fields = ['name']

  def clean_name(self):
    # name was forced to be lowercase in Rails
    name = self.cleaned_data['name'].lower()
    return name


class NameForm(forms.ModelForm):
  class Meta:
    model = Name
    fields = ['initials']


class BatchForm(forms.Form):
  quantity = forms.IntegerField(min_value=1, required=True)
  entry_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
  name = forms.CharField(max_length=10, required=True)
  repository = forms.ModelChoiceField(
    # The queryset tells the dropdown what options to display
    queryset=Repository.objects.all(),
    required=True,
  )

  def clean_name_initials(self):
    data = self.cleaned_data.get('name')
    if data:
      return data.strip().lower()
    return data

  def clean_repository_name(self):
    data = self.cleaned_data.get('repository')
    if data:
      return data.strip().lower()
    return data


class AutoNumberForm(forms.ModelForm):
  class Meta:
    model = AutoNumber
    fields = ['entry_date', 'name', 'repository']

    widgets = {
      'entry_date': forms.DateInput(attrs={'type': 'date'}),
    }
