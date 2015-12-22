from django.http import Http404
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from apps.contact.forms import ContactForm


def home(request):
    contact_form = ContactForm()
    return render(request, 'pages/home.html', {'form': contact_form})


def project(request, project_name):
    template_path = 'projects/modals/' + project_name + '.html'
    try:
        get_template(template_path)
    except TemplateDoesNotExist:
        raise Http404

    return render(request, template_path)
