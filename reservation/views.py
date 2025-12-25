# reservation/views.py - WERSJA 2: Function-based view
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .forms import ContactForm
from pets.models import Dog


def reservation_form_view(request):
    """
    Formularz kontaktowy/rezerwacyjny z wysyłką emaila
    WERSJA 2: Function-based (prostsza, bardziej explicitna)
    """

    if request.method == 'POST':
        # Przetwarzanie wysłanego formularza
        form = ContactForm(request.POST)

        if form.is_valid():
            # Pobierz dane z formularza
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            dog = form.cleaned_data.get('dog')  # Może być None
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Przygotuj nazwę psa jeśli wybrano
            dog_info = ''
            if dog:
                dog_info = f"\nZainteresowanie psem: {dog.name} (ID: {dog.id})"

            # Przygotuj treść emaila
            subject_choices = {
                'reservation': 'Rezerwacja szczeniaka',
                'info': 'Pytanie o hodowlę',
                'visit': 'Umówienie wizyty',
                'other': 'Inne',
            }
            subject_display = subject_choices.get(subject, subject)

            email_body = f"""
Nowa wiadomość z formularza kontaktowego Costa Rizada:

========================================
DANE KONTAKTOWE:
========================================
Imię i nazwisko: {name}
Email: {email}
Telefon: {phone}

========================================
TEMAT WIADOMOŚCI:
========================================
{subject_display}{dog_info}

========================================
TREŚĆ WIADOMOŚCI:
========================================
{message}

========================================
Dodatkowe informacje:
User Agent: {request.META.get('HTTP_USER_AGENT', 'Nieznane')}
IP: {get_client_ip(request)}
"""

            # Wyślij email
            try:
                send_mail(
                    subject=f'[Costa Rizada] {subject_display}',
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )

                # Opcjonalnie: Wyślij potwierdzenie do użytkownika
                send_confirmation_email(email, name)

                # Pokaż sukces
                messages.success(
                    request,
                    'Dziękujemy za wiadomość! Odpowiemy w ciągu 24-48 godzin.'
                )

                # Przekieruj na tę samą stronę (POST-REDIRECT-GET pattern)
                return redirect('rezerwacja:reservation-form')  # ← ZMIENIONE!

            except Exception as e:
                # Błąd wysyłki
                messages.error(
                    request,
                    'Wystąpił błąd przy wysyłaniu wiadomości. '
                    'Prosimy o kontakt telefoniczny: +48 123 456 789'
                )
                print(f"Email error: {e}")  # Log do konsoli/logów

        else:
            # Formularz ma błędy
            messages.error(
                request,
                'Formularz zawiera błędy. Proszę je poprawić i spróbować ponownie.'
            )

    else:
        # GET request - pokaż pusty formularz
        form = ContactForm()

    # Renderuj szablon z formularzem
    context = {
        'form': form,
    }

    return render(request, 'reservation/reservation.html', context)


def get_client_ip(request):
    """Pomocnicza funkcja - pobierz IP użytkownika"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_confirmation_email(user_email, user_name):
    """Opcjonalnie: Wyślij potwierdzenie do użytkownika"""
    try:
        send_mail(
            subject='Potwierdzenie - Twoja wiadomość do Costa Rizada',
            message=f"""
Witaj {user_name}!

Dziękujemy za kontakt z hodowlą Costa Rizada.

Otrzymaliśmy Twoją wiadomość i odpowiemy na nią w ciągu 24-48 godzin roboczych.

Jeśli sprawa jest pilna, zachęcamy do kontaktu telefonicznego:
+48 123 456 789 (Pn-Pt: 9:00-18:00)

Pozdrawiamy,
Zespół Costa Rizada
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=True,
        )
    except:
        pass