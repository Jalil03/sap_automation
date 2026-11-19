"""Build the administrator report from verified project findings; no SAP access."""
from pathlib import Path
import re,json
from html import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT,TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf/S4600_Rapport_administrateur_2026-10-23.pdf'
QA=ROOT/'tmp/pdfs/s4600_admin_review'
OUT.parent.mkdir(parents=True,exist_ok=True);QA.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial',boldItalic='Arial-Bold')
NAVY=colors.HexColor('#17324D');TEAL=colors.HexColor('#126C75');INK=colors.HexColor('#233344');MUTED=colors.HexColor('#526170');LINE=colors.HexColor('#D9E1E8');PALE=colors.HexColor('#F2F6F8')
styles={
 'body':ParagraphStyle('Body',fontName='Arial',fontSize=10.2,leading=14.2,textColor=INK,spaceAfter=8),
 'small':ParagraphStyle('Small',fontName='Arial',fontSize=9,leading=12.3,textColor=MUTED,spaceAfter=7),
 'title':ParagraphStyle('Title',fontName='Arial-Bold',fontSize=25,leading=29,textColor=NAVY,spaceAfter=12),
 'h1':ParagraphStyle('H1',fontName='Arial-Bold',fontSize=18,leading=22,textColor=NAVY,spaceAfter=12),
 'h2':ParagraphStyle('H2',fontName='Arial-Bold',fontSize=11.3,leading=15,textColor=TEAL,spaceBefore=10,spaceAfter=6),
 'cell':ParagraphStyle('Cell',fontName='Arial',fontSize=9.1,leading=12.1,textColor=INK),
 'head':ParagraphStyle('Head',fontName='Arial-Bold',fontSize=9.1,leading=12,textColor=colors.white),
 'number':ParagraphStyle('Number',fontName='Arial-Bold',fontSize=9.6,leading=12,textColor=NAVY,alignment=TA_CENTER),
}
story=[];coverage=[]
def clean(s):return str(s).replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')
def p(s,style='body'):return Paragraph(clean(s),styles[style])
def para(s,style='body'):story.append(p(s,style))
def head(n,title,subtitle=None):
    para(f'{n:02d}  {title}','h1')
    if subtitle:para(subtitle,'small')
