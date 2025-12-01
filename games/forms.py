from django import forms
from .models import Game

class NewGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['room_name']
        widgets = {
            'room_name': forms.TextInput(attrs={'placeholder': 'Nombre de la sala (único)'})
        }

    def clean_room_name(self):
        rn = self.cleaned_data['room_name'].strip()
        if Game.objects.filter(room_name__iexact=rn).exists():
            raise forms.ValidationError("Ya existe una sala con ese nombre.")
        return rn
