from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def SendUserEmail(
    request,
    user,
    template_name,
    mail_subject,
    to_email,
    token,
    description,
    title,
    password,
):
    use_https = False
    current_site = get_current_site(request)
    site_name = current_site.name
    context = {
        "domain": current_site.domain,
        "site_name": site_name,
        "protocol": "https" if use_https else "http",
        "user": user,
        "token": token if token else "",
        "description": description if description else "",
        "title": title if title else "",
    }
    message = render_to_string(str(template_name), context)
    email_message = EmailMultiAlternatives(
        mail_subject, message, settings.EMAIL_HOST_USER, [to_email]
    )
    html_email = render_to_string(str(template_name), context)
    email_message.attach_alternative(html_email, "text/html")
    status = email_message.send()
    return status


def get_pagination(request, data):
    page = request.GET.get("page", 1)
    paginator = Paginator(data, 10)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    except Exception:
        data = None
    return data
