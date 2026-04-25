---
title: Detaillierte Use Cases
tags:
  - Anforderungen
  - Use Cases
---

# Detaillierte Use-Case-Beschreibungen

Die folgenden zehn Use Cases decken die zentralen Funktionsbereiche ab.
Jeder UC ist nach der standardisierten Schablone beschrieben.

---

## UC-01 – Projekt anlegen {#uc-01}

> **Verantwortlich:** Mitglied 1

| Feld | Inhalt |
|---|---|
| **Name** | Projekt anlegen |
| **Primärer Nutzer** | Projektleiter / Geschäftsführung |
| **Ziel** | Ein neues Projekt mit allen Stammdaten, Kostenrahmen und Terminen anlegen |
| **Priorität** | 🔴 Hoch |

**Vorbedingung**
:  Der Nutzer ist angemeldet und besitzt die Rolle `Projektleiter` oder `Geschäftsführung`.
Mindestens ein Kunde ist im System vorhanden.

**Nachbedingung**
:  Das Projekt ist gespeichert, eine eindeutige Projektnummer ist vergeben,
das Ampelsystem ist initialisiert (🟢 Grün) und das Projekt erscheint im Dashboard.

**Beteiligte**
:  System (automatische Nummernvergabe), Mitarbeiter (Teamzuordnung), Kunde

### Standardablauf

1. Nutzer öffnet *„Neues Projekt"* im Menü
2. System zeigt das Projektformular
3. Nutzer füllt Pflichtfelder aus: Bezeichnung, Kunde, Start-/Enddatum, kalkulierte Gesamtkosten
4. Nutzer wählt Projektleiter und ordnet Mitarbeiter/Teams zu
5. Nutzer definiert Projekttätigkeiten (max. Stunden + Stundensatz)
6. Nutzer speichert das Projekt
7. System validiert die Eingaben und vergibt Projektnummer
8. System initialisiert Ampelstatus auf 🟢 Grün
9. System zeigt Bestätigung – Projekt erscheint im Dashboard

### Erweiterungen / Alternativszenarien

| ID | Auslöser | Reaktion |
|---|---|---|
| **E1** | Pflichtfelder fehlen | System zeigt Fehlermeldung, Speichern blockiert |
| **E2** | Enddatum vor Startdatum | Validierungsfehler mit Hinweistext |
| **E3** | Keine ausreichende Berechtigung | Zugriff verweigert, Hinweis auf Administrator |
| **E4** | Nutzer bricht ab | Keine Daten werden gespeichert |

---

## UC-05 – Projektstatus überwachen (Ampelsystem) {#uc-05}

> **Verantwortlich:** Mitglied 1

| Feld | Inhalt |
|---|---|
| **Name** | Projektstatus überwachen (Ampelsystem) |
| **Primärer Nutzer** | System (automatisiert), Projektleiter |
| **Ziel** | Automatische Erkennung von Kosten-/Terminüberschreitungen, optische Darstellung |
| **Priorität** | 🔴 Hoch |

**Vorbedingung**
:  Projekt ist aktiv, Kostenrahmen und Termine sind definiert, Aufwandsbuchungen liegen vor.

**Nachbedingung**
:  Ampelstatus korrekt gesetzt. Bei Warnstufe oder Kritisch wurde E-Mail-Benachrichtigung ausgelöst.

**Beteiligte**
:  Projektleiter (Empfänger der Warnung), E-Mail-Server

### Standardablauf

1. System berechnet nach jeder Buchung die aktuellen Gesamtkosten und den Erfüllungsgrad
2. System vergleicht aktuelle Kosten mit dem Kostenrahmen
3. System prüft verbleibende Zeit bis Enddatum

    | Status | Bedingung |
    |---|---|
    | 🟢 **Grün** | Kosten < 80 % des Rahmens **UND** Frist nicht nahe |
    | 🟡 **Gelb** | Kosten 80–99 % **ODER** Enddatum < 14 Tage |
    | 🔴 **Rot** | Kosten ≥ 100 % **ODER** Enddatum überschritten |

4. System aktualisiert Ampelfarbe im Dashboard
5. Bei 🟡 Gelb oder 🔴 Rot: System sendet automatisch E-Mail an Projektleiter

### Erweiterungen

| ID | Auslöser | Reaktion |
|---|---|---|
| **E1** | E-Mail-Server nicht erreichbar | Warnung im System-Log, E-Mail in Warteschlange |
| **E2** | Mehrere Projekte gleichzeitig kritisch | Jedes Projekt erhält separaten E-Mail-Versand |
| **E3** | Projektleiter hat keine E-Mail hinterlegt | Benachrichtigung an Geschäftsführung |

---

