# -*- coding: utf-8 -*-
import os
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable

def add_gui_and_conclusion(story, st):
    s_blue = st['s_blue']
    p_blue = st['p_blue']
    bg_light = st['bg_light']

    # Page GUI & Analyse critique
    story.append(Paragraph("7. Capture de l'Interface Graphique Desktop (GUI)", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=s_blue, spaceBefore=2, spaceAfter=8))

    sc_g = "screenshots/screenshot_gui_app.png"
    if os.path.exists(sc_g):
        story.append(Paragraph("<b>Capture 5 : Interface Graphique Interactive de la Suite de Compression</b>", st['h2']))
        story.append(Image(sc_g, width=17 * cm, height=10.5 * cm))
        story.append(Spacer(1, 8))

    story.append(Paragraph("8. Analyse Critique selon le Type de Donnees", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=s_blue, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "&bull; <b>Fichiers Texte :</b> Le codage par blocs BWT est parfait pour regrouper les contextes lexicaux rapproches, mais LZMA parvient a referencer des structures recurrentes grace a son dictionnaire 64 Mo.<br/>"
        "&bull; <b>Fichiers Audio PCM :</b> La correlation sinusoidale est difficilement traitable par BWT qui disperse les echantillons discrets dans la matrice. LZMA capture en revanche la periodicite des ondes sonores.<br/>"
        "&bull; <b>Images et Videos :</b> Les aplats de fond et les zones statiques entre trames consecutives produisent des gains exceptionnels (>97% a 99%), attestant de l'efficacite remarquable des algorithmes.",
        st['body']
    ))
    story.append(PageBreak())

    # Page Manuel & Email
    story.append(Paragraph("9. Manuel d'Utilisation Rapide (CLI & GUI)", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=s_blue, spaceBefore=2, spaceAfter=8))

    cmd_box = [
        [Paragraph(
            "<b># 1. Utilitaire bzip2 :</b><br/>"
            "python main.py bzip2 -v -k -9 fichier.txt         # Compresse avec ratio detaille<br/>"
            "python main.py bzip2 -d -k fichier.txt.bz2        # Decompresse sans supprimer l'archive<br/>"
            "python main.py bzip2 -t -v fichier.txt.bz2        # Verifie l'integrite CRC<br/><br/>"
            "<b># 2. Utilitaire lzma / xz :</b><br/>"
            "python main.py lzma -v -k -9 --check=crc64 image.bmp<br/>"
            "python main.py lzma -l image.bmp.xz              # Affiche les metadonnees et ratios<br/>"
            "python main.py lzma -t -v image.bmp.xz           # Test d'integrite<br/><br/>"
            "<b># 3. Utilitaire 7-Zip (7z) :</b><br/>"
            "python main.py 7z a archive.7z dossier/ -mx9     # Cree une archive 7z niveau ultra<br/>"
            "python main.py 7z l archive.7z                   # Liste les fichiers et attributs<br/>"
            "python main.py 7z x archive.7z -o./dest          # Extrait avec chemins complets<br/>"
            "python main.py 7z t archive.7z                   # Teste la somme de controle<br/>"
            "python main.py 7z b                              # Lance le benchmark CPU (MIPS)<br/><br/>"
            "<b># 4. Interface Graphique et Scripts batch :</b><br/>"
            "python main.py gui                               # Ouvre l'interface Desktop interactive<br/>"
            "python main.py benchmark                         # Rejoue le benchmark complet",
            st['code']
        )]
    ]
    t_cmd = Table(cmd_box, colWidths=[17.2 * cm])
    t_cmd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_cmd)
    story.append(Spacer(1, 10))

    story.append(Paragraph("10. Conclusion & Transmission par Email", st['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=s_blue, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Ce projet a permis de concilier une reproduction technique fidele des utilitaires <b>bzip2</b>, <b>lzma</b> et <b>7-zip</b> avec une analyse experimentale approfondie sur quatre types de donnees. "
        "L'ensemble du code source est versionne et deploye sur GitHub.",
        st['body']
    ))
    story.append(Spacer(1, 5))

    email_box = [
        [Paragraph(
            "<b>Modele d'Email Transmis a l'Enseignant :</b><br/><br/>"
            "<b>A :</b> lucsarobidynomenjanahary@gmail.com<br/>"
            "<b>Objet :</b> Rendu d'Examen - Clones des utilitaires de compression bzip2, lzma et 7-zip<br/><br/>"
            "Bonjour Mr Sarobidy,<br/><br/>"
            "Veuillez trouver ci-joint les livrables de l'examen pratique de compression de donnees.<br/>"
            "Le depot GitHub contenant le code complet executable est disponible a l'adresse :<br/>"
            "<font color='#2563eb'><u>https://github.com/tsiory-bainga/clone-compression-bzip2-lzma-7zip</u></font><br/><br/>"
            "Le document PDF complet incluant les captures d'ecran demontrant l'efficacite de la compression sur les 4 types de fichiers (texte, audio, image et video) est joint et accessible sur le Bureau.<br/><br/>"
            "Cordialement,<br/>"
            "L'Etudiant",
            st['body']
        )]
    ]
    t_email = Table(email_box, colWidths=[17.2 * cm])
    t_email.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('BOX', (0,0), (-1,-1), 1, p_blue),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_email)
