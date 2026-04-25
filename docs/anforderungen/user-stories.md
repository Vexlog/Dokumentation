---
title: User Stories
tags:
  - Anforderungen
  - User Stories
---

# User Stories mit Akzeptanzkriterien

Alle zehn User Stories im Standard-Format mit mindestens drei Akzeptanzkriterien
im **Given / When / Then**-Format.

---

## US-01 – Projekt anlegen {#us-01}

> **Verantwortlich:**  | **Rolle:** Projektleiter

!!! quote "Story"
    *„Als Projektleiter möchte ich ein neues Projekt mit allen Stammdaten anlegen können,
    damit ich Kosten, Termine und Ressourcen von Anfang an strukturiert planen kann."*

| # | Given | When | Then |
|---|---|---|---|
| **AK-1** | Ich als Projektleiter angemeldet bin | ich *„Neues Projekt"* öffne, alle Pflichtfelder ausfülle und speichere | wird das Projekt mit automatisch generierter Projektnummer gespeichert und erscheint im Dashboard |
| **AK-2** | Ich Pflichtfelder nicht ausgefüllt habe | ich auf *„Speichern"* klicke | zeigt das System inline Validierungsfehlermeldungen und speichert nicht |
| **AK-3** | Ich kein Recht habe Projekte anzulegen (normaler Mitarbeiter) | ich versuche die Projektanlage-Funktion aufzurufen | wird die Aktion verweigert und eine Meldung *„Unzureichende Berechtigung"* angezeigt |

---

## US-02 – Ampelwarnung {#us-02}

> **Verantwortlich:**  | **Rolle:** Projektleiter

!!! quote "Story"
    *„Als Projektleiter möchte ich sofort eine visuelle Warnung (Ampel) sehen, wenn ein Projekt
    drohende Kostenüberschreitungen aufweist, damit ich rechtzeitig gegensteuern kann."*

| # | Given | When | Then |
|---|---|---|---|
| **AK-1** | Ein Projekt 85 % des Kostenrahmens erreicht hat | ich das Dashboard öffne | zeigt das System ein 🟡 gelbes Ampelsymbol und ich erhalte eine E-Mail-Benachrichtigung |
| **AK-2** | Ein Projekt 100 % des Kostenrahmens überschritten hat | die Buchung gespeichert wird | wechselt der Status sofort auf 🔴 Rot und eine E-Mail an den Projektleiter wird versendet |
| **AK-3** | Alle Kosten unter 80 % liegen und der Termin nicht in 14 Tagen liegt | das Projekt angezeigt wird | ist die Ampel 🟢 Grün und es werden keine Warnungen ausgegeben |

---

## US-03 – Zeitbuchung {#us-03}

> **Verantwortlich:**  | **Rolle:** Mitarbeiter

!!! quote "Story"
    *„Als Mitarbeiter möchte ich meine geleisteten Arbeitsstunden auf ein Projekt buchen können,
    damit meine Leistung korrekt in die Projektkostenrechnung einfließt."*

| # | Given | When | Then |
|---|---|---|---|
| **AK-1** | Ich einem aktiven Projekt zugeordnet bin | ich eine Zeitbuchung mit Datum, Stunden und Tätigkeit erstelle | werden Kosten (`Stunden × Stundensatz`) berechnet und zum Projekt addiert |
| **AK-2** | Das Projekt bereits abgeschlossen ist | ich eine Buchung darauf vornehmen möchte | verweigert das System die Buchung mit *„Projekt ist abgeschlossen"* |
| **AK-3** | Ich mehr Stunden eingebe als das Maximum der Tätigkeit erlaubt | ich die Buchung abschicke | zeigt das System eine Warnung, erlaubt die Buchung aber trotzdem |

---

## US-04 – Materialbuchung {#us-04}

> **Verantwortlich:**  | **Rolle:** Mitarbeiter

!!! quote "Story"
    *„Als Mitarbeiter möchte ich Materialverbrauch mit Kosten auf ein Projekt buchen können,
    damit alle Sachkosten lückenlos erfasst werden."*

| # | Given | When | Then |
|---|---|---|---|
| **AK-1** | Ich einem aktiven Projekt zugeordnet bin | ich eine Materialbuchung mit Bezeichnung, Menge und Betrag erstelle und speichere | erscheint die Materialbuchung in der Kostenübersicht des Projekts |
| **AK-2** | Ich einen Betrag von 0 oder weniger eingebe | ich versuche zu speichern | zeigt das System *„Betrag muss größer als 0 sein"* |
| **AK-3** | Ich Pflichtfelder leer lasse | ich auf Speichern klicke | wird das Formular nicht abgeschickt und fehlende Felder rot hervorgehoben |

---

## US-05 – PDF-Export {#us-05}

> **Verantwortlich:**  | **Rolle:** Projektleiter

!!! quote "Story"
    *„Als Projektleiter möchte ich jederzeit eine vollständige Projektübersicht als PDF exportieren
    können, damit ich Stakeholdern einen strukturierten Statusbericht vorlegen kann."*

| # | Given | When | Then |
|---|---|---|---|
| **AK-1** | Ich ein Projekt in der Detailansicht geöffnet habe | ich auf *„PDF exportieren"* klicke | wird ein PDF mit Stammdaten, allen Unterprojekten und Kostenpositionen generiert und zum Download angeboten |
| **AK-2** | Das Projekt viele Unterprojekte hat | der Export gestartet wird | zeigt das System einen Ladeindikator bis das PDF fertig ist |
| **AK-3** | Ich keine Leseberechtigung für das Projekt habe | ich den Export versuche | wird der Export verweigert und eine entsprechende Meldung angezeigt |

