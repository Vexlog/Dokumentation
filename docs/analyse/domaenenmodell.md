---
title: Domänenklassendiagramm
tags:
  - Analyse
  - Klassendiagramm
  - UML
---

# Domänenklassendiagramm

Das Domänenklassendiagramm modelliert den **fachlichen Problembereich** ohne
technische Implementierungsdetails. Kern ist die Klasse `Projekt` mit rekursiver
Unterprojekt-Beziehung.

## Klassenübersicht

| Klasse | Beschreibung |
|---|---|
| **Projekt** | Zentrale Klasse. Selbstbeziehung ermöglicht beliebig tiefe Unterprojekte. Enthält finanzielle Kennzahlen, Termine und Ampelstatus. |
| **Aufwandsbuchung** | Abstrakte Superklasse für Zeit- und Materialbuchungen. Beide erhöhen `bisherigKosten` des Projekts. |
| **Zeitbuchung** | Erfasst Arbeitsstunden eines Mitarbeiters für eine Tätigkeit. |
| **Materialbuchung** | Erfasst Sachkosten mit Menge, Einheit und Betrag. |
| **Projekttaetigkeit** | Definiert Tätigkeitspositionen mit max. Stunden und Stundensatz (Budget-Referenz). |
| **ExterneKosten** | Kosten externer Dienstleister als feste Kostenposition ohne Mitarbeiterbezug. |
| **Mitarbeiter** | Unternehmens-Mitarbeiter. Bei Austritt: Status `INAKTIV` statt Löschung. Flag `istProjektleiter` steuert Berechtigung. |
| **Team** | Mitarbeitergruppe, die als Einheit Projekten zugewiesen werden kann. |
| **Teamzuordnung** | Assoziationsklasse zwischen Mitarbeiter und Team (Eintrittsdatum, Rolle). |
| **Kunde** | Auftraggeber. Adress- und Kontaktdaten fließen in Rechnungserstellung ein. |
| **Benutzer** | Systemzugang, verknüpft mit genau einem Mitarbeiter. Rolle steuert alle Zugriffsberechtigungen. |
| **Benachrichtigung** | Protokolliert ausgehende E-Mails. Versandstatus ermöglicht Wiederholung bei Fehlern. |
| **Rechnung** | Automatisch bei Projektabschluss erzeugt. Enthält aggregierte Kostenpositionen und PDF-Referenz. |

---

## Diagramm

```puml
@startuml BestPro_Domaenenklassendiagramm
class Projekt {
  projektnummer : String
  bezeichnung : String
  startdatum : Date
  enddatum : Date
  kalkulierteGesamtkosten : Decimal
  bisherigKosten : Decimal
  erfuellungsgrad : Double
  ampelstatus : AmpelStatus
  status : ProjektStatus
  anmerkungen : String
}

class Aufwandsbuchung {
  buchungsdatum : Date
  beschreibung : String
  buchungstyp : BuchungsTyp
}

class Zeitbuchung {
  stunden : Double
  berechneteKosten : Decimal
}

class Materialbuchung {
  materialbezeichnung : String
  menge : Double
  einheit : String
  betrag : Decimal
  belegnummer : String
}

class Projekttaetigkeit {
  bezeichnung : String
  maxStunden : Double
  stundensatz : Decimal
  budgetKosten : Decimal
}

class ExterneKosten {
  bezeichnung : String
  anbieter : String
  betrag : Decimal
}

class Mitarbeiter {
  personalnummer : String
  nachname : String
  vorname : String
  rolle : String
  stundensatz : Decimal
  istProjektleiter : Boolean
  status : MitarbeiterStatus
}

class Team {
  teamname : String
  beschreibung : String
}

class Teamzuordnung {
  eintrittsdatum : Date
  rolle : String
}

class Kunde {
  kundennummer : String
  name : String
  strasse : String
  plz : String
  ort : String
  land : String
  telefon : String
  email : String
  ansprechpartner : String
}

class Benutzer {
  benutzername : String
  email : String
  passwortHash : String
  rolle : Benutzerrolle
  aktiv : Boolean
}

class Benachrichtigung {
  versanddatum : DateTime
  empfaenger : String
  betreff : String
  status : VersandStatus
}

class Rechnung {
  rechnungsnummer : String
  rechnungsdatum : Date
  gesamtbetrag : Decimal
  pdfPfad : String
}

enum AmpelStatus {
  GRUEN
  GELB
  ROT
}

enum ProjektStatus {
  AKTIV
  ABGESCHLOSSEN
  PAUSIERT
}

enum BuchungsTyp {
  ZEIT
  MATERIAL
}

enum MitarbeiterStatus {
  AKTIV
  INAKTIV
}

enum Benutzerrolle {
  MITARBEITER
  PROJEKTLEITER
  GESCHAEFTSFUEHRUNG
  ADMIN
}

enum VersandStatus {
  AUSSTEHEND
  GESENDET
  FEHLER
}

' Hierarchie
Projekt "0..1" *-- "0..*" Projekt : enthaelt >

' Projektzuordnungen
Projekt "1" --> "1" Kunde : hat >
Projekt "1" --> "1" Mitarbeiter : geleitet von >
Projekt "0..*" --> "0..*" Team : zugeordnet >
Projekt "0..*" --> "0..*" Mitarbeiter : Team-Mitglieder >
Projekt "1" *-- "0..*" Projekttaetigkeit : definiert >
Projekt "1" *-- "0..*" ExterneKosten : beinhaltet >
Projekt "1" *-- "0..*" Aufwandsbuchung : hat >
Projekt "0..1" --> "0..1" Rechnung : erzeugt >

' Buchungs-Hierarchie
Aufwandsbuchung <|-- Zeitbuchung
Aufwandsbuchung <|-- Materialbuchung
Aufwandsbuchung "0..*" --> "1" Mitarbeiter : gebucht von >
Zeitbuchung "0..*" --> "1" Projekttaetigkeit : bezieht sich auf >

' Mitarbeiter und Teams
Mitarbeiter "0..*" -- "0..*" Team : Mitglied (via Teamzuordnung)
(Mitarbeiter, Team) .. Teamzuordnung

' Benutzer und Mitarbeiter
Benutzer "1" --> "1" Mitarbeiter : verknuepft mit >

' Benachrichtigungen
Projekt "1" --> "0..*" Benachrichtigung : ausgeloest >

@enduml
```