## UC-07 – Projektübersicht als PDF exportieren {#uc-07}

> **Verantwortlich:** Mitglied 3

| Feld | Inhalt |
|---|---|
| **Name** | Projektübersicht als PDF exportieren |
| **Primärer Nutzer** | Projektleiter, Geschäftsführung |
| **Ziel** | Vollständige Projektübersicht inkl. Unterprojekten und Kostenpositionen als PDF generieren |
| **Priorität** | 🔴 Hoch |

**Vorbedingung**
:  Nutzer ist angemeldet und hat Leseberechtigung für das Projekt. Das Projekt existiert.

**Nachbedingung**
:  Eine PDF-Datei ist generiert und steht zum Download bereit. Inhalt entspricht aktuellem Projektstand.

### Standardablauf

1. Nutzer öffnet die Projektdetailansicht
2. Nutzer klickt *„PDF exportieren"*
3. System sammelt alle Projektdaten inkl. Unterprojekte, Kostenpositionen, Buchungen und Ampelstatus
4. System generiert PDF mit Deckblatt, Projektdetails, Kostentabellen
5. System bietet Download der PDF-Datei an
6. Nutzer lädt die Datei herunter

### Erweiterungen

| ID | Auslöser | Reaktion |
|---|---|---|
| **E1** | Sehr viele Unterprojekte | Ladeindikator wird angezeigt |
| **E2** | Keine Leseberechtigung | Export wird verweigert |
| **E3** | Fehler im PDF-Generator | Fehlermeldung mit Hinweis, es erneut zu versuchen |

---

## UC-08 – Rechnung erstellen (PDF) {#uc-08}

> **Verantwortlich:** Mitglied 3

| Feld | Inhalt |
|---|---|
| **Name** | Rechnung erstellen (PDF) |
| **Primärer Nutzer** | Projektleiter |
| **Ziel** | Bei Projektabschluss automatisch eine Kundenrechnung mit allen Kostenpositionen erstellen |
| **Priorität** | 🔴 Hoch |

**Vorbedingung**
:  Projekt hat Status `Abgeschlossen`. Kundendaten sind vollständig gepflegt.

**Nachbedingung**
:  Die Rechnung ist als PDF gespeichert und steht zum Download/Versand bereit.

### Standardablauf

1. Projektleiter setzt Projektstatus auf *„Abgeschlossen"*
2. System fordert Bestätigung des Abschlusses
3. Projektleiter bestätigt
4. System aggregiert alle Kostenpositionen (Stunden, Material, externe Dienstleister)
5. System generiert Rechnung mit Rechnungsnummer, Datum, Kundendaten und Positionen
6. System erstellt PDF und zeigt Download-Button
7. Projektleiter lädt Rechnung herunter und versendet sie an den Kunden

### Erweiterungen

| ID | Auslöser | Reaktion |
|---|---|---|
| **E1** | Kundendaten unvollständig | Warnung – Abschluss trotzdem möglich, aber Hinweis |
| **E2** | Keine Kostenpositionen | Leere Rechnung mit Hinweis |
| **E3** | Nutzer bricht ab | Status bleibt `Aktiv` |

---

## UC-09 – Aufwand buchen (Zeit) {#uc-09}

> **Verantwortlich:** Mitglied 2

| Feld | Inhalt |
|---|---|
| **Name** | Aufwand buchen (Zeit) |
| **Primärer Nutzer** | Mitarbeiter |
| **Ziel** | Geleistete Arbeitsstunden auf ein Projekt buchen |
| **Priorität** | 🔴 Hoch |

**Vorbedingung**
:  Mitarbeiter ist angemeldet und mindestens einem Projekt zugeordnet. Projekt ist nicht abgeschlossen.

**Nachbedingung**
:  Buchung gespeichert. Projektkosten aktualisiert. Ampelsystem neu berechnet.

### Standardablauf

1. Mitarbeiter öffnet *„Aufwand buchen"*
2. System zeigt dem Mitarbeiter zugeordnete Projekte
3. Mitarbeiter wählt Projekt und Tätigkeit
4. Mitarbeiter gibt Datum, Stundenzahl und optionale Beschreibung ein
5. System berechnet Kosten: `Stunden × Stundensatz der Tätigkeit`
6. Mitarbeiter bestätigt die Buchung
7. System speichert Buchung und aktualisiert Projektkosten
8. System prüft Ampelstatus, löst ggf. Warnung aus

### Erweiterungen

| ID | Auslöser | Reaktion |
|---|---|---|
| **E1** | Stunden > Maximum der Tätigkeit | Warnung, Buchung dennoch möglich |
| **E2** | Datum in der Zukunft | Hinweis, Buchung bleibt erlaubt |
| **E3** | Projekt inzwischen abgeschlossen | Buchung wird abgewiesen mit Fehlermeldung |
| **E4** | Keine Tätigkeiten zugewiesen | Fehlermeldung – Projektleiter informieren |

