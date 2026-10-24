# -*- coding: utf-8 -*-
import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from src.report.styles import get_report_styles, NumberedCanvas
from src.report.sections_intro import add_cover, add_toc_intro, add_architecture_and_algos
from src.report.sections_benchmark import add_datasets_and_results, add_charts_and_screenshots
from src.report.sections_conclusion import add_gui_and_conclusion

def build_pdf_report(output_pdf: str = "dist/Rapport_Projet_Compression_Sarobidy.pdf",
                     results_json: str = "src/benchmark/benchmark_results.json") -> str:
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    if os.path.exists(results_json):
        with open(results_json, 'r', encoding='utf-8') as f:
            bench_data = json.load(f)
    else:
        bench_data = {}

    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    st = get_report_styles()
    story = []

    # Construction ordonnee des sections
    add_cover(story, st)
    add_toc_intro(story, st)
    add_architecture_and_algos(story, st)
    add_datasets_and_results(story, st, bench_data)
    add_charts_and_screenshots(story, st)
    add_gui_and_conclusion(story, st)

    doc.build(story, canvasmaker=NumberedCanvas)
    return output_pdf
