---
title: Systemsequenzdiagramme
tags:
  - Analyse
  - Sequenzdiagramm
  - UML
---

# Systemsequenzdiagramme (SSD)

Die zehn Systemsequenzdiagramme zeigen die Interaktion zwischen Akteuren
und dem System auf hoher Abstraktionsebene. Interne Systemdetails werden
**nicht** dargestellt.

---

## SSD-01 – Projekt anlegen {#ssd-01}

> **Verantwortlich:** Mitglied 1

Zeigt die Interaktion beim Anlegen eines neuen Projekts. Das System validiert
die Eingaben, vergibt eine Projektnummer und initialisiert den Ampelstatus.

!!! note "Leseanleitung"
    Das Diagramm liest sich von oben nach unten als zeitlicher Ablauf. Der Projektleiter
    eröffnet den Dialog mit `neuesProjektOeffnen()`. Das System antwortet mit dem Anzeigeformular.
    Anschließend übergibt der Nutzer in drei aufeinanderfolgenden Nachrichten die Stammdaten,
    Tätigkeiten und Teamzuordnungen. Nach dem Speicheraufruf führt das System intern drei
    Aktionen aus (erkennbar an den Selbst-Nachrichten `SYS→SYS`): Pflichtfeldvalidierung,
    automatische Projektnummernvergabe und Initialisierung des Ampelstatus auf `GRÜN`. Erst
    dann wird der Projektleiter mit einer Bestätigungsnachricht informiert. Der gestrichelte
    Rückpfeil kennzeichnet jeweils eine Systemantwort.

```puml
@startuml SSD01_ProjektAnlegen
actor "Projektleiter" as PL
participant "System" as SYS

PL -> SYS : neuesProjektOeffnen()
SYS --> PL : zeigeProjektformular()
PL -> SYS : projektdatenEingeben(bezeichnung, kunde, startdatum, enddatum, kosten)
PL -> SYS : taetigkeitenDefinieren(taetigkeiten[])
PL -> SYS : teamZuordnen(mitarbeiter[], teams[])
PL -> SYS : projektSpeichern()
SYS -> SYS : validierePflichtfelder()
SYS -> SYS : vergibProjektnummer()
SYS -> SYS : initialisiereAmpel(GRUEN)
SYS --> PL : zeigeBestaetigung(projektnummer)
@enduml
```

---

## SSD-02 – Ampelstatus prüfen & E-Mail senden {#ssd-02}

> **Verantwortlich:** Mitglied 1

Beschreibt den automatischen Prozess nach jeder Kostenbuchung: System berechnet
Kosten- und Terminfortschritt, setzt Ampelstatus und sendet ggf. Warn-E-Mail.

!!! note "Leseanleitung"
    Dieses Diagramm zeigt **drei Akteure gleichzeitig**: Mitarbeiter (Auslöser), System
    (Verarbeiter) und Projektleiter (Empfänger). Besonders zu beachten ist der `alt`-Block
    (alternatives Fragment), der drei mögliche Pfade darstellt:

    - **Rot-Zweig:** Kosten ≥ 100 % oder Termin überschritten → Ampel auf ROT, sofortiger E-Mail-Versand
    - **Gelb-Zweig:** Kosten 80–99 % oder Termin < 14 Tage → Ampel auf GELB, E-Mail-Versand
    - **Grün-Zweig (else):** Alles im Rahmen → Ampel bleibt GRÜN, keine E-Mail

    Das Diagramm verdeutlicht, dass der Projektleiter **keine aktive Rolle** spielt, sondern
    lediglich als Nachrichtenempfänger erscheint.

```puml
@startuml SSD02_AmpelUndEmail
actor "Mitarbeiter" as MA
participant "System" as SYS
actor "Projektleiter" as PL

MA -> SYS : buchungSpeichern(stunden, taetigkeit)
SYS -> SYS : aktualisiereKosten()
SYS -> SYS : berechneAmpelstatus()

alt Kosten >= 100% oder Termin überschritten
  SYS -> SYS : setzeAmpel(ROT)
  SYS -> PL : sendeEmail(betreff, projektname, details)
else Kosten 80–99% oder Termin < 14 Tage
  SYS -> SYS : setzeAmpel(GELB)
  SYS -> PL : sendeEmail(betreff, projektname, details)
else Alles ok
  SYS -> SYS : setzeAmpel(GRUEN)
end

SYS --> MA : zeigeAktualisiertesProjekt(ampelstatus)
@enduml
```

---

## SSD-03 – Aufwand (Zeit) buchen {#ssd-03}