---

## UC-10 – Materialkosten buchen {#uc-10}

> **Verantwortlich:** Mitglied 2

| Feld | Inhalt |
|---|---|
| **Name** | Materialkosten buchen |
| **Primärer Nutzer** | Mitarbeiter |
| **Ziel** | Verbrauchte Materialien mit Kosten als Buchungsposition auf ein Projekt erfassen |
| **Priorität** | 🔴 Hoch |

**Vorbedingung**
:  Mitarbeiter ist angemeldet und einem aktiven Projekt zugeordnet.

**Nachbedingung**
:  Materialbuchung gespeichert. Projektkosten aktualisiert. Ampelstatus neu bewertet.

### Standardablauf

1. Mitarbeiter öffnet *„Aufwand buchen"* → Tab *„Material"*
2. System zeigt zugeordnete Projekte
3. Mitarbeiter wählt Projekt
4. Mitarbeiter gibt Materialbezeichnung, Menge, Einheit und Betrag ein
5. Mitarbeiter fügt optional Belegnummer / Beschreibung hinzu
6. Mitarbeiter bestätigt die Buchung
7. System speichert Materialbuchung als Kostenposition
8. System aktualisiert Projektkosten und prüft Ampelstatus

### Erweiterungen

| ID | Auslöser | Reaktion |
|---|---|---|
| **E1** | Betrag = 0 oder negativ | Validierungsfehler |
| **E2** | Pflichtfelder fehlen | Formular-Validierung verhindert Speichern |
| **E3** | Projekt ist abgeschlossen | Buchung wird abgewiesen |

---

## UC-11 – Mitarbeiter anlegen {#uc-11}

> **Verantwortlich:** Mitglied 4

| Feld | Inhalt |
|---|---|
| **Name** | Mitarbeiter anlegen |
| **Primärer Nutzer** | Geschäftsführung / Administrator |
| **Ziel** | Neuen Mitarbeiter mit vollständigen Stammdaten im System anlegen |
| **Priorität** | 🔴 Hoch |

**Vorbedingung**
:  Nutzer hat Rolle `Admin` oder `Geschäftsführung`. Personalnummer ist eindeutig.

**Nachbedingung**
:  Mitarbeiter ist gespeichert, hat Status `Aktiv` und kann Projekten zugeordnet werden.

### Standardablauf

1. Admin öffnet *„Mitarbeiterverwaltung"* → *„Neuer Mitarbeiter"*
2. System zeigt Eingabeformular
3. Admin füllt Pflichtfelder: Personalnummer, Name, Vorname, Rolle/Tätigkeit, Stundensatz
4. Admin gibt an, ob Mitarbeiter als Projektleiter geeignet ist (Ja/Nein)
5. Admin weist Mitarbeiter optional einem oder mehreren Teams zu
6. Admin speichert
7. System validiert und speichert den Mitarbeiter mit Status `Aktiv`

### Erweiterungen

| ID | Auslöser | Reaktion |
|---|---|---|
| **E1** | Personalnummer bereits vorhanden | Fehlermeldung, Duplikate werden verhindert |
| **E2** | Stundensatz = 0 | Warnung, Speichern bleibt möglich |
| **E3** | Pflichtfelder fehlen | Validierungsfehler mit Hinweis |

---

## UC-13 – Team anlegen und Mitarbeiter zuordnen {#uc-13}

> **Verantwortlich:** Mitglied 5

| Feld | Inhalt |
|---|---|
| **Name** | Team anlegen und Mitarbeiter zuordnen |
| **Primärer Nutzer** | Projektleiter / Geschäftsführung |
| **Ziel** | Neues Team anlegen und Mitarbeiter zuordnen, um es als Einheit Projekten zuzuweisen |
| **Priorität** | 🟡 Mittel |

**Vorbedingung**
:  Nutzer hat Berechtigung `Projektleiter` oder `GF`. Mindestens ein Mitarbeiter ist im System.

**Nachbedingung**
:  Team gespeichert. Alle zugeordneten Mitarbeiter sind Mitglieder. Team ist für Projektzuordnung verfügbar.

### Standardablauf

1. Projektleiter öffnet *„Teams"* → *„Neues Team"*
2. System zeigt Formular mit Teamname und Mitarbeiterliste
3. Projektleiter gibt Teambezeichnung ein
4. Projektleiter wählt Mitarbeiter aus der Liste (Mehrfachauswahl)
5. Projektleiter speichert
6. System legt Team an und erstellt alle Mitgliedschaften
7. Team erscheint in der Projektteam-Auswahl

