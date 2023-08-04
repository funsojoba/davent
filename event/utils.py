import io
import os
import uuid
import pdfkit
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
from django.template.loader import render_to_string

from helpers.event_ticket import download_as_pdf_view
from event.service import EventService

from xhtml2pdf import pisa 


def generate_pdf(context):
    
    template_path = 'ticket_pdf.html'

    response = HttpResponse(content_type='application/pdf')
    file_name = f"{uuid.uuid4().hex}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    html = render_to_string(template_path, context)

    pisaStatus = pisa.CreatePDF(html, dest=response, getSize=100)
    return response 




#NOTE: Not working
def download_as_pdf_view(context, template_path):
    # create PDF from HTML template file with context.
    # invoice = Invoice.objects.get(pk=pk)
    _html = render_to_string(template_path, context)
    # remove header
    _html = _html[_html.find("<body>") :]

    # create new header
    new_header = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8"/>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100;200;500&display=swap" rel="stylesheet">
    </head>
    <style>
        @font-face {
        font-family: Recoleta;
        src:local("Recoleta-RegularDEMO.otf");
        src:local(f'os.path.join(settings.BASE_DIR, "ticket.css")')
    }
    """
    # add style from css file. please change to your css file path.
    css_path = os.path.join(settings.BASE_DIR, "ticket.css")
    with open(css_path, "r") as f:
        new_header += f.read()
    new_header += "\n</style>"

    # add head to html
    _html = new_header + _html[_html.find("<body>") :]

    # convert html to pdf
    file_name = f"{uuid.uuid4().hex}.pdf"
    pdf_path = os.path.join(settings.BASE_DIR, "static", "pdf", file_name)
    pdfkit.from_string(
        _html, pdf_path, options={"enable-local-file-access": "", "no-xserver": ""}
    )
    pdf_file = open(pdf_path, "rb")
    return pdf_file