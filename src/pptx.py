# Génération du contenu de la présentation PowerPoint pour Stephane
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

prs = Presentation()

# Format général de la présentation
SLD_TITLE = prs.slide_layouts[0]
SLD_CONTENT = prs.slide_layouts[1]

# Helper pour ajouter une slide avec titre

def add_slide(title, content="", bullet_points=None):
    slide = prs.slides.add_slide(SLD_CONTENT)
    slide.shapes.title.text = title
    content_box = slide.placeholders[1]
    content_box.text = content
    if bullet_points:
        for point in bullet_points:
            p = content_box.text_frame.add_paragraph()
            p.text = point
            p.level = 0
    return slide

# Titre
slide_title = prs.slides.add_slide(SLD_TITLE)
slide_title.shapes.title.text = "Projektpräsentation – Sommerprüfung 2025"
slide_title.placeholders[1].text = "Stephane Sob Fouodji\nWave Distribution & Computersysteme GmbH"

# Präambel & Projektname
add_slide("Einleitung", bullet_points=[
    "Projekt: Entwicklung einer Browser-Applikation zur Gruppenverwaltung in ELO",
    "Ziel: Effiziente, benutzerfreundliche Verwaltung von AD-Gruppen und ELO-Rechten",
    "Durchgeführt bei Wave Distribution in Zusammenarbeit mit der internen IT"
])

# Unternehmenskontext
add_slide("Unternehmenskontext", bullet_points=[
    "Wave Distribution ist auf IT-Komponenten & Systemlösungen spezialisiert",
    "Teil der ALTERNATE GmbH Gruppe",
    "Einsatz von ELO zur Dokumentenarchivierung & E-Mail-Management",
    "Benutzerverwaltung über Active Directory – ohne direkte ELO-Integration"
])

# Agenda
add_slide("Agenda", bullet_points=[
    "Einleitung",
    "Analyse",
    "Entwurf & Architektur",
    "Implementierung",
    "Tests & Qualität",
    "Wirtschaftlichkeit",
    "Fazit & Ausblick"
])

# Analyse – Ist-Zustand
add_slide("Analyse – Ist-Zustand", bullet_points=[
    "Manuelle Rechtevergabe in ELO",
    "Keine zentrale Übersicht",
    "Keine AD-Validierung",
    "Hoher Zeitaufwand und Fehleranfälligkeit"
])

# Analyse – Soll-Zustand
add_slide("Analyse – Soll-Zustand", bullet_points=[
    "Zentrale Web-Applikation zur Rechteverwaltung",
    "Direkte LDAP-Validierung der Gruppen",
    "Filter, Suche, responsives Design",
    "Sichere Authentifizierung via MSAL"
])

# Architektur
add_slide("Systemarchitektur", bullet_points=[
    "Frontend: Angular UI mit MSAL",
    "Backend: Quarkus REST API (Java)",
    "PostgreSQL als Datenbank",
    "Verbindung zu ELO API & Active Directory (LDAP)"
])

# Platzhalter für Diagramme
add_slide("Architekturdiagramm (Platzhalter)", "[Diagramm hier einfügen – Zoombereit]")
add_slide("Klassendiagramm (Platzhalter)", "[Diagramm hier einfügen – Zoombereit]")
add_slide("Use Case Diagramm (Platzhalter)", "[Diagramm hier einfügen – Zoombereit]")

# Implementierung – Backend & Frontend
add_slide("Implementierung – Backend", bullet_points=[
    "Quarkus + Panache",
    "REST-API mit CRUD-Endpunkten",
    "ADVerificationService via LDAP",
    "EloProcess zur Rechtevergabe in ELO"
])

add_slide("Implementierung – Frontend", bullet_points=[
    "Angular SPA mit Routing & Services",
    "Login-Komponente mit MSAL",
    "Gruppenverwaltung mit Dialogen",
    "Mocking zur Entwicklungszeit"
])

# Tests & Qualität
add_slide("Tests & Qualitätssicherung", bullet_points=[
    "Postman-Tests aller REST-Endpunkte",
    "Mock-Daten für UI-Validierung",
    "Validierungslogik Frontend & Backend",
    "UI-Test mit Entwickler-Tools"
])

# Wirtschaftlichkeit
add_slide("Wirtschaftlichkeit (Simulation)", bullet_points=[
    "Interne Umsetzung ohne Lizenzkosten",
    "Gesamtkosten (Simuliert): ca. 1.278 €",
    "Hohe Effizienz durch Eigenentwicklung",
    "Geringe Wartungskosten dank modularer Struktur"
])

# Fazit
add_slide("Fazit", bullet_points=[
    "Ziele vollständig erreicht",
    "Moderne, sichere, wartbare Lösung",
    "Echte Zeitersparnis für Admins",
    "Wissen in Angular, Quarkus & LDAP vertieft"
])

# Ausblick & Lessons Learned
add_slide("Ausblick & Lessons Learned", bullet_points=[
    "Rollenbasierte UI-Funktionen",
    "Protokollierung von Benutzeraktionen",
    "Optionales Rücksynchronisieren mit ELO",
    "Erfahrung mit realistischen Problemen & pragmatischen Lösungen"
])

# Danke
add_slide("Vielen Dank für Ihre Aufmerksamkeit", "Fragen willkommen! \nProjektbetreuer: Alexander Ernst")

# Enregistrer la présentation
pptx_path = "/mnt/data/Stephane_ELO_Gruppenverwaltung_Praesentation.pptx"
prs.save(pptx_path)
pptx_path