### Erweiterungen

| ID | Auslöser | Reaktion |
|---|---|---|
| **E1** | Teamname bereits vergeben | Warnung, Speichern wird nicht blockiert |
| **E2** | Kein Mitarbeiter gewählt | Leeres Team wird angelegt (Warnung) |
| **E3** | Mitarbeiter bereits in 5 Teams | Warnung – Mehrfachmitgliedschaft bleibt erlaubt |

---

## UC-14 – Kunden anlegen {#uc-14}

> **Verantwortlich:** Mitglied 5

| Feld | Inhalt |
|---|---|
| **Name** | Kunden anlegen |
| **Primärer Nutzer** | Geschäftsführung / Administrator |
| **Ziel** | Neuen Kunden mit vollständigen Kontaktdaten anlegen, um ihn Projekten zuordnen zu können |
| **Priorität** | 🔴 Hoch |

**Vorbedingung**
:  Nutzer hat Rolle `Admin` oder `GF`. Kundennummer ist eindeutig.

**Nachbedingung**
:  Kunde ist gespeichert und kann bei der Projektanlage ausgewählt werden.

### Standardablauf

1. Admin öffnet *„Kundenverwaltung"* → *„Neuer Kunde"*
2. System zeigt Eingabeformular
3. Admin füllt aus: Kundennummer, Name, Anschrift (Straße, PLZ, Ort, Land), Kontaktdaten (Telefon, E-Mail, Ansprechpartner)
4. Admin speichert
5. System validiert und speichert den Kunden
6. Kunde erscheint in der Auswahlliste bei Projektanlage

### Erweiterungen

| ID | Auslöser | Reaktion |
|---|---|---|
| **E1** | Kundennummer bereits vorhanden | Fehlermeldung |
| **E2** | Pflichtfelder fehlen | Validierungsfehler |
| **E3** | E-Mail-Format ungültig | Inline-Validierung zeigt Fehler |

---

## UC-16 – Benutzer anlegen / Rolle zuweisen {#uc-16}

> **Verantwortlich:** Mitglied 4

| Feld | Inhalt |
|---|---|
| **Name** | Benutzer anlegen / Rolle zuweisen |
| **Primärer Nutzer** | Administrator |
| **Ziel** | Systembenutzerzugänge anlegen und Benutzerrollen mit Berechtigungen zuweisen |
| **Priorität** | 🔴 Hoch |

**Vorbedingung**
:  Nutzer hat Rolle `Admin`. Benutzername/E-Mail ist eindeutig.

**Nachbedingung**
:  Benutzer kann sich anmelden. Berechtigungen gelten sofort.

### Standardablauf

1. Admin öffnet *„Benutzerverwaltung"* → *„Neuer Benutzer"*
2. Admin gibt E-Mail, Benutzername ein und wählt Rolle (`Mitarbeiter` / `Projektleiter` / `GF` / `Admin`)
3. Admin verknüpft Benutzer mit Mitarbeiterdatensatz
4. Admin speichert
5. System legt Benutzer an und sendet **Einladungsmail** mit Link zur Passwort-Festlegung
6. Benutzer folgt Link und setzt Passwort
7. Benutzer kann sich ab sofort anmelden

### Erweiterungen

| ID | Auslöser | Reaktion |
|---|---|---|
| **E1** | E-Mail bereits vorhanden | Fehlermeldung |
| **E2** | E-Mail-Server nicht erreichbar | Benutzer angelegt, Mail in Warteschlange |
| **E3** | Falscher Rollentyp gewählt | Admin kann Rolle nachträglich ändern |

---

## Rollenmatrix (Berechtigungsübersicht)

| Funktion | Mitarbeiter | Projektleiter | GF | Admin |
|---|:---:|:---:|:---:|:---:|
| Dashboard – eigene Projekte | ✅ | ✅ | ✅ | ✅ |
| Dashboard – alle Projekte | ❌ | ❌ | ✅ | ✅ |
| Projekt anlegen | ❌ | ✅ | ✅ | ✅ |
| Projekt bearbeiten | ❌ | ✅ (eigene) | ✅ | ✅ |
| Projekt abschließen | ❌ | ✅ | ✅ | ✅ |
| Aufwand buchen | ✅ | ✅ | ✅ | ✅ |
| PDF exportieren | ✅ | ✅ | ✅ | ✅ |
| Mitarbeiter verwalten | ❌ | ❌ | ✅ | ✅ |
| Kunden verwalten | ❌ | ❌ | ✅ | ✅ |
| Benutzer / Rollen verwalten | ❌ | ❌ | ❌ | ✅ |
