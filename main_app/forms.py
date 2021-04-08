from django import forms

from main_app.models import Movie, Tag


class MovieNoteForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'placeholder': 'Notatka', 'class': "form-control"}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nazwa', 'class': "form-control"}),
        }


class SearchForm(forms.Form):
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'placeholder': 'Film/Tag', 'class': 'form-control me-2'}))