> **Verantwortlich:** Mitglied 2

Ein Mitarbeiter bucht geleistete Arbeitsstunden. Das System berechnet die
Kosten und aktualisiert den Projektstand.

!!! note "Leseanleitung"
    Das Diagramm ist **zweigeteilt**: Die erste Hälfte (bis `buchungBestaetigen`) stellt den
    interaktiven Teil dar, in dem der Mitarbeiter schrittweise Projekt, Tätigkeit und
    Buchungsdaten auswählt — das System antwortet jeweils mit den verfügbaren Optionen
    (z. B. Tätigkeitsliste). In der zweiten Hälfte folgen vier interne Systemaktionen
    (`SYS→SYS`): Kostenberechnung (`Stunden × Stundensatz`), Persistierung der Buchung,
    Aktualisierung der Projektkosten und Ampelstatusüberprüfung. Eine einzelne Buchungsaktion
    löst somit eine ganze Kette von Systemreaktionen aus.

```puml
@startuml SSD03_AufwandBuchen
actor "Mitarbeiter" as MA
participant "System" as SYS

MA -> SYS : aufwandBuchenOeffnen()
SYS --> MA : zeigeProjektliste(zugeordneteProjekte)
MA -> SYS : projektAuswaehlen(projektId)
SYS --> MA : zeigeTaetigkeiten(taetigkeiten[])
MA -> SYS : buchungseingaben(datum, stunden, taetigkeit, beschreibung)
SYS -> SYS : berechneKosten(stunden * stundensatz)
MA -> SYS : buchungBestaetigen()
SYS -> SYS : speichereBuchung()
SYS -> SYS : aktualisiereKosten(projekt)
SYS -> SYS : pruefeAmpelstatus()
SYS --> MA : zeigeBestaetigung(buchungsdetails)
@enduml
```

---

## SSD-04 – Materialbuchung erfassen {#ssd-04}

> **Verantwortlich:** Mitglied 2

Ein Mitarbeiter bucht Materialkosten. Der Ablauf unterscheidet sich von der
Zeitbuchung durch fehlende Tätigkeitsauswahl und direkte Kostenangabe.

!!! note "Leseanleitung"
    Im Vergleich zu SSD-03 entfällt die **Tätigkeitsauswahl**, da Materialkosten nicht an
    eine definierte Tätigkeit gebunden sind, sondern direkt als Eurobetrag erfasst werden.
    Das Diagramm zeigt, dass das System vor dem Speichern eine Betragvalidierung durchführt
    (`validiereBetrag > 0`) — eine der wenigen explizit sichtbaren Validierungsregeln auf
    Systemebene. Der anschließende interne Ablauf ist identisch mit SSD-03: Buchung speichern,
    Gesamtkosten aktualisieren, Ampelstatus prüfen.

```puml
@startuml SSD04_MaterialBuchen
actor "Mitarbeiter" as MA
participant "System" as SYS

MA -> SYS : materialTabOeffnen()
SYS --> MA : zeigeProjektliste()
MA -> SYS : projektAuswaehlen(projektId)
MA -> SYS : materialEingeben(bezeichnung, menge, einheit, betrag, belegnr)
SYS -> SYS : validiereBetrag(betrag > 0)
MA -> SYS : buchungSpeichern()
SYS -> SYS : erzeugeMaterialbuchung()
SYS -> SYS : aktualisiereGesamtkosten()
SYS -> SYS : pruefeAmpelstatus()
SYS --> MA : zeigeErfolgsmeldung()
@enduml
```

---

## SSD-05 – PDF-Projektübersicht exportieren {#ssd-05}

> **Verantwortlich:** Mitglied 3

Der Nutzer exportiert eine vollständige Projektübersicht als PDF. Das System
sammelt rekursiv alle Unterprojekte und Kostenpositionen.

!!! note "Leseanleitung"
    Auffällig ist, dass **fast alle Aktionen** als Selbst-Nachrichten (`SYS→SYS`) erscheinen:
    Das System prüft zunächst die Berechtigung des anfragenden Nutzers, lädt danach rekursiv
    alle Unterprojektdaten und schließlich alle Kostenpositionen. Erst nach diesen
    Vorbereitungsschritten wird der PDF-Generator aufgerufen. Der Nutzer sieht lediglich
    den Auslöse-Klick und den finalen Download-Link. Das Diagramm verdeutlicht, dass die
    PDF-Generierung für komplexe Projekthierarchien mehrere interne Ladeschritte erfordert.

