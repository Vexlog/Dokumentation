---
title: BEST-PRO Dokumentation
description: Zentrale Wissensdatenbank für das BEST-PRO Projektmanagementsystem
tags:
  - Übersicht
---

# BEST-PRO – Entwicklerdokumentation

> **Modul:** Softwareprojekt (5 WI(P) 28) | **Semester:** SS 2026  
> **Studiengang:** Bachelor Wirtschaftsinformatik

---

## Was ist BEST-PRO?

Best-Pro ist ein webbasiertes **Projektmanagementsystem**, das das Unternehmen Best-Pro bei der
Steuerung und Überwachung seiner Projekte unterstützt. Bisherige Werkzeuge (Excel, Office-Tools)
stoßen an ihre Grenzen – BEST-PRO ersetzt sie durch eine zentrale, rollenbasierte Softwarelösung.

### Kernfunktionen auf einen Blick

| Bereich | Beschreibung |
|---|---|
| 📁 **Projektverwaltung** | Projekte & beliebig tiefe Unterprojekte anlegen, bearbeiten, abschließen |
| 🚦 **Ampelsystem** | Automatische Kosten-/Terminüberwachung mit visueller Warnung & E-Mail |
| 👥 **Mitarbeiterverwaltung** | Mitarbeiter, Teams & Rollen verwalten |
| 🏢 **Kundenverwaltung** | Kundenstammdaten pflegen, Projekten zuordnen |
| ⏱ **Aufwandsbuchung** | Zeitbuchungen und Materialbuchungen je Projekttätigkeit |
| 📄 **PDF-Export** | Projektübersicht & automatische Kundenrechnung bei Abschluss |
| 🔐 **Berechtigungskonzept** | Rollenbasierter Zugriff (Mitarbeiter / PL / GF / Admin) |

---

## Schnellnavigation

<div class="grid cards" markdown>

-   :clipboard: **Anforderungen**

    ---

    Use Cases, User Stories und detaillierte Anforderungsbeschreibungen

    [:octicons-arrow-right-24: Zur Anforderungsübersicht](anforderungen/index.md)

-   :mag: **Analyse**

    ---

    Domänenklassendiagramm und Systemsequenzdiagramme (PlantUML)

    [:octicons-arrow-right-24: Zur Analyse](analyse/index.md)

-   :art: **Design**

    ---

    Mockups aller Bildschirmmasken und vollständiger Styleguide

    [:octicons-arrow-right-24: Zum Design](design/index.md)

-   :hammer_and_wrench: **Entwicklung**

    ---

    Setup, Architektur, Datenbankschema und Coding Guidelines

    [:octicons-arrow-right-24: Zur Entwicklung](entwicklung/index.md)

</div>

---

## Projekteckdaten

| Feld | Wert |
|---|---|
| **Modul** | Softwareprojekt (5 WI(P) 28) |
| **Semester** | Sommersemester 2026 |
| **Kick-Off** | 22.04.2026 |
| **Abgabe Projektbericht** | 03.07.2026 |
| **Nächster Meilenstein** | [1. Meilensteintreffen – 06.05.2026](projekt/meilensteine.md) |

---

## Wie diese Dokumentation funktioniert

!!! info "Lebende Dokumentation"
    Diese Doku wächst mit dem Projekt. Jedes Teammitglied pflegt **seinen Bereich** direkt in den
    Markdown-Dateien. Änderungen werden über Git versioniert und sind im Footer jeder Seite sichtbar.

!!! tip "PlantUML-Diagramme"
    Alle UML-Diagramme sind als **PlantUML-Code** eingebettet und werden beim Build automatisch
    gerendert. Den Code findest du direkt auf der jeweiligen Seite – einfach bearbeiten und committen.

!!! warning "Noch nicht fertig?"
    Seiten mit dem Badge `🚧 In Bearbeitung` sind Platzhalter und werden während der Entwicklung
    befüllt. Trage dort ein, sobald du Inhalte ergänzt hast.