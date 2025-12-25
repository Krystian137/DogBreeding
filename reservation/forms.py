# reservation/forms.py (lub tam gdzie masz views.py)
from django import forms
from pets.models import Dog

class ContactForm(forms.Form):
    """Formularz kontaktowy/rezerwacyjny"""

    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Jan Kowalski',
            'class': 'form-control'
        }),
        label='Imię i nazwisko'
    )

    email = forms.EmailField(
        max_length=200,
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'jan.kowalski@example.com',
            'class': 'form-control'
        }),
        label='Email'
    )

    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '+48 123 456 789',
            'class': 'form-control'
        }),
        label='Telefon'
    )

    dog = forms.ModelChoiceField(
        queryset=Dog.objects.none(),  # Ustawi się w __init__
        required=False,
        empty_label='-- Wybierz psa lub pozostaw puste --',
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Zainteresowanie szczeniakiem'
    )

    SUBJECT_CHOICES = [
        ('', '-- Wybierz temat --'),
        ('reservation', 'Rezerwacja szczeniaka'),
        ('info', 'Pytanie o hodowlę'),
        ('visit', 'Umówienie wizyty'),
        ('other', 'Inne'),
    ]

    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Temat'
    )

    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Proszę opisać swoje zainteresowanie, pytania lub uwagi...',
            'class': 'form-control',
            'rows': 6
        }),
        label='Wiadomość'
    )

    consent = forms.BooleanField(
        required=True,
        label='Wyrażam zgodę na przetwarzanie moich danych osobowych',
        error_messages={
            'required': 'Musisz wyrazić zgodę na przetwarzanie danych osobowych.'
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ustawienie dostępnych psów
        self.fields['dog'].queryset = Dog.objects.filter(
            status__in=['available', 'reserved']
        ).order_by('name')

    def clean_phone(self):
        """Walidacja numeru telefonu"""
        phone = self.cleaned_data.get('phone')
        # Usuń spacje i myślniki
        phone_digits = ''.join(filter(str.isdigit, phone))

        if len(phone_digits) < 9:
            raise forms.ValidationError('Numer telefonu jest za krótki.')

        return phone