---

## US-06 – Rechnung bei Projektabschluss {#us-06}

> **Verantwortlich:**  | **Rolle:** Projektleiter

!!! quote "Story"
    *„Als Projektleiter möchte ich beim Projektabschluss automatisch eine Kundenrechnung als PDF
    erhalten, damit ich diese direkt an den Kunden weiterleiten kann."*

| # | Given | When | Then |
|---|---|---|---|
| **AK-1** | Ein Projekt als *„Abgeschlossen"* markiert wird | ich die Aktion bestätige | generiert das System automatisch eine Rechnung mit allen Kostenpositionen als PDF |
| **AK-2** | Die Kundendaten vollständig sind | die Rechnung generiert wird | enthält das PDF die vollständige Kundenanschrift, Rechnungsnummer und alle Leistungspositionen |
| **AK-3** | Ich den Abschluss abbrecht | ich *„Abbrechen"* klicke | bleibt das Projekt im Status `Aktiv` und keine Rechnung wird erstellt |

---

## US-07 – GF-Dashboard {#us-07}

> **Verantwortlich:**  | **Rolle:** Geschäftsführung

!!! quote "Story"
    *„Als Mitglied der Geschäftsführung möchte ich alle Projekte im Unternehmen im Überblick sehen
    und nach Status filtern können, damit ich schnell Handlungsbedarf erkennen kann."*

| # | Given | When | Then |
|---|---|---|---|
| **AK-1** | Ich als GF angemeldet bin | ich das Dashboard öffne | sehe ich alle Projekte des Unternehmens mit Ampelstatus, Fortschrittsbalken und Projektleiter |
| **AK-2** | Ich nach *„Kritisch (Rot)"* filtere | der Filter angewendet wird | zeigt das Dashboard nur Projekte mit Ampelstatus 🔴 ROT |
| **AK-3** | Ein Mitarbeiter angemeldet ist | er das Dashboard öffnet | sieht er nur Projekte, denen er direkt zugeordnet ist |

---

## US-08 – Benutzerverwaltung {#us-08}

> **Verantwortlich:**  | **Rolle:** Administrator

!!! quote "Story"
    *„Als Administrator möchte ich Benutzerrollen verwalten und Rechte zuweisen können,
    damit jeder Nutzer nur auf die für ihn bestimmten Daten zugreifen kann."*

| # | Given | When | Then |
|---|---|---|---|
| **AK-1** | Ein neuer Mitarbeiter im System angelegt wurde | ich einen Benutzer mit Rolle *„Mitarbeiter"* erstelle und speichere | erhält der Mitarbeiter eine Einladungsmail und kann sich danach anmelden |
| **AK-2** | Ein Benutzer die Rolle *„Projektleiter"* hat | er versucht ein Projekt anzulegen | ist die Funktion für ihn zugänglich und nutzbar |
| **AK-3** | Ein Benutzer nur die Rolle *„Mitarbeiter"* hat | er die Benutzerverwaltung aufzurufen versucht | wird der Zugriff verweigert und eine Meldung erscheint |

---

## US-09 – Team-Verwaltung {#us-09}

> **Verantwortlich:**  | **Rolle:** Projektleiter

!!! quote "Story"
    *„Als Projektleiter möchte ich Teams anlegen und Mitarbeitern zuordnen können, damit ich bei
    der Projektanlage ganze Teams auf einmal zuweisen kann."*

| # | Given | When | Then |
|---|---|---|---|
| **AK-1** | Ich als Projektleiter angemeldet bin | ich ein Team anlege, Mitarbeiter auswähle und speichere | ist das Team verfügbar und alle Mitarbeiter als Mitglieder eingetragen |
| **AK-2** | Ein Mitarbeiter bereits in einem anderen Team ist | er einem weiteren Team zugeordnet wird | ist die Mehrfachmitgliedschaft erlaubt und er erscheint in beiden Teams |
| **AK-3** | Ich ein Team bei der Projektanlage auswähle | das Projekt gespeichert wird | sind alle Teammitglieder automatisch dem Projekt zugeordnet und können Buchungen vornehmen |

---

## US-10 – Mitarbeiter deaktivieren {#us-10}

> **Verantwortlich:**  | **Rolle:** Administrator

!!! quote "Story"
    *„Als Administrator möchte ich ausgeschiedene Mitarbeiter deaktivieren statt löschen können,
    damit historische Buchungen und Projektdaten erhalten bleiben."*

| # | Given | When | Then |
|---|---|---|---|
| **AK-1** | Ein Mitarbeiter das Unternehmen verlässt | ich ihn auf Status *„Inaktiv"* setze | wird er in der aktiven Mitarbeiterliste nicht mehr angezeigt, historische Buchungen bleiben erhalten |
| **AK-2** | Ein inaktiver Mitarbeiter existiert | ich versuche ihn einem neuen Projekt zuzuordnen | erscheint er in der Auswahlliste nicht und kann nicht zugewiesen werden |
| **AK-3** | Ein inaktiver Mitarbeiter historische Buchungen hat | die Projektkosten angezeigt werden | sind alle historischen Buchungen weiterhin in der Kostenübersicht enthalten |
