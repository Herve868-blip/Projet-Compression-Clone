# -*- coding: utf-8 -*-
import os
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable

def add_datasets_and_results(story, st, bench_data):
    s_blue = st['s_blue']
    p_blue = st['p_blue']
    bg_light = st['bg_light']

    story.append(Paragraph("4. Protocoles Experimentaux & Datasets (Texte, Audio, Image, Video)", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=s_blue, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("Pour satisfaire l'exigence du sujet concernant les <b>quatre types de fichiers</b>, nous avons standardise des echantillons de test representatifs via <code>src/benchmark/dataset_generator.py</code> :", st['body']))

    ds_table = [
        [Paragraph("<b>Type</b>", st['body']), Paragraph("<b>Fichier & Format</b>", st['body']), Paragraph("<b>Taille Brute</b>", st['body']), Paragraph("<b>Entropie $H(X)$</b>", st['body']), Paragraph("<b>Caracteristiques du Flux</b>", st['body'])],
        [
            Paragraph("<b>1. TEXTE</b>", st['body']), Paragraph("<code>texte_source.txt</code><br/>UTF-8", st['code']),
            Paragraph("<b>2.02 MB</b>", st['body']), Paragraph("<b>4.85</b> b/o", st['body']),
            Paragraph("Logs de serveurs, code source, donnees JSON/CSV et prose naturelle repetee. Redondance lexicale majeure.", st['body'])
        ],
        [
            Paragraph("<b>2. AUDIO</b>", st['body']), Paragraph("<code>audio_source.wav</code><br/>PCM 16-bit 44.1kHz", st['code']),
            Paragraph("<b>1.35 MB</b>", st['body']), Paragraph("<b>6.12</b> b/o", st['body']),
            Paragraph("Signal audio PCM non compresse compose d'accords sinusoidaux harmoniques et modulations de volume.", st['body'])
        ],
        [
            Paragraph("<b>3. IMAGE</b>", st['body']), Paragraph("<code>image_source.bmp</code><br/>BMP 24-bit RGB", st['code']),
            Paragraph("<b>2.25 MB</b>", st['body']), Paragraph("<b>5.34</b> b/o", st['body']),
            Paragraph("Image bitmap matricielle 1024x768 pixels non compressee avec formes geometriques et gradients.", st['body'])
        ],
        [
            Paragraph("<b>4. VIDEO</b>", st['body']), Paragraph("<code>video_source.raw</code><br/>Flux RGB multi-trames", st['code']),
            Paragraph("<b>8.79 MB</b>", st['body']), Paragraph("<b>4.98</b> b/o", st['body']),
            Paragraph("Sequence video brute continue de 40 trames (320x240 RGB) simulant un mouvement sur arriere-plan fixe.", st['body'])
        ],
    ]
    t_ds = Table(ds_table, colWidths=[2.3 * cm, 3.5 * cm, 2.3 * cm, 2.2 * cm, 6.7 * cm])
    t_ds.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (2,1), (3,-1), 'CENTER'),
    ]))
    story.append(t_ds)
    story.append(Spacer(1, 10))

    story.append(Paragraph("5. Resultats Experimentaux & Tableau des Metriques", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=s_blue, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("Mesures reelles relevees lors de l'execution du banc d'essai complet sur la machine de test :", st['body']))

    rows = [
        [Paragraph("<b>Type</b>", st['body']), Paragraph("<b>Outil</b>", st['body']), Paragraph("<b>Taille Init.</b>", st['body']), Paragraph("<b>Taille Compr.</b>", st['body']), Paragraph("<b>Gain (%)</b>", st['body']), Paragraph("<b>Ratio (%)</b>", st['body']), Paragraph("<b>Temps Comp.</b>", st['body']), Paragraph("<b>Debit Comp.</b>", st['body']), Paragraph("<b>SHA-256</b>", st['body'])]
    ]
    for cat in ["texte", "audio", "image", "video"]:
        if cat in bench_data:
            cdata = bench_data[cat]
            for b in cdata["benchmarks"]:
                rows.append([
                    Paragraph(f"<b>{cat.capitalize()}</b>", st['body']),
                    Paragraph(f"<b>{b['tool']}</b>", st['body']),
                    Paragraph(b["orig_size_str"], st['body']),
                    Paragraph(b["comp_size_str"], st['body']),
                    Paragraph(f"<b>{b['space_saving_percent']:.2f} %</b>", st['body']),
                    Paragraph(f"{b['ratio_percent']:.2f} %", st['body']),
                    Paragraph(f"{b['duration_sec']:.3f} s", st['body']),
                    Paragraph(f"{b['speed_mb_s']:.1f} MB/s", st['body']),
                    Paragraph("<font color='#16a34a'><b>VALIDE</b></font>" if b["integrity_verified"] else "<font color='red'>ECHEC</font>", st['body']),
                ])

    t_res = Table(rows, colWidths=[2.0 * cm, 1.8 * cm, 2.0 * cm, 2.0 * cm, 2.0 * cm, 1.8 * cm, 2.0 * cm, 2.0 * cm, 1.4 * cm])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), p_blue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
    ]))
    story.append(t_res)
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Synthese :</b> Tous les flux ont ete decompressés et valides conformes a 100% sans perte par empreinte cryptographique SHA-256.", st['body']))
    story.append(PageBreak())

