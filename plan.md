## Plan: TIPI Tutorial 0-5 Struktur

Der Lernpfad bleibt bei Level 0 bis Level 5. Level 0 ist der Einstieg, Level 1-5 bilden den Kern der Transformation von einem einzelnen Trainingsskript zu einem verwaltbaren TIPI-CLI-Prozess. DemoPipeline wird als Referenz für Struktur und Denkmodell genutzt, aber nicht als 1:1 Kopie. Scope bleibt ohne CI/CD, Container oder Cloud-Deployment.

**Steps**
1. Phase A - Dokumentationsfundament angleichen
1.1 Navigation in MkDocs auf den vollständigen Pfad vorbereiten (bestehende Level sichtbar, fehlende Level vorgesehen).
1.2 README in eine Roadmap umformen: Zielbild, Zielgruppe, Lernpfad, erwartete Resultate je Stufe.
1.3 Sprachliche Konsistenz über alle Levels sicherstellen (Terminologie, Übergänge, Nutzenargumentation).

2. Phase B - Einheitliche Kapitelstruktur pro Level umsetzen (depends on 1)
2.1 Jedes Level-Dokument folgt exakt derselben Gliederung:
- Lernziel
- Vorher / Nachher
- Aufgaben
- Ergebnis
- Troubleshooting
2.2 Für jedes Level einen kurzen Abschnitt "Warum dieser Schritt produktionsnäher ist" integrieren.
2.3 Pro Level mindestens einen reproduzierbaren CLI-Aufruf dokumentieren.

3. Phase C - Level-spezifische Inhalte definieren (depends on 2)
3.1 Level 0 - Einstieg (bereits vorhanden, in Struktur überführen)
- Lernziel: Lokales Setup, erstes lauffähiges Trainingsskript, Verständnis der Ausgangsbasis.
- Vorher/Nachher: Kein Projektzustand -> lauffähiges Basisskript mit festen Parametern.
- Aufgaben: Environment aufsetzen, FashionMNIST laden, Trainings/Testloop ausführen.
- Ergebnis: Skript läuft reproduzierbar, Modell wird gespeichert.
- Troubleshooting: Dependency-Fehler, Datendownload, Device-Auswahl.

3.2 Level 1 - Refactoring in Trainer-Klasse (bereits vorhanden, schärfen)
- Lernziel: Logik von Main-Skript in wiederverwendbare Klasse verschieben.
- Vorher/Nachher: Monolithischer Loop im Skript -> gekapselte Methoden in Trainer.
- Aufgaben: train/test Loop auslagern, run_epochs zentralisieren, State sauber verwalten.
- Ergebnis: Gleiches Verhalten wie Level 0, aber modulare Struktur.
- Troubleshooting: Importpfade, Typing-Hinweise, Reihenfolge train/eval.

3.3 Level 2 - Erste TIPI-Funktionalität per Decorator (bereits vorhanden, konsolidieren)
- Lernziel: Progress-Tracking via TIPI einführen ohne Kernlogik zu brechen.
- Vorher/Nachher: Nur print-basierte Laufanzeige -> Fortschrittsbalken plus bestehende Ausgabe.
- Aufgaben: progress_task Decorator auf Loop-Methoden anwenden, Ausgabe interpretieren.
- Ergebnis: Sichtbarer Trainingsfortschritt mit TIPI-Baustein.
- Troubleshooting: Decorator-Import, unerwartete Terminaldarstellung, doppelte Ausgabe.

3.4 Level 3 - Skript zu parametrisiertem CLI-Entry (neu)
- Lernziel: Training über CLI-Argumente steuerbar machen.
- Vorher/Nachher: Harte Werte im Code -> Parameter via CLI (z. B. epochs, lr, batch-size, output).
- Aufgaben: Argument-Parser ergänzen, Parameter validieren, an Trainer durchreichen.
- Ergebnis: Reproduzierbarer, variierbarer Aufruf ohne Codeänderung.
- Troubleshooting: Ungültige Argumente, Pfadfehler für Output, Defaults.

