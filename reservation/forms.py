# reservation/forms.py
from django import forms

class ContactForm(forms.Form):
    """Contact and reservation form"""

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

    def clean_phone(self):
        """Phone number validation"""
        phone = self.cleaned_data.get('phone')
        # Remove spaces and dashes
        phone_digits = ''.join(filter(str.isdigit, phone))

        if len(phone_digits) < 9:
            raise forms.ValidationError('Numer telefonu jest za krótki.')

        return phone