```puml
@startuml SSD05_PDFExport
actor "Projektleiter" as PL
participant "System" as SYS

PL -> SYS : pdfExportKlicken(projektId)
SYS -> SYS : pruefeBerechtigung(nutzer, projekt)
SYS -> SYS : ladeProjektdaten(rekursiv alle Unterprojekte)
SYS -> SYS : ladeKostenpositionen(alle Buchungen)
SYS -> SYS : generierePDF(projektdaten)
SYS --> PL : liefereDownload(pdfDatei)
@enduml
```

---

## SSD-06 – Projekt abschließen & Rechnung erstellen {#ssd-06}

> **Verantwortlich:** Mitglied 3

Der Projektleiter schließt ein Projekt ab. Das System bestätigt den Abschluss,
sperrt weitere Buchungen und erstellt automatisch eine Kundenrechnung als PDF.

!!! note "Leseanleitung"
    Das Diagramm zeigt ein explizites **Bestätigungsmuster**: Nach dem ersten Klick des
    Projektleiters antwortet das System mit einem Bestätigungsdialog, bevor der eigentliche
    Abschluss erfolgt. Erst nach der zweiten Bestätigung folgt die Kette der Systemaktionen:
    Status setzen → Buchungen sperren → Kostenpositionen aggregieren → Rechnungsnummer
    vergeben → PDF erzeugen. Dieser zweistufige Ablauf **schützt vor versehentlichem
    Abschluss**. Das Diagramm zeigt außerdem, dass die Rechnungserstellung keine separate
    Nutzeraktion erfordert, sondern automatisch und atomar mit dem Abschluss erfolgt.

```puml
@startuml SSD06_ProjektAbschluss
actor "Projektleiter" as PL
participant "System" as SYS

PL -> SYS : projektAbschliessenKlicken(projektId)
SYS --> PL : zeigeBestaetigung(dialog)
PL -> SYS : abschlussBestaetigen()
SYS -> SYS : setzeStatusAbgeschlossen()
SYS -> SYS : sperreWeitereKostenbuchungen()
SYS -> SYS : aggregiereKostenpositionen()
SYS -> SYS : vergibRechnungsnummer()
SYS -> SYS : generiereRechnungPDF(kundendetails, positionen)
SYS --> PL : zeigeDownloadlink(rechnung.pdf)
@enduml
```

---

## SSD-07 – Mitarbeiter anlegen {#ssd-07}

> **Verantwortlich:** Mitglied 4

Ein Administrator legt einen neuen Mitarbeiter an. Das System prüft die
Eindeutigkeit der Personalnummer und speichert den Datensatz.

!!! note "Leseanleitung"
    Das Diagramm unterscheidet **zwei Eingabephasen**: Zuerst die Pflichtdaten
    (Personalnummer, Name, Rolle, Stundensatz, Projektleiter-Flag), dann optional die
    Teamzuordnung. Die kritische Systemlogik ist die Prüfung der Personalnummer auf
    Eindeutigkeit (`pruefePersonalnummerEindeutig`), die vor dem Speichern erfolgt. Erst
    wenn diese Prüfung positiv ausfällt, wird der Mitarbeiter mit Status `AKTIV` persistiert.
    Das Diagramm zeigt bewusst **keinen Fehlerfall** — Systemsequenzdiagramme stellen
    typischerweise den Erfolgsfall dar; Fehlerfälle sind in der UC-Schablone beschrieben.

```puml
@startuml SSD07_MitarbeiterAnlegen
actor "Admin" as ADM
participant "System" as SYS

ADM -> SYS : neuerMitarbeiterOeffnen()
SYS --> ADM : zeigeFormular()
ADM -> SYS : mitarbeiterdatenEingeben(pnr, name, rolle, stundensatz, istPL)
ADM -> SYS : teamZuordnenOptional(teams[])
ADM -> SYS : speichern()
SYS -> SYS : pruefePersonalnummerEindeutig(pnr)
SYS -> SYS : speichereMitarbeiter(status=AKTIV)
SYS --> ADM : zeigeBestaetigung(mitarbeiterId)
@enduml
```

---

## SSD-08 – Benutzer anlegen & Rolle zuweisen {#ssd-08}

> **Verantwortlich:** Mitglied 4

Ein Administrator richtet einen Systemzugang ein, weist die Benutzerrolle zu
und das System versendet eine Einladungsmail.