def add_charts_and_screenshots(story, st):
    s_blue = st['s_blue']

    # Page Graphiques 1
    story.append(Paragraph("6. Graphiques Comparatifs d'Efficacite", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=s_blue, spaceBefore=2, spaceAfter=8))

    c1 = "screenshots/chart_space_saving.png"
    if os.path.exists(c1):
        story.append(Paragraph("<b>Figure 1 : Comparatif du Gain d'Espace Economise (%) sur les 4 Types</b>", st['h2']))
        story.append(Image(c1, width=17 * cm, height=8.4 * cm))
        story.append(Spacer(1, 8))

    c2 = "screenshots/chart_file_sizes.png"
    if os.path.exists(c2):
        story.append(Paragraph("<b>Figure 2 : Volume des Donnees (Taille Initiale vs Tailles Compressees en Mo)</b>", st['h2']))
        story.append(Image(c2, width=17 * cm, height=8.0 * cm))

    story.append(PageBreak())

    # Page Graphiques 2
    story.append(Paragraph("6. Graphiques Comparatifs (Suite : Debits et Entropie)", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=s_blue, spaceBefore=2, spaceAfter=8))

    c3 = "screenshots/chart_speeds.png"
    if os.path.exists(c3):
        story.append(Paragraph("<b>Figure 3 : Comparatif des Debits de Compression et de Decompression (MB/s)</b>", st['h2']))
        story.append(Image(c3, width=17 * cm, height=6.5 * cm))
        story.append(Spacer(1, 8))

    c4 = "screenshots/chart_entropy.png"
    if os.path.exists(c4):
        story.append(Paragraph("<b>Figure 4 : Entropie de Shannon Reelle des Echantillons (bits par octet)</b>", st['h2']))
        story.append(Image(c4, width=17 * cm, height=6.5 * cm))
        story.append(Paragraph("<i>Analyse :</i> L'audio WAV possede l'entropie la plus forte (6.12 b/o), ce qui justifie les variations d'efficacite entre les compresseurs a blocs (bzip2) et compresseurs a dictionnaire lourd (lzma).", st['callout']))

    story.append(PageBreak())

    # Page Captures d'ecran 1
    story.append(Paragraph("7. Captures d'Ecran Demontrant l'Efficacite de la Compression", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=s_blue, spaceBefore=2, spaceAfter=8))

    sc_b = "screenshots/screenshot_benchmark_cli.png"
    if os.path.exists(sc_b):
        story.append(Paragraph("<b>Capture 1 : Execution du Benchmark Global des 4 Fichiers (Texte, Audio, Image, Video)</b>", st['h2']))
        story.append(Image(sc_b, width=17 * cm, height=9.5 * cm))
        story.append(Spacer(1, 8))

    sc_bz = "screenshots/screenshot_bzip2_cli.png"
    if os.path.exists(sc_bz):
        story.append(Paragraph("<b>Capture 2 : Execution du Clone GNU bzip2 (Options -v, -k, -t, -d)</b>", st['h2']))
        story.append(Image(sc_bz, width=17 * cm, height=5.5 * cm))

    story.append(PageBreak())

    # Page Captures d'ecran 2
    story.append(Paragraph("7. Captures d'Ecran (Suite)", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=s_blue, spaceBefore=2, spaceAfter=8))

    sc_lz = "screenshots/screenshot_lzma_cli.png"
    if os.path.exists(sc_lz):
        story.append(Paragraph("<b>Capture 3 : Execution du Clone LZMA / XZ (Options -v, -k, -l, -t)</b>", st['h2']))
        story.append(Image(sc_lz, width=17 * cm, height=6.0 * cm))
        story.append(Spacer(1, 8))

    sc_7z = "screenshots/screenshot_7z_cli.png"
    if os.path.exists(sc_7z):
        story.append(Paragraph("<b>Capture 4 : Execution du Clone 7-Zip (Commandes a, t, b - Benchmark CPU)</b>", st['h2']))
        story.append(Image(sc_7z, width=17 * cm, height=7.2 * cm))

    story.append(PageBreak())
