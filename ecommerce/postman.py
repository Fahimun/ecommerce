from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_email(subject, to_email, template_name, context, file_paths=None):
    try:
        # Render the HTML template
        html_template = render_to_string(template_name, context)
        plain_text = strip_tags(html_template)  # HTML থেকে প্লেইন টেক্সট বের করা

        # ইমেইল পাঠানোর জন্য কনফিগারেশন
        from_email = settings.DEFAULT_FROM_EMAIL
        # Email বানানো
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_text,  # ফাঁকা না রেখে প্লেইন টেক্সট দেওয়া হলো
            from_email=from_email,
            to=[to_email] if isinstance(to_email, str) else to_email  # যদি একাধিক রিসিপিয়েন্ট থাকে
        )

        # Attach HTML content
        email.attach_alternative(html_template, "text/html")

        # Attach files (যদি থাকে)
        if file_paths:
            for file_path in file_paths:
                email.attach_file(file_path)

        # ইমেইল পাঠানো
        email.send()

        return {
            "status": "sent",
            "message": "Email sent successfully"
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": str(e)
        }