!!! note "Leseanleitung"
    Dieses Diagramm stellt als einziges einen **asynchronen Prozess über zwei Sitzungen**
    hinweg dar: die Benutzeranlage durch den Administrator und die spätere Passwort-Festlegung
    durch den neuen Nutzer. Nach dem Speichern durch den Administrator durchläuft das System
    intern zwei Schritte (E-Mail-Prüfung, Benutzer erstellen), bevor es eine Einladungsmail
    sendet. Die letzten drei Nachrichten repräsentieren eine **zeitlich spätere, separate
    Aktion**: Der neue Nutzer folgt dem Link, setzt sein Passwort und wird danach aktiviert.
    Dieser Zeitsprung ist bewusst im selben Diagramm dargestellt, um den vollständigen
    Onboarding-Prozess abzubilden.

```puml
@startuml SSD08_BenutzerAnlegen
actor "Admin" as ADM
participant "System" as SYS
actor "Neuer Benutzer" as NB

ADM -> SYS : neuerBenutzerOeffnen()
ADM -> SYS : benutzerdatenEingeben(email, rolle)
ADM -> SYS : mitarbeiterVerknuepfen(mitarbeiterId)
ADM -> SYS : speichern()
SYS -> SYS : pruefeEmailEindeutig(email)
SYS -> SYS : erstelleBenutzer()
SYS -> NB : sendeEinladungsmail(resetLink)
NB -> SYS : passwortSetzen(neuesPasswort)
SYS -> SYS : aktiviereBenutzer()
SYS --> NB : loginMoeglich()
@enduml
```

---

## SSD-09 – Team anlegen und Mitarbeiter zuordnen {#ssd-09}

> **Verantwortlich:** Mitglied 5

Ein Projektleiter erstellt ein neues Team und weist Mitarbeiter zu.

!!! note "Leseanleitung"
    Das Diagramm beginnt mit der Systemreaktion auf den Öffnungsdialog: Das System liefert
    die Liste aller **aktiven** Mitarbeiter. Der Projektleiter übergibt Teamname, Beschreibung
    und die gewählten Mitarbeiter-IDs als Array. Intern erzeugt das System das Team und
    erstellt danach für jeden Mitarbeiter einzeln eine Mitgliedschaft
    (`erstelleMitgliedschaften` mit Array). Die Bestätigungsnachricht enthält bewusst die
    **Anzahl der Mitglieder**, damit der Nutzer sofort sieht, ob alle gewünschten Zuordnungen
    erfolgreich waren.

```puml
@startuml SSD09_TeamAnlegen
actor "Projektleiter" as PL
participant "System" as SYS

PL -> SYS : neuesTeamOeffnen()
SYS --> PL : zeigeMitarbeiterliste(aktive)
PL -> SYS : teamdatenEingeben(teamname, beschreibung)
PL -> SYS : mitarbeiterAuswaehlen(mitarbeiterIds[])
PL -> SYS : teamSpeichern()
SYS -> SYS : speichereTeam()
SYS -> SYS : erstelleMitgliedschaften(mitarbeiterIds[])
SYS --> PL : zeigeBestaetigung(teamId, anzahlMitglieder)
@enduml
```

---

## SSD-10 – Kunden anlegen {#ssd-10}

> **Verantwortlich:** Mitglied 5

Ein Administrator legt einen neuen Kunden an. Der Kunde steht danach
in der Projektanlage zur Auswahl bereit.

!!! note "Leseanleitung"
    Der strukturell einfachste der zehn Abläufe verdeutlicht dennoch zwei wichtige
    systemseitige Validierungsschritte: Das System führt vor dem Speichern **zwei parallele
    Prüfungen** durch — die Eindeutigkeit der Kundennummer und die Korrektheit des
    E-Mail-Formats. Erst wenn beide Validierungen positiv ausfallen, wird der Kunde
    persistiert. Der kompakte Aufbau dieses Diagramms spiegelt die vergleichsweise einfache
    Fachlichkeit der Kundenverwaltung wider, die **keine komplexen Folgeaktionen** wie
    Rechnungsgenerierung oder Ampelprüfung auslöst.

```puml
@startuml SSD10_KundeAnlegen
actor "Admin" as ADM
participant "System" as SYS

ADM -> SYS : neuerKundeOeffnen()
SYS --> ADM : zeigeKundenformular()
ADM -> SYS : kundendatenEingeben(kundennummer, name, adresse, kontakt)
ADM -> SYS : speichern()
SYS -> SYS : pruefeKundennummerEindeutig(nr)
SYS -> SYS : validiereEmailFormat(email)
SYS -> SYS : speichereKunde()
SYS --> ADM : zeigeBestaetigung(kundenId)
@enduml
```
