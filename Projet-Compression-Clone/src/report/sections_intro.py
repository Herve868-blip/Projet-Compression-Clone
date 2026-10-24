# -*- coding: utf-8 -*-
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import ParagraphStyle

def add_cover(story, st):
    p_blue = st['p_blue']
    s_blue = st['s_blue']
    dark = st['dark']
    bg_light = st['bg_light']

    story.append(Spacer(1, 30))
    story.append(Paragraph("PROJET D'EVALUATION EN COMPRESSION DE DONNEES", ParagraphStyle('TN', fontName='Helvetica-Bold', fontSize=11, textColor=s_blue, alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("CLONES FONCTIONNELS DES UTILITAIRES DE COMPRESSION", st['title']))
    story.append(Paragraph("<b>bzip2 (BWT) &bull; lzma (LZMA/XZ) &bull; 7-zip (LZMA2 / 7z)</b>", st['sub']))
    story.append(HRFlowable(width="85%", thickness=2, color=p_blue, spaceBefore=5, spaceAfter=15))
    story.append(Paragraph("<b>Etude comparative, architecture logicielle et demonstration d'efficacite sur 4 types de fichiers : Texte, Audio, Image et Video</b>", ParagraphStyle('DC', fontName='Helvetica', fontSize=10, leading=14, alignment=1, textColor=dark)))
    story.append(Spacer(1, 35))

    info = [
        [Paragraph("<b>Destinataire de l'evaluation :</b>", st['body']), Paragraph("<b>Mr Luc Sarobidy Nomenjanahary</b><br/>Email : <font color='#2563eb'><u>lucsarobidynomenjanahary@gmail.com</u></font>", st['body'])],
        [Paragraph("<b>Date limite de soumission :</b>", st['body']), Paragraph("<b>Samedi 24 octobre 2026 a 23h59</b>", st['body'])],
        [Paragraph("<b>Depot GitHub du code :</b>", st['body']), Paragraph("<font color='#2563eb'><u>https://github.com/tsiory-bainga/clone-compression-bzip2-lzma-7zip</u></font>", st['body'])],
        [Paragraph("<b>Livrables fournis :</b>", st['body']), Paragraph("1. Code source complet et executable (Python 3)<br/>2. Document PDF officiel avec captures d'ecran et graphiques<br/>3. Interface Graphique Desktop (GUI) et Scripts batch", st['body'])],
        [Paragraph("<b>Emplacement local :</b>", st['body']), Paragraph("<code>C:\\Users\\Adminlocal\\Desktop\\Projet-Compression-Clone</code>", st['code'])]
    ]
    t_info = Table(info, colWidths=[5.5 * cm, 11.5 * cm])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('BOX', (0,0), (-1,-1), 1.5, p_blue),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 45))
    story.append(Paragraph("<i>Session d'Evaluation Universitaire 2026</i>", ParagraphStyle('FT', fontName='Helvetica-Oblique', fontSize=9, alignment=1, textColor=colors.gray)))
    story.append(PageBreak())

