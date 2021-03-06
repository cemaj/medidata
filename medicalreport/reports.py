import os
import xhtml2pdf.pisa as pisa
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.template.loader import get_template
from services.xml.base64_attachment import Base64Attachment
from services.emisapiservices import services
import reportlab
import reportlab.lib.pagesizes as pdf_sizes
from PIL import Image
from django.conf import settings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = BASE_DIR + '/medicalreport/templates/medicalreport/reports/medicalreport.html'


def link_callback(uri, rel):
    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT

    if uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))

    path = BASE_DIR + '/medi/' + path

    if not os.path.isfile(path):
        raise Exception('static URI must start with %s' % (sUrl))
    return path


class MedicalReport:

    @staticmethod
    def render(params: dict):
        template = get_template(REPORT_DIR)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, link_callback=link_callback)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)

    @staticmethod
    def download(params: dict):
        template = get_template(REPORT_DIR)
        html = template.render(params)
        file = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), file, link_callback=link_callback)

        if not pdf.err:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            response.write(file.getvalue())
            return response

    @staticmethod
    def get_pdf_file(params: dict):
        template = get_template(REPORT_DIR)
        html = template.render(params)
        file = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), file, link_callback=link_callback)
        if not pdf.err:
            return ContentFile(file.getvalue())


class AttachmentReport:
    def __init__(self, instruction: object, path_file: str):
        self.raw_xml = services.GetAttachment(instruction.patient.emis_number,path_file).call()
        self.file_name = Base64Attachment(self.raw_xml).filename()
        self.file_type = self.file_name.split('.')[-1]

    def render(self):
        if self.file_type == "pdf":
            return self.render_pdf()
        else:
            return self.render_image()

    def render_pdf(self):
        attachment = Base64Attachment(self.raw_xml).data()
        buffer = BytesIO()
        buffer.write(attachment)
        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/pdf",
        )
        return response

    def render_image(self):
        attachment = Base64Attachment(self.raw_xml).data()
        image = Image.open(BytesIO(attachment))
        image_format = image.format
        if image_format == "TIFF":
            return self.render_pdf_with_tiff(image)
        extension = str(image_format)
        response = HttpResponse(content_type="image/" + extension.lower())
        image.save(response, image_format)
        return response

    def render_pdf_with_tiff(self, image, max_pages = 200):
        height = image.tag[0x101][0]
        width = image.tag[0x100][0]
        out_pdf_io = BytesIO()
        c = reportlab.pdfgen.canvas.Canvas(out_pdf_io, pagesize=pdf_sizes.letter)
        pdf_width, pdf_height = pdf_sizes.letter
        page = 0
        while True:
            try:
                image.seek(page)
            except EOFError:
                break
            if pdf_width * height / width <= pdf_height:
                c.drawInlineImage(image, 0, 0, pdf_width, pdf_width * height / width)
            else:
                c.drawInlineImage(image, 0, 0, pdf_height * width / height, pdf_height)
            c.showPage()
            if max_pages and page > max_pages:
              break
            page += 1
        c.save()
        response = HttpResponse(
            out_pdf_io.getvalue(),
            content_type="application/pdf",
        )
        return response
