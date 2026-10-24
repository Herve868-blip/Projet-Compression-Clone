# -*- coding: utf-8 -*-
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count):
        if self._pageNumber == 1:
            return
        self.saveState()
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#475569'))
        self.drawString(54, 800, "EXAMEN : CLONES BZIP2, LZMA ET 7-ZIP — RAPPORT D'EFFICACITE")
        self.drawRightString(541, 800, "OCTOBRE 2026")
        self.setStrokeColor(colors.HexColor('#cbd5e1'))
        self.setLineWidth(0.5)
        self.line(54, 793, 541, 793)
        self.line(54, 45, 541, 45)
        self.drawString(54, 32, "Destinataire : lucsarobidynomenjanahary@gmail.com | Mr Sarobidy")
        self.drawRightString(541, 32, f"Page {self._pageNumber} / {page_count}")
        self.restoreState()

def get_report_styles():
    base = getSampleStyleSheet()
    p_blue = colors.HexColor('#1e3a8a')
    s_blue = colors.HexColor('#0284c7')
    dark = colors.HexColor('#0f172a')
    return {
        'title': ParagraphStyle('DocTitle', parent=base['Heading1'], fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=p_blue, alignment=1, spaceAfter=12),
        'sub': ParagraphStyle('DocSub', parent=base['Normal'], fontName='Helvetica', fontSize=11, leading=15, textColor=s_blue, alignment=1, spaceAfter=20),
        'h1': ParagraphStyle('H1', parent=base['Heading1'], fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=p_blue, spaceBefore=14, spaceAfter=6, keepWithNext=True),
        'h2': ParagraphStyle('H2', parent=base['Heading2'], fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=s_blue, spaceBefore=9, spaceAfter=4, keepWithNext=True),
        'body': ParagraphStyle('Body', parent=base['Normal'], fontName='Helvetica', fontSize=8.8, leading=12.5, textColor=dark, spaceAfter=4),
        'callout': ParagraphStyle('Callout', parent=base['Normal'], fontName='Helvetica-Oblique', fontSize=8.5, leading=12, textColor=colors.HexColor('#1e293b')),
        'code': ParagraphStyle('Code', parent=base['Code'], fontName='Courier', fontSize=7.8, leading=9.8, textColor=dark),
        'p_blue': p_blue,
        's_blue': s_blue,
        'dark': dark,
        'bg_light': colors.HexColor('#f8fafc'),
    }
