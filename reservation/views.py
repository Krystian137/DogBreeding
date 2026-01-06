# reservation/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from .forms import ContactForm

class FAQ(TemplateView):
    template_name = 'reservation/FAQ.html'

def reservation_form_view(request):
    """
    Contact/reservation form with email sending
    """

    if request.method == 'POST':
        # Process submitted form
        form = ContactForm(request.POST)

        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Prepare subject display name
            subject_choices = {
                'reservation': 'Rezerwacja szczeniaka',
                'info': 'Pytanie o hodowlę',
                'visit': 'Umówienie wizyty',
                'other': 'Inne',
            }
            subject_display = subject_choices.get(subject, subject)

            # Prepare email body
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
{subject_display}

========================================
TREŚĆ WIADOMOŚCI:
========================================
{message}

========================================
Dodatkowe informacje:
User Agent: {request.META.get('HTTP_USER_AGENT', 'Nieznane')}
IP: {get_client_ip(request)}
"""

            # Send email
            try:
                send_mail(
                    subject=f'[Costa Rizada] {subject_display}',
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )

                # Optional: Send confirmation to user
                send_confirmation_email(email, name)

                # Show success message
                messages.success(
                    request,
                    'Dziękujemy za wiadomość! Odpowiemy w ciągu 24-48 godzin.'
                )

                # Redirect (POST-REDIRECT-GET pattern)
                return redirect('rezerwacja:reservation-form')

            except Exception as e:
                # Email sending error
                messages.error(
                    request,
                    'Wystąpił błąd przy wysyłaniu wiadomości. '
                    'Prosimy o kontakt telefoniczny: +48 123 456 789'
                )
                print(f"Email error: {e}")  # Log to console

        else:
            # Form has errors
            messages.error(
                request,
                'Formularz zawiera błędy. Proszę je poprawić i spróbować ponownie.'
            )

    else:
        # GET request - show empty form
        form = ContactForm()

    # Render template with form
    context = {
        'form': form,
    }

    return render(request, 'reservation/reservation.html', context)


def get_client_ip(request):
    """Helper function - get user's IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_confirmation_email(user_email, user_name):
    """Optional: Send confirmation to user"""
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