## Diagrammbeschreibung

Das Domänenklassendiagramm modelliert den fachlichen Problembereich der Best-Pro-Software
**ohne technische Implementierungsdetails**. Es zeigt ausschließlich fachlich relevante
Klassen, ihre Attribute und die Beziehungen zwischen ihnen. Methoden sind bewusst nicht
dargestellt.

### Zentrale Klasse Projekt

Das `Projekt` steht im Mittelpunkt des gesamten Datenmodells. Es besitzt eine **rekursive
Kompositionsbeziehung** zu sich selbst (`0..1` zu `0..*`), was die beliebig tiefe
Verschachtelung von Unterprojekten ermöglicht. Ein Projekt ohne übergeordnetes Projekt
ist ein Wurzelprojekt.

Jedes Projekt ist:

- genau **einem Kunden** zugeordnet (1:1)
- von genau **einem Mitarbeiter** geleitet
- optional mit **mehreren Teams und einzelnen Mitarbeitern** verknüpft

Die Attribute `kalkulierteGesamtkosten`, `bisherigKosten` und `erfuellungsgrad` bilden
die rechnerische Grundlage für das Ampelsystem.

### Kostenpositionen

Einem Projekt sind drei verschiedene Arten von Kostenpositionen zugeordnet:

| Art | Klasse | Beschreibung |
|---|---|---|
| Stundenbudget | `Projekttaetigkeit` | Definiert `maxStunden × stundensatz` als Budget-Referenz für Zeitbuchungen |
| Dienstleister | `ExterneKosten` | Pauschalbeträge externer Rechnungen, kein Mitarbeiterbezug |
| Mitarbeiteraktionen | `Aufwandsbuchung` | Abstrakte Superklasse, konkretisiert als `Zeitbuchung` oder `Materialbuchung` |

Sowohl `Zeitbuchung` (Stunden × Stundensatz) als auch `Materialbuchung` (Sachkosten mit
Belegnummer) erhöhen die `bisherigenKosten` des Projekts.

### Mitarbeiter und Teams

Ein Mitarbeiter kann mehreren Teams angehören (**n:m-Beziehung**), abgebildet durch die
Assoziationsklasse `Teamzuordnung` mit eigenem `eintrittsdatum` und `rolle`.

Das Attribut `istProjektleiter` steuert, ob ein Mitarbeiter Projekte anlegen darf.
Ausgeschiedene Mitarbeiter erhalten den Status `INAKTIV` — sie werden **nicht gelöscht**,
damit historische Buchungen erhalten bleiben.

### Benutzer und Berechtigungen

Die Klasse `Benutzer` repräsentiert den Systemzugang und ist genau einem `Mitarbeiter`
zugeordnet. Die Benutzerrolle (`Enum`: `MITARBEITER`, `PROJEKTLEITER`, `GESCHAEFTSFUEHRUNG`,
`ADMIN`) steuert alle Zugriffsberechtigungen.

!!! info "Trennung Mitarbeiter / Benutzer"
    Durch diese Trennung ist es möglich, dass ein Mitarbeiter **existiert, ohne Systemzugang**
    zu haben — zum Beispiel als historischer Datensatz oder vor der Benutzeranlage durch
    den Administrator.

### Automatisierte Klassen

- **`Benachrichtigung`** protokolliert alle ausgehenden E-Mails und ermöglicht durch den
  `VersandStatus` (`AUSSTEHEND`, `GESENDET`, `FEHLER`) eine Wiederholungslogik.
- **`Rechnung`** wird bei Projektabschluss automatisch erzeugt und referenziert die
  generierte PDF-Datei über einen Dateipfad (`pdfPfad`).

---

## Enumerationen

| Enum | Werte | Verwendung |
|---|---|---|
| `AmpelStatus` | `GRUEN`, `GELB`, `ROT` | Projektstatus-Anzeige |
| `ProjektStatus` | `AKTIV`, `ABGESCHLOSSEN`, `PAUSIERT` | Projektlebenszyklus |
| `BuchungsTyp` | `ZEIT`, `MATERIAL` | Buchungsunterscheidung |
| `MitarbeiterStatus` | `AKTIV`, `INAKTIV` | Soft-Delete für Mitarbeiter |
| `Benutzerrolle` | `MITARBEITER`, `PROJEKTLEITER`, `GESCHAEFTSFUEHRUNG`, `ADMIN` | Zugriffssteuerung |
| `VersandStatus` | `AUSSTEHEND`, `GESENDET`, `FEHLER` | E-Mail-Tracking |
