---
title: API Testing
tags:
  - Entwicklung
  - API
  - Testing
---

# API Testing

Verschiedene Werkzeuge und Beispiele zum Testen der BEST-PRO REST API.

**Basis-URL (lokal):** `http://localhost:8081/api`

---

## Authentifizierung

Die meisten Endpunkte erfordern ein **JWT Bearer Token**. Token zuerst holen:

```bash
curl -s -X POST http://localhost:8081/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"benutzername": "pl.mueller", "passwort": "pl123"}' | jq .
```

```json
{
  "token": "eyJhbGciOiJIUzI1NiJ9...",
  "rolle": "PROJEKTLEITER",
  "mitarbeiterId": 3
}
```

Token als Variable speichern:

```bash
TOKEN=$(curl -s -X POST http://localhost:8081/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"benutzername":"pl.mueller","passwort":"pl123"}' | jq -r .token)

echo $TOKEN   # Token anzeigen
```

---

## cURL – Wichtige Endpunkte

### Projekte

```bash
# Alle Projekte (gefiltert nach Rolle)
curl -s -H "Authorization: Bearer $TOKEN" \
     http://localhost:8081/api/projekte | jq .

# Einzelnes Projekt
curl -s -H "Authorization: Bearer $TOKEN" \
     http://localhost:8081/api/projekte/1 | jq .

# Neues Projekt anlegen
curl -s -X POST \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "bezeichnung": "Testprojekt",
       "kundeId": 1,
       "projektleiterId": 3,
       "startdatum": "2026-05-01",
       "enddatum": "2026-12-31",
       "kalkulierteGesamtkosten": 50000.00
     }' \
     http://localhost:8081/api/projekte | jq .

# Projekt abschließen
curl -s -X POST \
     -H "Authorization: Bearer $TOKEN" \
     http://localhost:8081/api/projekte/1/abschliessen | jq .

# PDF exportieren (speichert Datei lokal)
curl -s -H "Authorization: Bearer $TOKEN" \
     http://localhost:8081/api/projekte/1/pdf \
     -o projekt_1_export.pdf
```

### Buchungen

```bash
# Zeitbuchung erfassen
curl -s -X POST \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "projektId": 1,
       "projekttaetigkeitId": 2,
       "datum": "2026-04-24",
       "stunden": 8.0,
       "beschreibung": "Implementierung Login-Modul"
     }' \
     http://localhost:8081/api/buchungen/zeit | jq .

# Materialbuchung erfassen
curl -s -X POST \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "projektId": 1,
       "materialbezeichnung": "Testserver SSD",
       "menge": 2,
       "einheit": "Stück",
       "betrag": 149.99,
       "belegnummer": "RE-2026-0042"
     }' \
     http://localhost:8081/api/buchungen/material | jq .
```

### Mitarbeiter

```bash
# Alle Mitarbeiter (GF/Admin)
curl -s -H "Authorization: Bearer $TOKEN" \
     http://localhost:8081/api/mitarbeiter | jq .

# Neuen Mitarbeiter anlegen
curl -s -X POST \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "personalnummer": "1005",
       "nachname": "Schmidt",
       "vorname": "Lisa",
       "rolle": "Entwicklerin",
       "stundensatz": 95.00,
       "istProjektleiter": false
     }' \
     http://localhost:8081/api/mitarbeiter | jq .
```

### Kunden

```bash
# Alle Kunden
curl -s -H "Authorization: Bearer $TOKEN" \
     http://localhost:8081/api/kunden | jq .

# Neuen Kunden anlegen
curl -s -X POST \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "kundennummer": "K010",
       "name": "Neue GmbH",
       "strasse": "Musterstraße 1",
       "plz": "32756",
       "ort": "Detmold",
       "land": "Deutschland",
       "telefon": "05231-123456",
       "email": "kontakt@neue-gmbh.de",
       "ansprechpartner": "Max Muster"
     }' \
     http://localhost:8081/api/kunden | jq .
```

---

## REST Client (VS Code Extension)

Erstelle eine Datei `requests.http` im Projekt-Root:

```http
### Variablen
@baseUrl = http://localhost:8081/api
@contentType = application/json

### 1. Login
# @name login
POST {{baseUrl}}/auth/login
Content-Type: {{contentType}}

{
  "benutzername": "pl.mueller",
  "passwort": "pl123"
}

### Token aus Login-Response verwenden
@token = {{login.response.body.token}}

### 2. Alle Projekte
GET {{baseUrl}}/projekte
Authorization: Bearer {{token}}

### 3. Zeitbuchung
POST {{baseUrl}}/buchungen/zeit
Authorization: Bearer {{token}}
Content-Type: {{contentType}}

{
  "projektId": 1,
  "projekttaetigkeitId": 1,
  "datum": "2026-04-24",
  "stunden": 6.5,
  "beschreibung": "Frontend Routing"
}

### 4. Health Check (kein Token nötig)
GET http://localhost:8081/actuator/health
```

**Nutzung:** Klick auf `Send Request` über der jeweiligen Anfrage.

---

## Thunder Client (VS Code)

1. Extension installieren: `rangav.vscode-thunder-client`
2. Thunder-Icon in der Sidebar öffnen
3. **New Request** → Methode, URL, Headers und Body eintragen
4. Collections für BEST-PRO anlegen und mit dem Team teilen

---

## Postman

### Collection importieren

Sobald Swagger/OpenAPI verfügbar ist:

```bash
# OpenAPI-Spec herunterladen
curl http://localhost:8081/v3/api-docs -o bestpro-api.json
```

In Postman: `Import → bestpro-api.json` → Collection wird automatisch erstellt.

### Environment einrichten

| Variable | Wert |
|---|---|
| `baseUrl` | `http://localhost:8081/api` |
| `token` | *(nach Login automatisch befüllen)* |

---

## HTTP Status Codes – Referenz

| Code | Bedeutung | Häufige Ursache |
|---|---|---|
| `200 OK` | Erfolg | — |
| `201 Created` | Ressource angelegt | POST erfolgreich |
| `204 No Content` | Erfolg ohne Body | DELETE/PUT |
| `400 Bad Request` | Validierungsfehler | Pflichtfeld fehlt |
| `401 Unauthorized` | Kein/ungültiger Token | Neu einloggen |
| `403 Forbidden` | Keine Berechtigung | Falsche Rolle |
| `404 Not Found` | Ressource nicht gefunden | ID falsch |
| `409 Conflict` | Duplikat | Projektnummer bereits vergeben |
| `500 Internal Server Error` | Backend-Fehler | Logs prüfen |

---

## Swagger UI

Sobald das Backend läuft, ist die interaktive API-Doku erreichbar unter:

`http://localhost:8081/swagger-ui/index.html`

Dort können alle Endpunkte direkt im Browser getestet werden.

---

## Siehe auch

- [API Endpunkte](api/endpunkte.md)
- [Authentifizierung](api/authentifizierung.md)
- [Debugging](debugging.md)
- [VS Code Extensions](ide-setup/vscode-erweiterungen.md)