3.5 Level 4 - Konfigurationsgetriebener Ablauf (neu)
- Lernziel: Parameter und Laufverhalten über Config-Dateien steuern.
- Vorher/Nachher: Einzelaufruf mit vielen Flags -> zentral versionierbare Konfiguration.
- Aufgaben: Config-Schema definieren, Laden/Validieren integrieren, CLI um config-Flag erweitern.
- Ergebnis: Reproduzierbare Runs über dokumentierte Configs.
- Troubleshooting: Fehlende Config-Felder, Typkonflikte, Priorität CLI-Override vs Config.

3.6 Level 5 - TIPI-nativer verwaltbarer Prozess (neu)
- Lernziel: Aus dem Training-Skript einen klar verwaltbaren TIPI-CLI-Prozess machen.
- Vorher/Nachher: Script-orchestrierter Ablauf -> TIPI-orientierte Prozessstruktur mit klaren Zuständigkeiten.
- Aufgaben: Prozessstruktur nach TIPI-Konzept modellieren, Entry klar benennen, Artefakte konsistent verwalten.
- Ergebnis: Nutzbarer End-to-End CLI-Workflow innerhalb TIPI-Logik.
- Troubleshooting: Prozessregistrierung, Konfigurationskopplung, Laufzeitzustand.

4. Phase D - Umsetzungs- und Abnahmekriterien (depends on 3)
4.1 Definition of Done pro Level verbindlich festhalten.
4.2 Verifikation je Level dokumentieren: Startkommando, erwartete Ausgabe, erwartete Artefakte.
4.3 Cross-Level-Migration dokumentieren: Was wird übernommen, ersetzt oder entfernt.
4.4 Finaler Story-Check: Level 0-5 muss eine lückenlose Skript->CLI->verwaltbarer Prozess Entwicklung zeigen.

**Relevant files**
- /home/admin/Documents/GIT/Tipi-Project/Tutorial/README.md — Roadmap und Gesamtvision 0-5
- /home/admin/Documents/GIT/Tipi-Project/Tutorial/mkdocs.yml — Navigation für konsistenten Lernpfad
- /home/admin/Documents/GIT/Tipi-Project/Tutorial/docs/level_0.md — in Zielstruktur überführen
- /home/admin/Documents/GIT/Tipi-Project/Tutorial/docs/level_1.md — in Zielstruktur überführen
- /home/admin/Documents/GIT/Tipi-Project/Tutorial/docs/level_2.md — in Zielstruktur überführen
- /home/admin/Documents/GIT/Tipi-Project/Tutorial/docs/level_3.md — neu anlegen nach Zielstruktur
- /home/admin/Documents/GIT/Tipi-Project/Tutorial/docs/level_4.md — neu anlegen nach Zielstruktur
- /home/admin/Documents/GIT/Tipi-Project/Tutorial/docs/level_5.md — neu anlegen nach Zielstruktur

**Verification**
1. Jeder Level-Artikel (0-5) enthält exakt die fünf Abschnitte: Lernziel, Vorher/Nachher, Aufgaben, Ergebnis, Troubleshooting.
2. README, mkdocs und Level-Seiten beschreiben denselben Pfad ohne Widersprüche.
3. Für jedes Level existiert mindestens ein ausführbarer, dokumentierter CLI-Aufruf.
4. Level 5 bleibt auf TIPI-bezogene Prozess-Transformation begrenzt (ohne CI/CD).

**Decisions**
- Level 0 bleibt erhalten, Gesamtpfad ist 0-5.
- TIPI CLI ist das primäre Zielbild.
- Level 5 umfasst nur TIPI-relevante Schritte vom Skript zum CLI-Tool.
- DemoPipeline dient als Orientierungsrahmen für Struktur und Prozessdenken.