def add_toc_intro(story, st):
    s_blue = st['s_blue']
    story.append(Paragraph("Table des Matieres", st['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=s_blue, spaceBefore=2, spaceAfter=10))
    toc = [
        [Paragraph("<b>1. Introduction et Cahier des Charges</b>", st['body']), Paragraph("Page 2", st['body'])],
        [Paragraph("<b>2. Architecture Technique des Clones Developpes</b>", st['body']), Paragraph("Page 3", st['body'])],
        [Paragraph("<b>3. Fondements Algorithmiques (BWT, MTF, LZMA, 7-Zip)</b>", st['body']), Paragraph("Page 4", st['body'])],
        [Paragraph("<b>4. Protocoles Experimentaux & Datasets (Texte, Audio, Image, Video)</b>", st['body']), Paragraph("Page 5", st['body'])],
        [Paragraph("<b>5. Resultats Experimentaux & Tableau des Metriques</b>", st['body']), Paragraph("Page 6", st['body'])],
        [Paragraph("<b>6. Graphiques Comparatifs d'Efficacite</b>", st['body']), Paragraph("Page 7", st['body'])],
        [Paragraph("<b>7. Captures d'Ecran Demontrant le Bon Fonctionnement</b>", st['body']), Paragraph("Page 9", st['body'])],
        [Paragraph("<b>8. Analyse Critique selon le Type de Donnees</b>", st['body']), Paragraph("Page 11", st['body'])],
        [Paragraph("<b>9. Manuel d'Utilisation (CLI, Batch et GUI)</b>", st['body']), Paragraph("Page 12", st['body'])],
        [Paragraph("<b>10. Conclusion & Transmission par Email</b>", st['body']), Paragraph("Page 12", st['body'])],
    ]
    t_toc = Table(toc, colWidths=[14 * cm, 3 * cm])
    t_toc.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#f1f5f9')), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_toc)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Introduction et Cahier des Charges", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=s_blue, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("Ce projet a pour objectif de concevoir un clone fonctionnel des trois utilitaires de compression majeurs : <b>bzip2</b>, <b>lzma</b> et <b>7-zip</b>. Le travail realise respecte rigoureusement les deux livrables attendus :", st['body']))
    story.append(Paragraph("&bull; <b>Livrable 1 :</b> Le code source complet et fonctionnel accessible via le depot GitHub, dont le lien est a transmettre par email a <code>lucsarobidynomenjanahary@gmail.com</code>.<br/>&bull; <b>Livrable 2 :</b> Un document PDF officiel integrant des captures d'ecran demontrant l'efficacite de la compression sur <b>quatre types de fichiers : texte, audio, image et video</b>.<br/>&bull; <b>Date limite de soumission :</b> Samedi 24 octobre 2026 a 23h59.", st['body']))
    story.append(Paragraph("Une suite de benchmark automatisee et une interface graphique ergonomique completent ces outils en ligne de commande pour faciliter leur verification et leur evaluation experimentale.", st['body']))
    story.append(PageBreak())

def add_architecture_and_algos(story, st):
    s_blue = st['s_blue']
    story.append(Paragraph("2. Architecture Technique des Clones Developpes", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=s_blue, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("L'architecture globale du projet est concue pour offrir une fidelite absolue avec les CLI originaux tout en etant extensible et modulaire :", st['body']))

    arch_data = [
        [Paragraph("<b>Composant</b>", st['body']), Paragraph("<b>Fichier Source</b>", st['body']), Paragraph("<b>Role et Conformite</b>", st['body'])],
        [Paragraph("<b>bzip2 Clone</b>", st['body']), Paragraph("<code>src/bzip2_clone.py</code>", st['code']), Paragraph("Clone fidele de GNU bzip2. Supporte <code>-c, -d, -z, -t, -f, -k, -s, -v, -1..-9</code>. Format conteneur standard <code>.bz2</code>.", st['body'])],
        [Paragraph("<b>lzma Clone</b>", st['body']), Paragraph("<code>src/lzma_clone.py</code>", st['code']), Paragraph("Clone fidele de l'utilitaire LZMA/XZ. Supporte <code>-z, -d, -t, -l, -k, -f, -0..-9, -F, -C</code>. Gere formats <code>.xz</code> et flux <code>.lzma</code>.", st['body'])],
        [Paragraph("<b>7-Zip Clone</b>", st['body']), Paragraph("<code>src/sevenzip_clone.py</code>", st['code']), Paragraph("Clone de la CLI Igor Pavlov (7z). Supporte les commandes <code>a, x, e, l, t, d, b</code> et commutateurs <code>-t, -mx, -m0, -p, -o, -y, -r</code>.", st['body'])],
        [Paragraph("<b>BWT Pedagogique</b>", st['body']), Paragraph("<code>src/core/bwt.py</code>", st['code']), Paragraph("Implementation pure de BWT (LF-mapping), Move-To-Front (MTF) et RLE a vocation didactique.", st['body'])],
        [Paragraph("<b>Metriques Coeur</b>", st['body']), Paragraph("<code>src/core/metrics.py</code>", st['code']), Paragraph("Calcul d'entropie de Shannon, debits MB/s, ratios %, gains d'espace et validation cryptographique SHA-256.", st['body'])],
        [Paragraph("<b>Benchmark Suite</b>", st['body']), Paragraph("<code>src/benchmark/</code>", st['code']), Paragraph("Generateur de datasets (Texte, Audio, Image, Video), execution de benchmark et extraction Matplotlib.", st['body'])],
        [Paragraph("<b>Interface Graphique</b>", st['body']), Paragraph("<code>src/gui/app.py</code>", st['code']), Paragraph("Interface Desktop moderne Tkinter avec visualisation temps reel des operations et onglets de graphiques.", st['body'])],
        [Paragraph("<b>Lanceur Principal</b>", st['body']), Paragraph("<code>main.py</code>", st['code']), Paragraph("Point d'entree unifie (<code>python main.py bzip2|lzma|7z|benchmark|gui|report</code>) double de scripts <code>.bat</code>.", st['body'])],
    ]
    t_arch = Table(arch_data, colWidths=[3.0 * cm, 4.2 * cm, 9.8 * cm])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Fondements Algorithmiques Comparatifs", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=s_blue, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("<b>3.1 bzip2 : Tri de Contexte par Blocs (BWT + MTF + Huffman)</b><br/>"
                           "bzip2 n'utilise pas de dictionnaire glissant mais transforme le flux d'octets en cinq etapes successives : RLE-1 -> BWT (tri cyclique par blocs 100k a 900k octets) -> Move-to-Front (MTF) -> RLE-2 -> Codage de Huffman canonique. La transformation BWT exploite la propriete <i>LF-Mapping</i> pour regrouper les contextes identiques sans modification de l'alphabet.<br/><br/>"
                           "<b>3.2 LZMA : Lempel-Ziv-Markov Chain Algorithm</b><br/>"
                           "LZMA ameliore l'approche LZ77 grace a un dictionnaire glissant etendu (jusqu'a 64 Mo) et remplace le codage Huffman par un codeur par intervalles binaire adaptatif (Range Coder) avec modelisation contextuelle Markovienne.<br/><br/>"
                           "<b>3.3 7-Zip : Architecture Conteneur & Algorithme LZMA2</b><br/>"
                           "7-Zip utilise LZMA2, decoupant le flux en blocs independants facilitant le multithreading et gerant intelligemment les donnees incompressibles, tout en fournissant l'archivage solide et le chiffrement AES-256.", st['body']))
    story.append(PageBreak())