def table(headers,rows,widths,exercise=False):
    data=[[p(escape(x),'head') for x in headers]]
    for row in rows:
        data.append([p(str(x),'number' if exercise and i==0 else 'cell') for i,x in enumerate(row)])
    t=Table(data,colWidths=[w*mm for w in widths],repeatRows=1,hAlign='LEFT')
    cmds=[('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('BOX',(0,0),(-1,-1),.45,LINE),('INNERGRID',(0,0),(-1,-1),.35,LINE),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]
    for i in range(1,len(data)):
        if i%2==0:cmds.append(('BACKGROUND',(0,i),(-1,i),PALE))
    t.setStyle(TableStyle(cmds));story.append(t);story.append(Spacer(1,8))
    if exercise:coverage.extend(int(row[0]) for row in rows)
def newpage():story.append(PageBreak())

# Page 1: decision summary.
para('S4600<br/>Rapport d’avancement<br/>et de faisabilité','title')
para('<b>À l’attention de l’administrateur SAP et de l’équipe de formation</b><br/>Situation arrêtée au 23 octobre 2026','body')
para('Système <b>A4H</b>  |  Mandant <b>600</b>  |  Utilisateur <b>ABDELJ</b><br/>Groupe <b>00</b>  |  Domaine commercial <b>FR10 / 10 / 1W</b>','small')
para('Nous avons terminé et vérifié <b>17 exercices sur 36</b> : 13 exercices pratiques et 4 exercices théoriques. Les 19 autres restent ouverts. Le présent rapport précise ce qui a réellement été exécuté, ce qui a été vérifié sans sauvegarde et les blocages à traiter.')
table(['État principal','Exercices','Total'],[
 ('Terminés et vérifiés','2, 3, 4, 5, 6, 7, 12, 15, 16, 18, 19, 21, 22, 24, 25, 28, 29','17'),
 ('Faisabilité partielle vérifiée','20, 26, 34','3'),
 ('Blocages directs ou écarts au manuel','8, 9, 11, 17, 23, 30, 31','7'),
 ('Dépendance à un prédécesseur','10, 13, 14, 27, 32, 33','6'),
 ('Parcours Fiori non vérifiés','1, 35, 36','3'),
], [65,96,13])
para('Décisions attendues de l’administrateur','h2')
for s in [
 '<b>30 :</b> identifier le produit SAP correspondant à T-F100 et ses données de fabrication en FR10.',
 '<b>8 :</b> communiquer le compte banque/caisse FR10 adapté à l’encaissement.',
 '<b>9 et 11 :</b> valider les valeurs du client participant et le modèle complet de l’article à créer.',
 '<b>31 :</b> définir les données de la vue article-usine du produit de service 90000133.',
 '<b>17 et 23 :</b> décider d’une adaptation pédagogique ou d’un scénario isolé reproduisant le manuel.',
]:para(s,'small')
para('<b>Consigne actuelle : faisabilité uniquement.</b> Aucun nouveau document, mouvement de stock, avoir ou changement de paramétrage n’est autorisé par ce rapport. Les tests positifs partiels ne constituent pas une validation intégrale.','small')

# Page 2: completed exercises.
newpage();head(2,'Exercices terminés et vérifiés','17 exercices clôturés : 13 pratiques et 4 théoriques')
para('Les résultats pratiques reposent sur l’adaptation retenue : FR10, secteur 1W et prélèvement dans la livraison sans EWM. Les interfaces Fiori spécifiques ne sont pas toutes validées par ces exécutions.','small')
table(['Ex.','Sujet','Résultat vérifié'],[
 ('2','Structures organisationnelles','Réponses théoriques comparées aux solutions du manuel.'),
 ('3','Commande client','Commande <b>154</b>, référence 4-200, net <b>3 100 EUR</b> ; deux postes conformes.'),
 ('4','Affichage de commande','Données commerciales et logistiques de la commande <b>154</b> relues.'),
 ('5','Livraison sortante','Livraison <b>80000085</b>, magasin <b>0001</b>, quantités et prélèvement vérifiés.'),
 ('6','Traitement des marchandises','Sortie de <b>80000085</b>, mouvement <b>601</b>, document matériel <b>4900000263</b> / 2026.'),
 ('7','Facturation','Facture <b>90000090</b> ; pièce FI <b>9300000009</b> ; brut <b>3 720 EUR</b>.'),
 ('12','Fiche client-article','<b>K-MS-00</b>, commande <b>159</b>, livraison <b>80000087</b> ; « Phare Premium » repris.'),
 ('15','Données de condition','Questions théoriques traitées et vérifiées.'),
 ('16','Proposition de postes','Proposition <b>50000001</b> affectée au client et copiée dans la commande <b>160</b>.'),
 ('18','Détermination automatique','Commande <b>156</b>, référence 6-100, créée puis relue indépendamment.'),
 ('19','Ordonnancement','Commande <b>157</b> : deux réceptionnaires et dates d’éligibilité vérifiés.'),
 ('21','Transfert des besoins','Commande <b>161</b> : besoin de <b>20 pièces au 27/10</b>, lié à la mise à disposition.'),
 ('22','Livraisons partielles','Commande <b>162</b> : livraison complète non exigée ; codes de fractionnement relus.'),
 ('24','Fonctions ATP','Réponses théoriques comparées aux solutions du manuel.'),
 ('25','Livraisons collectives','Création de <b>80000088, 80000089, 80000090</b> ; neuf postes relus, sans sortie.'),
 ('28','Avant-vente','Demande <b>10000104</b> puis offre <b>20000103</b> puis commande <b>155</b>.'),
 ('29','Documents d’avant-vente','Questions théoriques traitées et vérifiées.'),
],[11,48,115],True)
para('<b>Exercices théoriques :</b> 2, 15, 24 et 29. Leur clôture ne vaut pas validation de configuration SAP. Les livraisons créées au 25 n’ont pas été prélevées ni comptabilisées pendant les contrôles de faisabilité.','small')

# Page 3: qualified positive feasibility.
newpage();head(3,'Faisabilité vérifiée avec limites','Ces trois exercices ne sont pas déclarés terminés')
table(['Ex.','Constat positif','Limite de validation'],[
 ('20','Données du contrôle de disponibilité accessibles. Groupe ATP de <b>10000284 / FR10 = 01</b>.','Le manuel attend <b>02</b>. Lecture faisable, mais résultats à interpréter selon la configuration réelle.'),
 ('26','Livraisons <b>80000088 à 80000090</b> présentes. Stocks physiques suffisants. Fonctions de prélèvement et de sortie disponibles ; routes déjà éprouvées sur 80000085.','Magasins des nouveaux postes encore vides, prélèvement non fait. Aucun mode test démontré pour ces fonctions OData. Comptabilisation des nouvelles cibles non garantie.'),
 ('34','Brouillon <b>RE</b> sur FR10 accepté : client <b>1000000112</b>, article <b>10000284 × 3</b>, motif <b>103</b>, net <b>360 EUR</b>.','Brouillon abandonné sans sauvegarde. Livraison de retour, entrée en stock et avoir non validés. Aucun retour créé.'),
],[11,82,81],True)
para('Détail du brouillon de retour','h2')
para('SAP a déterminé la division et le point d’expédition <b>FR10</b>, le poste <b>REN</b> et l’échéance <b>DN</b>. Le contrôle d’incomplétude a répondu <b>« Le document est complet »</b>. Le blocage d’avoir a été conservé ; la fermeture a été effectuée avec <b>Non</b> à la sauvegarde.')
para('Couverture physique des quatre livraisons préparées','h2')
table(['Article','Quantité à livrer¹','Stock libre FR10 / 0001'],[
 ('10000282','32','3 699'),('10000283','23','3 235'),('10000284','21','3 170')
],[47,58,69])
para('¹ Ensemble des livraisons 80000088 à 80000091 : les trois du 26 et la préparation du 32. Un stock physique suffisant ne garantit ni la confirmation ATP, ni l’absence de concurrence, ni la réussite d’une écriture FI.','small')
para('Sécurité des vérifications','h2')
para('Les statuts des quatre livraisons et les quantités de stock contrôlées sont restés <b>inchangés</b> après les simulations. Aucune fonction de sortie, d’annulation ou de prélèvement persistante n’a été appelée pour démontrer la faisabilité.')

# Page 4: substantive blockers.
newpage();head(4,'Blocages directs à résoudre','Sept exercices : données manquantes, contrat incomplet ou comportement différent du manuel')
table(['Ex.','Blocage constaté','Action minimale attendue'],[
 ('8','Encaissement : créance de <b>3 720 EUR</b> vérifiée, mais compte banque/caisse FR10 non établi. Adaptation sans escompte déjà retenue.','<b>FI :</b> communiquer le compte de trésorerie et, si nécessaire, les données de banque société ; les relire avant un test de paiement.'),
 ('9','Client <b>T-CUS00</b> non créé/mappé. Proposition FR10 préparée, mais numérotation, valeurs FI/fiscales et contrat complet non validés.','Valider la proposition champ par champ et le contrat de création. La copie automatique d’un client de référence n’est pas autorisée.'),
 ('11','Article <b>T-MS400</b> non identifié dans les recherches ciblées. Modèle, vues complètes, texte ADV, fiscalité et valorisation non validés.','Valider un modèle et les valeurs nécessaires, puis démontrer la préparation complète sans sauvegarde si la route le permet.'),
 ('17','Commande <b>158</b> corrigée, mais livraison <b>80000086</b> acceptée avant correction : les champs testés ne bloquent pas la livraison. Poids net demandé <b>20 KG</b>, brut <b>14 KG</b>.','Décider d’une adaptation pédagogique ou d’un scénario isolé. Ne pas modifier globalement les procédures partagées.'),
 ('23','ATP <b>01</b> au lieu de <b>02</b> ; stock <b>3 170</b>. Le test confirme <b>95/95</b> au 30/10. L’usine <b>1020</b> est absente ; le scénario de pénurie entre deux usines n’est pas reproduit.','Définir deux usines adaptées et une pénurie dans un scénario isolé, ou accepter une adaptation partielle. Ne pas consommer le stock partagé pour tester.'),
 ('30','Mapping de <b>T-F100</b> inconnu. Aucun résultat sous les filtres complémentaires FR10 stratégie 20 ou approvisionnement E. Nomenclature/gamme non rattachables à une cible.','<b>En attente admin :</b> fournir le numéro SAP du produit de fabrication prévu. Aucun produit de remplacement ni cycle MRP lancé.'),
 ('31','Service <b>90000133</b> : prix PR00/ZPR0 et poste TAD vérifiés, mais vue article-usine FR10 et dates logistiques manquantes. Aucune commande <b>8-600</b> créée.','Définir le contrat et les données nécessaires à l’extension article-usine, sans création de valorisation ou modification globale pour tester.'),
],[11,84,79],True)
para('<b>Portée des recherches :</b> un résultat nul sur un identifiant ou un filtre n’établit pas l’absence de tout produit équivalent dans SAP. Pour le 30, le constat est « mapping non identifié », pas « fabrication impossible dans tout le système ».','small')

# Page 5: dependencies and UI.
newpage();head(5,'Dépendances et parcours non validés','Six exercices attendent un prédécesseur ; trois parcours Fiori restent à contrôler')
table(['Ex.','État actuel','Dépendance exacte'],[
 ('10','Ajout de réceptionnaire et commande non testés sur la cible participant.','Client du <b>9</b> à créer/mapp er.'.replace('mapp er','mapper')),
 ('13','PR00 et séquence PR02 présents ; pas de prix de test sur les objets partagés.','Article participant du <b>11</b> et validation de la détermination du prix.'),
 ('14','K007 présent ; barème connu, mais aucune remise de test appliquée au client commun.','Client participant du <b>9</b> et contrat du barème isolé.'),
 ('27','Simulation collective exécutée sur les neuf postes de <b>80000088 à 80000090</b> : refus <b>VF066</b>.','Sorties du <b>26</b> manquantes. Aucune facture créée ; ventilation/FI non validées.'),
 ('32','Commande <b>163</b> et livraison <b>80000091</b> préparées ; simulation de facture refusée <b>VF066</b>.','Sortie de 80000091, puis facture source avant demande d’avoir et avoir. <b>Exercice partiellement exécuté.</b>'),
 ('33','Fonction API Cancel disponible, sans mode test observé. Aucune annulation lancée.','Avoir de l’exercice <b>32</b> absent. Ne pas annuler un document existant pour tester.'),
],[11,91,72],True)
para('<b>VF066 :</b> « Aucune sortie de marchandises encore enregistrée pour la livraison ». C’est un prérequis manquant, pas un défaut de facturation démontré. Les deux simulations ont utilisé <b>TESTRUN=X</b>, POSTING vide, sans COMMIT ; aucune facture n’a été persistée.','small')
para('Fiori accessible mais parcours non vérifiés','h2')
para('L’utilisateur a confirmé son accès au Launchpad par une capture. La limite ci-dessous ne doit pas être présentée comme une absence d’accès SAP.','small')
table(['Ex.','Parcours attendu','Ce qui reste à contrôler'],[
 ('1','Navigation et personnalisation','Compte cible, groupe de favoris, trois applications et valeurs personnelles. Exercice laissé de côté à la demande de l’utilisateur.'),
 ('35','Analyse et résolution des commandes','Application, catalogue/droits et traitement complet d’une commande incomplète.'),
 ('36','Analyse des ventes','Application analytique, filtres, navigation, graphique et export du manuel.'),
],[11,58,105],True)
para('Le pilotage navigateur requis est indisponible dans la session d’automatisation. Un parcours manuel guidé reste possible. Un calcul ou une lecture API ne remplace pas la validation des écrans demandés.','small')

# Page 6: evidence and handoff.
newpage();head(6,'Traçabilité et cadre de poursuite','Documents déjà présents et références de vérification')
table(['Scénario','Documents SAP de référence'],[
 ('Cycle initial - 3 à 7','Commande <b>154</b> ; livraison <b>80000085</b> ; document matériel <b>4900000263</b> ; facture <b>90000090</b> ; pièce FI <b>9300000009</b>.'),
 ('Avant-vente - 28','Demande <b>10000104</b> ; offre <b>20000103</b> ; commande <b>155</b>.'),
 ('Données / dates - 18 et 19','Commandes <b>156</b> et <b>157</b>.'),
 ('Incomplétude - 17','Commande <b>158</b> ; livraison <b>80000086</b>, sans sortie.'),
 ('Client-article - 12','Fiche <b>K-MS-00</b> ; commande <b>159</b> ; livraison <b>80000087</b>, sans sortie.'),
 ('Proposition - 16','Proposition <b>50000001</b> ; commande <b>160</b>.'),
 ('Besoins / fractionnement','Commandes <b>161</b> et <b>162</b>.'),
 ('Traitement collectif - 25','Livraisons <b>80000088, 80000089, 80000090</b>, sans prélèvement ni sortie.'),
 ('Préparation - 32','Commande <b>163</b> ; livraison <b>80000091</b>, sans sortie ni facture.'),
],[56,118])
para('Sources disponibles dans le dossier du projet','h2')
for s in [
 '<b>Rapport global :</b> reports/S4600_rapport_global_exercices_2026-10-23.md',
 '<b>Faisabilité :</b> reports/s4600_remaining_exercises_feasibility_2026-10-23.md',
 '<b>Exécutions :</b> rapports datés des exercices 4, 6, 7 et 28 ; lot du 22/10 pour 12, 16, 21, 22, 25 et préparation 32.',
 '<b>Diagnostics :</b> rapports 8, 9/11, 17/20, 30 et 31 ; validation du brouillon 34 du 23/10.',
 '<b>Preuves techniques :</b> runtime/sap_reads et runtime/sap_writes ; journaux avant/après, retours SAP et relectures indépendantes.',
]:para(s,'small')
para('Cadre de poursuite','h2')
para('Le dernier audit n’a créé aucun document ni modifié les états SAP contrôlés. Les quantités de stock, statuts de livraison et absences de factures ont été relus indépendamment après simulation.')
para('Les dossiers en attente de l’administrateur, notamment le <b>30</b>, restent inchangés. Toute création, réception, sortie, facture, avoir ou annulation nécessiterait un périmètre distinct explicitement autorisé. Aucun changement de fiscalité, ledger, devises ou Material Ledger n’est demandé par le présent rapport.')
para('<b>Bilan final : 17 exercices terminés ; 19 non terminés avec un état documenté.</b> Les validations partielles sont conservées sans être assimilées à une exécution complète.','small')

assert sorted(coverage)==list(range(1,37)),coverage
def decorate(canvas,doc):
    canvas.saveState();w,h=A4
    if doc.page>1:
        canvas.setFont('Arial-Bold',8);canvas.setFillColor(NAVY);canvas.drawString(18*mm,h-14*mm,'S4600  |  AVANCEMENT ET FAISABILITÉ')
        canvas.setFont('Arial',8);canvas.setFillColor(MUTED);canvas.drawRightString(w-18*mm,h-14*mm,'A4H / 600  -  Groupe 00')
    canvas.setStrokeColor(LINE);canvas.setLineWidth(.5);canvas.line(18*mm,17*mm,w-18*mm,17*mm)
    canvas.setFont('Arial',8);canvas.setFillColor(MUTED);canvas.drawString(18*mm,11*mm,'Situation au 23 octobre 2026  |  Destinataire : administration SAP')
    canvas.setFont('Arial-Bold',8);canvas.drawRightString(w-18*mm,11*mm,f'{doc.page:02d} / 06')
    canvas.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=23*mm,bottomMargin=23*mm,title='S4600 Rapport administrateur Avancement et faisabilité',author='Projet de préparation SAP',subject='Bilan des 36 exercices S4600 sur A4H600 FR10',pageCompression=1)
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
pdf=pymupdf.open(OUT)
assert len(pdf)==6,f'Unexpected pagination: {len(pdf)} pages'
texts=[]
for i,page in enumerate(pdf):
    texts.append(page.get_text())
    page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5),alpha=False).save(QA/f'page-{i+1}.png')
    for word in page.get_text('words'):
        assert word[0]>=17*mm-1 and word[2]<=A4[0]-17*mm+1,f'Text outside margins page{i+1}: {word}'
text='\n'.join(texts)
for needle in ('17 exercices sur 36','VF066','90000090','9300000009','T-F100','360 EUR','TESTRUN=X'):
    assert needle in text,needle
(QA/'validation.json').write_text(json.dumps({'page_count':len(pdf),'exercise_coverage':coverage,'text_and_margin_checks':'PASS','pdf':str(OUT)},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pdf':str(OUT),'pages':len(pdf),'qa':str(QA),'size_bytes':OUT.stat().st_size},ensure_ascii=False))
