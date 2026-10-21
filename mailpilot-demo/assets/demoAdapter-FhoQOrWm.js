import{t as e}from"./axios-CIEBgY9x.js";var t=`deepseek/deepseek-v4.1-flash`,n={ANFRAGE:`Sehr geehrte Damen und Herren,

vielen Dank für Ihre Anfrage und Ihr Interesse an unseren Leistungen.

Gerne senden wir Ihnen ein unverbindliches Angebot zu. Damit wir Ihnen die passenden Positionen und eine belastbare Kostenschätzung nennen können, benötigen wir noch einige Angaben zu Ihrem Vorhaben:

- gewünschter Leistungsumfang und Startzeitpunkt
- Anzahl der beteiligten Mitarbeitenden bzw. Nutzer
- bestehende Systeme, die angebunden werden sollen

Sobald uns diese Informationen vorliegen, erhalten Sie das Angebot innerhalb von zwei Werktagen. Für ein kostenloses Erstgespräch schicken wir Ihnen gerne Terminvorschläge.

Mit freundlichen Grüßen
Kundenservice`,REKLAMATION:`Sehr geehrte Damen und Herren,

vielen Dank für Ihre Nachricht. Es tut uns leid, dass die Lieferung nicht einwandfrei ist.

Ihren Fall haben wir umgehend an unseren Kundendienst weitergeleitet. Bitte senden Sie uns, sofern noch nicht geschehen, ein Foto des Defekts sowie die Auftrags- oder Bestellnummer, damit wir den Vorgang eindeutig zuordnen können.

Sie erhalten innerhalb von 24 Stunden eine Rückmeldung mit einem Versandlabel für die Rücksendung. Sobald das Gerät bei uns eingegangen ist, veranlassen wir den Austausch oder die Reparatur und informieren Sie über den weiteren Ablauf.

Wir entschuldigen uns für die entstandenen Unannehmlichkeiten und danken Ihnen für Ihre Geduld.

Mit freundlichen Grüßen
Kundenservice`,RECHNUNG:`Sehr geehrte Damen und Herren,

vielen Dank für Ihre Rückmeldung zur Rechnung und Ihr aufmerksames Prüfen der Positionen.

Wir haben die Rechnung anhand der getroffenen Vereinbarung nachgerechnet und korrigieren die strittige Position. Eine berichtigte Rechnung senden wir Ihnen im Anhang dieser E-Mail zu. Der ursprüngliche Beleg ist damit ungültig; eine bereits gebuchte Zahlung gleichen wir aus.

Für Ihre Unterlagen weisen wir die korrigierten Beträge gesondert aus. Sollten Sie darüber hinaus eine Position nicht nachvollziehen können, nennen Sie uns bitte die entsprechende Zeile – wir prüfen dies umgehend.

Vielen Dank für Ihr Verständnis.

Mit freundlichen Grüßen
Buchhaltung`,TERMIN:`Sehr geehrte Damen und Herren,

vielen Dank für Ihre Terminanfrage.

Gerne bestätigen wir Ihnen einen Termin aus Ihren Vorschlägen. Bitte teilen Sie uns kurz mit, ob unser Gegenvorschlag für Sie passt; andernfalls nennen wir Ihnen gerne zwei Alternativtermine.

Die geplante Dauer beträgt etwa vier Stunden vor Ort. Für die Durchführung benötigen wir Zugang zu den betroffenen Systemen sowie eine kurze Ansprechperson beim Kunden. Sollte sich an Ihrem Termin etwas ändern, bitten wir um rechtzeitige Benachrichtigung.

Wir freuen uns auf den Termin.

Mit freundlichen Grüßen
Kundenservice`,SPAM:`Sehr geehrte Damen und Herren,

wir haben Ihre Nachricht erhalten und geprüft. Wir nehmen keine Gewinne an, die wir nicht selbst bei einer von uns veranstalteten Aktion erzielt haben, und wir übermitteln keine persönlichen Daten oder Zahlungen für die angebliche Auszahlung eines Gewinns.

Ihre Nachricht wird aus unserem Postfach als Spam markiert und nicht weiter bearbeitet. Eine Rückmeldung an Ihre Adresse unterbleibt, sofern es sich nicht um einen berechtigten Anspruch handelt.

Hinweis für Sie selbst: Senden Sie niemals Ausweiskopien oder Kontodaten an unbekannte Absender. Bei Zweifeln wenden Sie sich bitte direkt an Ihre Bank.

Mit freundlichen Grüßen
Kundenservice`,SONSTIGES:`Sehr geehrte Damen und Herren,

vielen Dank für Ihre Nachricht und Ihr Interesse an einer Zusammenarbeit.

Gerne greifen wir Ihr Anliegen auf. Damit wir einschätzen können, ob und in welcher Form ein Austausch sinnvoll ist, bitten wir um einige kurze Angaben: Worin sehen Sie den möglichen Nutzen für beide Seiten, welche Zeitfenster schweben Ihnen vor und wer wäre Ihr Ansprechpartner?

Wir melden uns nach Eingang Ihrer Rückmeldung mit einem Terminvorschlag für ein kurzes unverbindliches Gespräch.

Mit freundlichen Grüßen
Kundenservice`};function r(e){return n[e]??n.SONSTIGES}var i=new Date,a=e=>String(e).padStart(2,`0`);function o(e){return`${e.getFullYear()}-${a(e.getMonth()+1)}-${a(e.getDate())}T${a(e.getHours())}:${a(e.getMinutes())}:${a(e.getSeconds())}`}function s(e){return`${e.getFullYear()}-${a(e.getMonth()+1)}-${a(e.getDate())}`}function c(e){let t=new Date(i);return t.setDate(t.getDate()-e),t}function l(e){let t=new Date(i);return t.setDate(t.getDate()+e),t}function u(e){return o(new Date(i.getTime()-e*3600*1e3))}function d(e){return o(c(e))}function ee(e){return o(new Date(i.getTime()+e*60*1e3))}function f(e){return`${a(e.getDate())}.${a(e.getMonth()+1)}.${e.getFullYear()}`}function p(e){return e.toLocaleDateString(`de-DE`,{weekday:`long`})}function m(e){return`RE-${e.getFullYear()}-${a(e.getMonth()+1)}${a(e.getDate())}`}var h={id:1,firmenname:`Demo GmbH`,monatlichesLimitUsd:25,limitVerhalten:`HARD_STOP`,fallbackModellId:null,bevorzugtesModellId:null,demoModus:!0,tonalitaet:`FREUNDLICH`,aboStatus:`AKTIV`,trialEndeAm:null,plan:`STANDARD`},g=1,_=h.id,v={token:``,email:`admin@example.com`,vorname:`Anna`,nachname:`Adler`,rolle:`ADMIN`,mandantId:_,firmenname:h.firmenname,demoModus:!0,emailVerifiziert:!0,aboStatus:h.aboStatus,trialEndeAm:h.trialEndeAm,plan:h.plan};function te(){let e={sub:String(g),email:v.email,mandantId:_,rolle:v.rolle,demoModus:v.demoModus,emailVerifiziert:v.emailVerifiziert,aboStatus:v.aboStatus,trialEndeAm:v.trialEndeAm};return`demo-header.${btoa(JSON.stringify(e)).replace(/=+$/,``)}.demo-signatur`}v.token=te();var y={id:1,emailAdresse:`demo@mailpilot.de`,provider:`GMAIL`,aktiv:!0,letzterAbruf:u(1)},b={bestellung:f(c(9)),bestellungErsatz:f(c(7)),lieferung:f(c(2)),rechnung:m(c(11)),vertrag:f(c(60)),forderung:m(c(24)),forderungFrist:f(l(7)),termin1:l(6),termin2:l(7),termin3:l(8),kooperation:`Q${Math.ceil((i.getMonth()+1)/3)} ${i.getFullYear()}`},x={anfrage:`Sehr geehrte Damen und Herren,

ich bin auf der Suche nach einem IT-Beratungsunternehmen, das uns bei der Einführung eines neuen CRM-Systems unterstützen kann. Wir sind ein mittelständisches Unternehmen mit ca. 50 Mitarbeitern. Könnten Sie mir ein unverbindliches Angebot für eine Erstberatung sowie eine grobe Kostenabschätzung zusenden?

Mit freundlichen Grüßen,
Max Mustermann
Geschäftsführer
max.mustermann@example.com`,reklamation:`Sehr geehrte Damen und Herren,

am ${b.bestellung} habe ich bei Ihnen ein Bürogerät (Modell: PrintMaster X200) bestellt. Die Lieferung erfolgte am ${b.lieferung}, jedoch ist das Gerät leider defekt. Der Druckkopf blockiert und es erscheint eine Fehlermeldung, die einen internen Hardware-Fehler anzeigt.

Da ich das Gerät dringend für meinen Geschäftsbetrieb benötige, bitte ich um umgehenden Austausch oder Reparatur. Ich erwarte eine Rückmeldung innerhalb von 24 Stunden.

Mit freundlichen Grüßen,
Anna Schmidt
anna.schmidt@example.com`,bestellung:`Guten Tag,

hiermit bestelle ich verbindlich ein Bürogerät Modell PrintMaster X200 (Bestellnummer: BP-${i.getFullYear()}-1043) zum Angebotspreis. Bitte bestätigen Sie mir den Liefertermin per E-Mail.

Mit freundlichen Grüßen,
Anna Schmidt
anna.schmidt@example.com`,rueckfrage:`Guten Tag,

ich hatte am ${b.bestellung} ein Bürogerät bestellt und noch keine Versandbestätigung erhalten. Können Sie mir den aktuellen Status nennen?

Mit freundlichen Grüßen,
Anna Schmidt
anna.schmidt@example.com`,rechnungEingang:`Guten Tag,

ich habe soeben Ihre Rechnung Nr. ${b.rechnung} über 2.450,00 € erhalten. Leider kann ich die Rechnung nicht ganz nachvollziehen:

- Position 1: IT-Beratung (10h) = 1.800,00 €
- Position 2: Lizenzgebühren (3 Monate) = 650,00 €

Laut unserer Vereinbarung vom ${b.vertrag} sollte der Stundensatz bei 160,00 € liegen, nicht bei 180,00 €. Könnten Sie dies bitte prüfen und korrigieren?

Mit freundlichen Grüßen,
Sabine Wagner
Buchhaltung`,termin:`Sehr geehrte Damen und Herren,

hiermit möchte ich einen Wartungstermin für unsere Serverinfrastruktur vereinbaren. Die letzte Wartung liegt bereits 6 Monate zurück.

Folgende Zeiträume wären bei uns möglich:
- ${p(b.termin1)}, ${f(b.termin1)} ab 10:00 Uhr
- ${p(b.termin2)}, ${f(b.termin2)} ab 14:00 Uhr
- ${p(b.termin3)}, ${f(b.termin3)} ganztägig

Bitte teilen Sie mir mit, welcher Termin für Sie passen würde.

Mit freundlichen Grüßen,
Stefan König
IT-Leiter`,spam:`HERZLICHEN GLÜCKWUNSCH!

Sie sind der glückliche Gewinner von 1.000.000 EURO in unserer Internationalen Online-Lotterie!

Um Ihren Gewinn zu erhalten, senden Sie bitte Ihre persönlichen Daten (Name, Adresse, Bankverbindung, Passkopie) sowie eine Bearbeitungsgebühr von 49,95 € an folgende Adresse:

lottery-claims@example.com

Dies ist Ihre letzte Chance! Nur noch 24 Stunden gültig!

Mit freundlichen Grüßen,
Jane Doe
Gewinnabwicklung`,eskaliert:`Sehr geehrte Damen und Herren,

hiermit fordere ich Sie als bevollmächtigter Rechtsanwalt der Firma Lieferant KG letztmalig auf, die offene Forderung in Höhe von 12.750,00 € aus Rechnung Nr. ${b.forderung} binnen 7 Tagen zu begleichen.

Sollte der Zahlungseingang bis zum ${b.forderungFrist} nicht erfolgen, werde ich ohne weitere Ankündigung gerichtliche Mahnverfahren einleiten und Strafanzeige wegen Untreue stellen.

Des Weiteren behalten wir uns vor, Schadensersatzforderungen sowie Verzugszinsen in Höhe von 9 Prozentpunkten über dem Basiszinssatz geltend zu machen.

Hochachtungsvoll,
RA Dr. Meyer
Fachanwalt für Wirtschaftsrecht
rechtsanwalt@example.org
Tel: +49 30 0000000`,sonstiges:`Guten Tag,

ich bin auf Ihr Unternehmen durch eine Empfehlung von Herrn Klaus Weber aufmerksam geworden. Wir sind eine auf digitale Transformation spezialisierte Unternehmensberatung und suchen für das ${b.kooperation} einen Kooperationspartner im Bereich E-Mail-Automation und KI-gestützter Kundenkommunikation.

Hätten Sie Interesse an einem unverbindlichen Austausch? Ich würde mich freuen, von Ihnen zu hören.

Mit freundlichen Grüßen,
Dr. Julia Richter
Partner Consulting GmbH
info@example.com`},S={anfrage:`Sehr geehrter Herr Mustermann,

vielen Dank für Ihre Anfrage bezüglich unserer IT-Beratungsleistungen.

Gerne unterbreiten wir Ihnen ein unverbindliches Angebot für eine Erstberatung zur CRM-Einführung. Wir würden uns freuen, in einem ersten Gespräch Ihre genauen Anforderungen kennenzulernen.

Bitte teilen Sie uns mit, ob wir Ihnen einen Terminvorschlag für ein kostenloses Erstgespräch zusenden sollen.

Mit freundlichen Grüßen,
Ihr MailPilot-Team`,reklamation:`Sehr geehrte Frau Schmidt,

vielen Dank für Ihre Nachricht. Es tut uns leid, dass Sie ein defektes Gerät erhalten haben.

Ich habe Ihren Fall umgehend an unseren Kundendienst weitergeleitet. Wir kümmern uns selbstverständlich umgehend um einen Austausch.

Sie erhalten bis morgen früh eine separate E-Mail mit einem Versandlabel für die Rücksendung des defekten Geräts sowie der Bestätigung für den Versand eines Ersatzgeräts.

Wir entschuldigen uns für die Unannehmlichkeiten.

Mit freundlichen Grüßen,
Ihr MailPilot-Team`,rechnung:`Sehr geehrte Frau Wagner,

vielen Dank für Ihre Rückmeldung zur Rechnung Nr. ${b.rechnung}.

Sie haben vollkommen recht – der vereinbarte Stundensatz beträgt 160,00 €. Es handelt sich hier um einen internen Übertragungsfehler. Ich habe die Korrektur bereits veranlasst und sende Ihnen die berichtigte Rechnung per E-Mail zu.

Der korrekte Betrag lautet:
- Position 1: IT-Beratung (10h × 160,00 €) = 1.600,00 €
- Position 2: Lizenzgebühren (3 Monate) = 650,00 €
- Gesamt: 2.250,00 €

Wir bitten den Fehler zu entschuldigen.

Mit freundlichen Grüßen,
Ihr MailPilot-Team`,termin:`Sehr geehrter Herr König,

vielen Dank für Ihre Terminanfrage bezüglich der Serverwartung.

Gerne bestätige ich Ihnen den Termin am ${p(b.termin3)}, den ${f(b.termin3)}, ab 09:00 Uhr. Unser Techniker wird voraussichtlich ca. 4 Stunden vor Ort sein.

Sollte sich bei Ihnen etwas ändern, bitten wir um rechtzeitige Benachrichtigung.

Mit freundlichen Grüßen,
Ihr MailPilot-Team`},C=`deepseek/deepseek-v4.1-flash`;function w(e,t,n,r,i={}){return{id:e,mailId:t,entwurfText:n,llmModellVerwendet:C,erstelltAm:r,bearbeitetVonUserId:null,finalText:null,versendetAm:null,autoGeneriert:!0,...i}}var T={1:{id:1,absender:`max.mustermann@example.com`,betreff:`Angebot für IT-Beratung`,inhaltRoh:x.anfrage,empfangenAm:u(2),gelesenAm:u(1),status:`ENTWURF_ERSTELLT`,postfachEmail:y.emailAdresse,provider:y.provider,kategorie:`ANFRAGE`,dringlichkeit:`NIEDRIG`,extrahierteDaten:JSON.stringify({Kundenname:`Max Mustermann`,Firma:`Mustermann GmbH`,Anliegen:`Angebot CRM-Beratung`,Referenz:``}),eskalationNoetig:!1,eskalationGrund:null,entwurf:w(1,1,S.anfrage,u(1)),anhangAnzahl:0},2:{id:2,absender:`anna.schmidt@example.com`,betreff:`Defektes Gerät - sofortige Lösung erforderlich`,inhaltRoh:x.reklamation,empfangenAm:u(5),gelesenAm:u(4),status:`ENTWURF_ERSTELLT`,postfachEmail:y.emailAdresse,provider:y.provider,kategorie:`REKLAMATION`,dringlichkeit:`HOCH`,extrahierteDaten:JSON.stringify({Kundenname:`Anna Schmidt`,Firma:``,Anliegen:`Defektes Gerät PrintMaster X200`,Referenz:`Bestellung ${b.bestellung}`}),eskalationNoetig:!1,eskalationGrund:null,entwurf:w(2,2,S.reklamation,u(4)),anhangAnzahl:2},3:{id:3,absender:`buchhaltung@example.org`,betreff:`Frage zu Rechnung Nr. ${b.rechnung}`,inhaltRoh:x.rechnungEingang,empfangenAm:u(8),gelesenAm:u(6),status:`ENTWURF_ERSTELLT`,postfachEmail:y.emailAdresse,provider:y.provider,kategorie:`RECHNUNG`,dringlichkeit:`MITTEL`,extrahierteDaten:JSON.stringify({Kundenname:`Sabine Wagner`,Firma:`Musterfirma GmbH`,Anliegen:`Rechnungskorrektur ${b.rechnung}`,Referenz:`Rechnung ${b.rechnung}`}),eskalationNoetig:!1,eskalationGrund:null,entwurf:w(3,3,S.rechnung,u(6)),anhangAnzahl:1},4:{id:4,absender:`s.koenig@example.com`,betreff:`Terminvereinbarung für Wartung`,inhaltRoh:x.termin,empfangenAm:u(3),gelesenAm:u(2),status:`ENTWURF_ERSTELLT`,postfachEmail:y.emailAdresse,provider:y.provider,kategorie:`TERMIN`,dringlichkeit:`MITTEL`,extrahierteDaten:JSON.stringify({Kundenname:`Stefan König`,Firma:`IT-Service König`,Anliegen:`Wartungstermin Server`,Referenz:``,Vorschlaege:[`${f(b.termin1)} 10:00`,`${f(b.termin2)} 14:00`,`${f(b.termin3)}`]}),eskalationNoetig:!1,eskalationGrund:null,entwurf:w(4,4,S.termin,u(2)),anhangAnzahl:0},5:{id:5,absender:`winner@example.org`,betreff:`Sie haben gewonnen! 1.000.000 €`,inhaltRoh:x.spam,empfangenAm:d(1),gelesenAm:null,status:`ANALYSIERT`,postfachEmail:y.emailAdresse,provider:y.provider,kategorie:`SPAM`,dringlichkeit:`NIEDRIG`,extrahierteDaten:JSON.stringify({Klassifizierung:`Betrugsversuch / Vorschussbetrug`,Gefahrenstufe:`HOCH`}),eskalationNoetig:!1,eskalationGrund:null,entwurf:null,anhangAnzahl:0},6:{id:6,absender:`rechtsanwalt@example.org`,betreff:`Letzte Mahnung vor rechtlichen Schritten`,inhaltRoh:x.eskaliert,empfangenAm:u(12),gelesenAm:u(10),status:`ESKALIERT`,postfachEmail:y.emailAdresse,provider:y.provider,kategorie:`SONSTIGES`,dringlichkeit:`HOCH`,extrahierteDaten:JSON.stringify({Kundenname:`RA Dr. Meyer`,Firma:`Kanzlei Meyer`,Anliegen:`Zahlungsforderung / rechtliche Schritte`,Referenz:`Rechnung ${b.forderung}`,Betrag:`12750.00`,Forderung:`Lieferant KG`}),eskalationNoetig:!0,eskalationGrund:`Rechtliche Drohung / Anwaltskontakt - sofortige Prüfung durch Vorgesetzten erforderlich. Stichworte: gerichtliches Mahnverfahren, Strafanzeige, Schadensersatzforderungen.`,entwurf:null,anhangAnzahl:0},7:{id:7,absender:`info@example.com`,betreff:`Kooperationsanfrage für ${b.kooperation}`,inhaltRoh:x.sonstiges,empfangenAm:ee(30),gelesenAm:null,status:`NEU`,postfachEmail:y.emailAdresse,provider:y.provider,kategorie:null,dringlichkeit:null,extrahierteDaten:null,eskalationNoetig:!1,eskalationGrund:null,entwurf:null,anhangAnzahl:0},8:{id:8,absender:`anna.schmidt@example.com`,betreff:`Bestellung Bürogerät PrintMaster X200`,inhaltRoh:x.bestellung,empfangenAm:d(9),gelesenAm:d(9),status:`VERSENDET`,postfachEmail:y.emailAdresse,provider:y.provider,kategorie:`ANFRAGE`,dringlichkeit:`NIEDRIG`,extrahierteDaten:JSON.stringify({Kundenname:`Anna Schmidt`,Firma:``,Anliegen:`Bestellung Bürogerät PrintMaster X200`,Referenz:`BP-${i.getFullYear()}-1043`}),eskalationNoetig:!1,eskalationGrund:null,entwurf:w(8,8,`Guten Tag Frau Schmidt,

vielen Dank für Ihre Bestellung. Gerne bestätigen wir Ihnen ein Bürogerät Modell PrintMaster X200.

Der Versand erfolgt voraussichtlich innerhalb von fünf Werktagen. Sobald das Gerät unser Lager verlassen hat, erhalten Sie eine separate Versandbestätigung mit Sendungsnummer.

Mit freundlichen Grüßen,
Ihr MailPilot-Team`,d(9),{finalText:`Guten Tag Frau Schmidt,

vielen Dank für Ihre Bestellung. Gerne bestätigen wir Ihnen ein Bürogerät Modell PrintMaster X200.

Der Versand erfolgt voraussichtlich innerhalb von fünf Werktagen. Sobald das Gerät unser Lager verlassen hat, erhalten Sie eine separate Versandbestätigung mit Sendungsnummer.

Mit freundlichen Grüßen,
Ihr MailPilot-Team`,versendetAm:d(9),bearbeitetVonUserId:g}),anhangAnzahl:0},9:{id:9,absender:`anna.schmidt@example.com`,betreff:`Rückfrage zur Lieferung`,inhaltRoh:x.rueckfrage,empfangenAm:d(2),gelesenAm:d(2),status:`GEPRUEFT`,postfachEmail:y.emailAdresse,provider:y.provider,kategorie:`ANFRAGE`,dringlichkeit:`MITTEL`,extrahierteDaten:JSON.stringify({Kundenname:`Anna Schmidt`,Firma:``,Anliegen:`Status Lieferung PrintMaster X200`,Referenz:`Bestellung ${b.bestellung}`}),eskalationNoetig:!1,eskalationGrund:null,entwurf:w(9,9,`Guten Tag Frau Schmidt,

vielen Dank für Ihre Nachricht. Ihre Bestellung ist bei uns eingegangen und für den Versand vorgemerkt.

Sie erhalten die Versandbestätigung mit Sendungsnummer, sobald das Gerät unser Lager verlassen hat. Bei Rückfragen stehen wir Ihnen gerne zur Verfügung.

Mit freundlichen Grüßen,
Ihr MailPilot-Team`,d(2),{bearbeitetVonUserId:g}),anhangAnzahl:0}},ne=`thread-demo-reklamation-1`,re=Object.values(T).map(e=>({id:e.id,postfachId:y.id,absender:e.absender,betreff:e.betreff,empfangenAm:e.empfangenAm,gelesenAm:e.gelesenAm,status:e.status,kategorie:e.kategorie,dringlichkeit:e.dringlichkeit,eskalationNoetig:e.eskalationNoetig,eskalationGrund:e.eskalationGrund,hatEntwurf:e.entwurf!==null,entwurfId:e.entwurf?e.entwurf.id:null})).sort((e,t)=>t.empfangenAm.localeCompare(e.empfangenAm)),E={2:{threadId:ne,mails:[8,9,2].map(e=>{let t=T[e],n=t.inhaltRoh||``;return{id:t.id,absender:t.absender,betreff:t.betreff,empfangenAm:t.empfangenAm,inhaltVorschau:n.length>150?`${n.substring(0,150)}...`:n,status:t.status}})},8:null,9:null};E[8]=E[2],E[9]=E[2];var ie={2:[{id:1,dateiname:`foto-druckkopf-defekt.png`,contentType:`image/png`,groesseBytes:184320,erstelltAm:u(5)},{id:2,dateiname:`lieferschein-printmaster-x200.pdf`,contentType:`application/pdf`,groesseBytes:96512,erstelltAm:u(5)}],3:[{id:3,dateiname:`rechnung-${b.rechnung}.pdf`,contentType:`application/pdf`,groesseBytes:131072,erstelltAm:u(8)}]},ae=[{id:1,mandantId:_,titel:`Wie sind die Geschäftszeiten des Supports?`,inhalt:`Unser Support ist montags bis freitags von 08:00 bis 17:00 Uhr erreichbar. Anfragen, die außerhalb dieser Zeiten eingehen, beantworten wir am nächsten Werktag. An Feiertagen bleibt das Büro geschlossen.`,tags:`FAQ, Support, Erreichbarkeit`,erstelltAm:d(40),aktualisiertAm:d(12)},{id:2,mandantId:_,titel:`Wie lange dauert die Lieferung?`,inhalt:`Standardlieferungen innerhalb Deutschlands dauern in der Regel drei bis fünf Werktage ab Bestellbestätigung. Bei Artikeln auf Lager erfolgt der Versand innerhalb von 24 Stunden. Sobald die Ware unser Lager verlässt, erhalten Sie eine Versandbestätigung mit Sendungsnummer.`,tags:`FAQ, Lieferung, Versand`,erstelltAm:d(38),aktualisiertAm:d(9)},{id:3,mandantId:_,titel:`Wie läuft eine Reklamation ab?`,inhalt:`Melden Sie defekte oder falsch gelieferte Artikel bitte innerhalb von 14 Tagen nach Erhalt. Wir senden Ihnen ein Rücksendelabel zu und prüfen das Gerät anschließend in unserer Werkstatt. Ist der Mangel bestätigt, erhalten Sie kostenlos ein Austauschgerät oder eine Erstattung.`,tags:`FAQ, Reklamation, Rückgabe`,erstelltAm:d(35),aktualisiertAm:d(7)},{id:4,mandantId:_,titel:`Welche Zahlungsarten bieten wir an?`,inhalt:`Wir akzeptieren Überweisung, Kauf auf Rechnung (14 Tage netto), Kreditkarte und Lastschrift. Bei Neukunden behalten wir uns eine Vorkasse vor. Alle Preise verstehen sich zuzüglich der gesetzlichen Umsatzsteuer.`,tags:`FAQ, Zahlung, Rechnung`,erstelltAm:d(30),aktualisiertAm:d(15)},{id:5,mandantId:_,titel:`Wie hoch ist der Stundensatz für Beratung?`,inhalt:`Der reguläre Stundensatz für Beratungs- und Servicedienstleistungen beträgt 160,00 € netto. Für Wartungspakete mit jährlicher Laufzeit gewähren wir 10 % Nachlass. Abweichende Satzvereinbarungen gelten nur, wenn sie schriftlich in einem Angebot bestätigt wurden.`,tags:`FAQ, Preise, Beratung, Stundensatz`,erstelltAm:d(28),aktualisiertAm:d(5)},{id:6,mandantId:_,titel:`Antwort auf verdächtige Mails (Phishing/Spam)`,inhalt:`E-Mails, die persönliche Daten, Bankverbindungen oder Vorauszahlungen verlangen, beantworten wir nicht inhaltlich. Wir dokumentieren den Vorgang intern, markieren die Nachricht als Spam und informieren bei Verdacht auf Betrug die zuständige Stelle. Keine Anhänge solcher Mails öffnen.`,tags:`FAQ, Spam, Sicherheit`,erstelltAm:d(20),aktualisiertAm:d(3)}];function oe(e){let t=e;return function(){t|=0,t=t+1831565813|0;let e=Math.imul(t^t>>>15,1|t);return e=e+Math.imul(e^e>>>7,61|e)^e,((e^e>>>14)>>>0)/4294967296}}var D=(e,t)=>{let n=10**t;return Math.round(e*n)/n},se=oe(20260929),ce=Array.from({length:30},(e,t)=>{let n=c(29-t),r=n.getDay(),i=r===0,a=0,o=0;return i||(a=D((r===6?.11:.22)+se()*.24,4),o=Math.max(1,Math.round(a/.008))),{tag:s(n),mandantId:_,firmenname:h.firmenname,kosten:a,anzahlCalls:o}}),le=ce.filter(e=>e.tag.startsWith(`${i.getFullYear()}-${a(i.getMonth()+1)}`)),O=D(le.reduce((e,t)=>e+t.kosten,0),4),k=le.reduce((e,t)=>e+t.anzahlCalls,0),ue=[{mandantId:_,firmenname:h.firmenname,monatlichesLimitUsd:h.monatlichesLimitUsd,limitVerhalten:h.limitVerhalten,fallbackModellId:h.fallbackModellId,gesamtKostenMonat:O,anzahlApiCalls:k,totalInputTokens:k*1180,totalOutputTokens:k*430,limitAuslastungProzent:D(O/h.monatlichesLimitUsd*100,1),schwellenwertErreicht:O>=h.monatlichesLimitUsd*.8}],A=[{id:6,userId:g,zeitpunkt:u(1),aktion:`ENTWURF_ERSTELLT`,details:`KI-Antwortentwurf für Mail 1 (Angebot für IT-Beratung) erstellt`,userName:`${v.vorname} ${v.nachname}`,mailId:1,mailBetreff:T[1].betreff},{id:5,userId:g,zeitpunkt:u(4),aktion:`ENTWURF_GESPEICHERT`,details:`Entwurf 2 manuell bearbeitet und gespeichert`,userName:`${v.vorname} ${v.nachname}`,mailId:2,mailBetreff:T[2].betreff},{id:4,userId:g,zeitpunkt:d(2),aktion:`VERSANDT`,details:`Entwurf 9 versendet an anna.schmidt@example.com via GMAIL (demo@mailpilot.de) [DEMO-MODUS - simulierter Versand]`,userName:`${v.vorname} ${v.nachname}`,mailId:9,mailBetreff:T[9].betreff},{id:3,userId:g,zeitpunkt:d(9),aktion:`VERSANDT`,details:`Entwurf 8 versendet an anna.schmidt@example.com via GMAIL (demo@mailpilot.de) [DEMO-MODUS - simulierter Versand]`,userName:`${v.vorname} ${v.nachname}`,mailId:8,mailBetreff:T[8].betreff},{id:2,userId:g,zeitpunkt:d(12),aktion:`WISSENSBASIS_ANGELEGT`,details:`Wissensbasis-Eintrag "Wie läuft eine Reklamation ab?" angelegt`,userName:`${v.vorname} ${v.nachname}`,mailId:null,mailBetreff:null},{id:1,userId:g,zeitpunkt:d(45),aktion:`POSTFACH_VERBUNDEN`,details:`Postfach demo@mailpilot.de (GMAIL) erfolgreich verbunden`,userName:`${v.vorname} ${v.nachname}`,mailId:null,mailBetreff:null}],de={content:A,page:{size:50,number:0,totalElements:A.length,totalPages:1},totalElements:A.length,totalPages:1,size:50,number:0,numberOfElements:A.length,first:!0,last:!0,empty:A.length===0},fe=C,pe=C,j={mandant:h,benutzer:v,postfach:y,mails:re,mailDetails:T,threads:E,anhaenge:ie,wissensbasis:ae,kostenUebersicht:ue,kostenVerlauf:ce,auditLog:de,einstellungen:{mandantId:_,firmenname:h.firmenname,bevorzugtesModellId:h.bevorzugtesModellId,globalClassifyModel:fe,globalDraftModel:pe}},M=`mailpilot-demo-state`,N=1,P=null,F=e=>e===void 0?void 0:JSON.parse(JSON.stringify(e)),I=e=>String(e).padStart(2,`0`);function L(){let e=new Date;return`${e.getFullYear()}-${I(e.getMonth()+1)}-${I(e.getDate())}T${I(e.getHours())}:${I(e.getMinutes())}:${I(e.getSeconds())}`}function me(){let e=new Date;return`${e.getFullYear()}-${I(e.getMonth()+1)}-${I(e.getDate())}`}function R(e,t=e=>e.id){return e.reduce((e,n)=>Math.max(e,t(n)||0),0)}function z(){let e=Object.values(j.mailDetails).map(e=>e.entwurf).filter(Boolean),t=Object.values(j.anhaenge).flat().filter(Boolean);return{version:N,benutzer:F(j.benutzer),postfaecher:[F(j.postfach)],mailDetails:F(j.mailDetails),threads:F(j.threads),anhaenge:F(j.anhaenge),wissensbasis:F(j.wissensbasis),einstellungen:F(j.einstellungen),kostenUebersicht:F(j.kostenUebersicht),kostenVerlauf:F(j.kostenVerlauf),auditLog:F(j.auditLog.content),naechsteIds:{entwurf:R(e)+1,wissensbasis:R(j.wissensbasis)+1,auditLog:R(j.auditLog.content)+1,anhang:R(t)+1}}}function he(){try{let e=window.sessionStorage.getItem(M);if(!e)return null;let t=JSON.parse(e);return!t||t.version!==N||!t.mailDetails||!t.benutzer||!t.naechsteIds?null:t}catch{return null}}function B(){try{window.sessionStorage.setItem(M,JSON.stringify(P))}catch{}}function V(){return P||=he()||z(),P}function ge(){return P=z(),B(),P}function H(e){let t=e(V());return B(),t}function _e(){let e=V();return e.postfaecher[0]?e.postfaecher[0].id:j.postfach.id}function ve(e){return{id:e.id,postfachId:_e(),absender:e.absender,betreff:e.betreff,empfangenAm:e.empfangenAm,gelesenAm:e.gelesenAm,status:e.status,kategorie:e.kategorie,dringlichkeit:e.dringlichkeit,eskalationNoetig:e.eskalationNoetig,eskalationGrund:e.eskalationGrund,hatEntwurf:e.entwurf!==null&&e.entwurf!==void 0,entwurfId:e.entwurf?e.entwurf.id:null}}function ye(e){let t=V(),n=e?String(e).toUpperCase():null;return F(Object.values(t.mailDetails).map(ve).filter(e=>!n||e.status===n).sort((e,t)=>t.empfangenAm.localeCompare(e.empfangenAm)))}function U(e){let t=V().mailDetails[e];return t?F(t):null}function W(e){let t=e.inhaltRoh||``;return{id:e.id,absender:e.absender,betreff:e.betreff,empfangenAm:e.empfangenAm,inhaltVorschau:t.length>150?`${t.substring(0,150)}...`:t,status:e.status}}function be(e){let t=V(),n=t.mailDetails[e];if(!n)return null;let r=t.threads[e];if(!r)return{threadId:null,mails:[W(n)]};let i=r.mails.map(e=>t.mailDetails[e.id]).filter(Boolean).map(W);return{threadId:r.threadId,mails:i}}function G(e,t,n){let r=V(),i=n?r.mailDetails[n]:null,a={id:r.naechsteIds.auditLog,userId:1,zeitpunkt:L(),aktion:e,details:t,userName:`${r.benutzer.vorname} ${r.benutzer.nachname}`,mailId:i?i.id:null,mailBetreff:i?i.betreff:null};return r.naechsteIds.auditLog+=1,r.auditLog.push(a),a}function xe({benutzerId:e,page:t=0,size:n=50}={}){let r=V().auditLog.filter(t=>!e||t.userId===Number(e)).slice().sort((e,t)=>t.zeitpunkt.localeCompare(e.zeitpunkt)),i=Number(n)>0?Number(n):50,a=Number(t)>0?Number(t):0,o=Math.max(1,Math.ceil(r.length/i)),s=r.slice(a*i,a*i+i);return{content:F(s),page:{size:i,number:a,totalElements:r.length,totalPages:o},totalElements:r.length,totalPages:o,size:i,number:a,numberOfElements:s.length,first:a===0,last:a>=o-1,empty:s.length===0}}function Se(e){let t=V().auditLog.filter(t=>!e||t.userId===Number(e)).slice().sort((e,t)=>t.zeitpunkt.localeCompare(e.zeitpunkt)),n=e=>`"${String(e??``).replace(/"/g,`""`)}"`,r=(...e)=>e.map(n).join(`;`);return[`\uFEFF${r(`Zeitpunkt`,`Benutzer`,`Aktion`,`Details`,`Mail-Betreff`)}`,...t.map(e=>r(e.zeitpunkt.replace(`T`,` `),e.userName,e.aktion,e.details,e.mailBetreff))].join(`\r
`)+`\r
`}function Ce(e,t,n){return H(r=>{let i=r.mailDetails[e];if(!i)return null;let a={id:r.naechsteIds.entwurf,mailId:i.id,entwurfText:t,llmModellVerwendet:n,erstelltAm:L(),bearbeitetVonUserId:null,finalText:null,versendetAm:null,autoGeneriert:!0};return r.naechsteIds.entwurf+=1,i.entwurf=a,i.status=`ENTWURF_ERSTELLT`,G(`ENTWURF_ERSTELLT`,`KI-Antwortentwurf für Mail ${i.id} (${i.betreff}) erstellt`,i.id),F(a)})}function we(e,t){return H(n=>{let r=n.mailDetails[e];return!r||!r.entwurf?null:(r.entwurf.entwurfText=t,r.entwurf.bearbeitetVonUserId=1,G(`ENTWURF_GESPEICHERT`,`Entwurf ${r.entwurf.id} manuell bearbeitet und gespeichert`,r.id),F(r.entwurf))})}function Te(e,t,n){return H(r=>{let i=r.mailDetails[e];if(!i||!i.entwurf)return null;let a=n&&n.trim()?n:i.entwurf.entwurfText,o=r.postfaecher[0]||j.postfach,s=L();return i.entwurf.finalText=a,i.entwurf.versendetAm=s,i.entwurf.bearbeitetVonUserId=Number(t)||1,i.status=`VERSENDET`,i.gelesenAm=s,G(`VERSANDT`,`Entwurf ${i.entwurf.id} versendet an ${i.absender} via ${o.provider} (${o.emailAdresse}) [DEMO-MODUS - simulierter Versand]`,i.id),F(i.entwurf)})}function Ee(){return F(V().postfaecher)}function De(e){return H(t=>{let n=t.postfaecher.find(t=>t.id===Number(e));return n?(n.aktiv=!1,F(n)):null})}function K(){return F(V().wissensbasis)}function Oe(e){let t=String(e||``).trim().toLowerCase();return t?K().filter(e=>[e.titel,e.inhalt,e.tags].filter(Boolean).some(e=>String(e).toLowerCase().includes(t))):K()}function ke({titel:e,inhalt:t,tags:n}){return H(r=>{let i=L(),a={id:r.naechsteIds.wissensbasis,mandantId:r.benutzer.mandantId,titel:e,inhalt:t,tags:n||null,erstelltAm:i,aktualisiertAm:i};return r.naechsteIds.wissensbasis+=1,r.wissensbasis.push(a),G(`WISSENSBASIS_ANGELEGT`,`Wissensbasis-Eintrag "${e}" angelegt`,null),F(a)})}function Ae(e,{titel:t,inhalt:n,tags:r}){return H(i=>{let a=i.wissensbasis.find(t=>t.id===Number(e));return a?(a.titel=t,a.inhalt=n,a.tags=r||null,a.aktualisiertAm=L(),F(a)):null})}function je(e){return H(t=>{let n=t.wissensbasis.findIndex(t=>t.id===Number(e));if(n===-1)return!1;let[r]=t.wissensbasis.splice(n,1);return G(`WISSENSBASIS_GELOESCHT`,`Wissensbasis-Eintrag "${r.titel}" gelöscht`,null),!0})}function Me(){let e=V();return{mandantId:e.benutzer.mandantId,firmenname:e.benutzer.firmenname,bevorzugtesModellId:e.einstellungen.bevorzugtesModellId,globalClassifyModel:e.einstellungen.globalClassifyModel,globalDraftModel:e.einstellungen.globalDraftModel}}function Ne({bevorzugtesModellId:e}){return H(t=>{let n=typeof e==`string`&&e.trim()?e.trim():null;return t.einstellungen.bevorzugtesModellId=n,Me()})}function Pe(){return F(V().kostenUebersicht)}function Fe(){return F(V().kostenVerlauf)}function Ie(){let e=V(),t={sub:`1`,email:e.benutzer.email,mandantId:e.benutzer.mandantId,rolle:e.benutzer.rolle,demoModus:e.benutzer.demoModus===!0,emailVerifiziert:e.benutzer.emailVerifiziert===!0,aboStatus:e.benutzer.aboStatus,trialEndeAm:e.benutzer.trialEndeAm,firmenname:e.benutzer.firmenname,vorname:e.benutzer.vorname,nachname:e.benutzer.nachname};return`demo-header.${btoa(JSON.stringify(t)).replace(/=+$/,``)}.demo-signatur`}function Le(){let e=V();return{token:Ie(),email:e.benutzer.email,vorname:e.benutzer.vorname,nachname:e.benutzer.nachname,rolle:e.benutzer.rolle,mandantId:e.benutzer.mandantId,firmenname:e.benutzer.firmenname,demoModus:e.benutzer.demoModus===!0,emailVerifiziert:e.benutzer.emailVerifiziert===!0,aboStatus:e.benutzer.aboStatus,trialEndeAm:e.benutzer.trialEndeAm,plan:e.benutzer.plan}}var Re=700,ze=`In der Demo nicht verfügbar.`,Be=e=>new Promise(t=>setTimeout(t,e)),q=e=>Number.parseInt(e,10),J=()=>({status:403,data:{error:ze}}),Y=()=>({status:404,data:null}),X=(e,t)=>({status:e,data:{error:t}});async function Ve(e){let t=e.data;if(t==null)return null;if(typeof t==`string`)try{return JSON.parse(t)}catch{return null}if(typeof FormData<`u`&&t instanceof FormData){let e=t.get(`request`);if(e&&typeof e.text==`function`)try{return JSON.parse(await e.text())}catch{return null}return null}return typeof t==`object`?t:null}function He(e){return e.params||{}}var Ue=()=>({status:200,data:Le()}),We=({query:e})=>({status:200,data:ye(e.status)}),Ge=({params:e})=>{let t=U(q(e.mailId));return t?{status:200,data:t}:Y()},Ke=({params:e})=>{let t=be(q(e.mailId));return t?{status:200,data:t}:Y()},qe=({params:e})=>({status:200,data:V().anhaenge?.[q(e.mailId)]||[]}),Je=async({params:e})=>{let n=q(e.mailId),i=U(n);if(!i)return Y();if(i.status===`ESKALIERT`)return X(400,`Eskalierte E-Mails erhalten keinen automatischen Entwurf.`);await Be(Re+Math.random()*800);let a=Ce(n,r(i.kategorie),t);return a?{status:201,data:a}:Y()},Ye=({params:e})=>{let t=U(q(e.mailId));return t?t.entwurf?{status:200,data:t.entwurf}:{status:404,data:{error:`Kein Entwurf vorhanden.`}}:Y()},Xe=({params:e,body:t})=>{let n=q(e.mailId),r=U(n);if(!r||!r.entwurf)return Y();let i=we(n,t&&typeof t.entwurfText==`string`?t.entwurfText:``);return i?{status:200,data:i}:Y()},Ze=({params:e,body:t})=>{let n=q(e.mailId),r=U(n);if(!r)return Y();if(!t||t.userId===void 0||t.userId===null)return X(400,`userId ist erforderlich`);if(r.status===`VERSENDET`)return X(400,`E-Mail ${n} wurde bereits versendet.`);if(r.status===`ESKALIERT`)return X(400,`Eskalierte E-Mails können nicht versendet werden. Bitte manuell bearbeiten.`);if(!r.entwurf)return X(400,`Kein Entwurf für E-Mail ${n} vorhanden. Bitte zuerst einen Entwurf erstellen.`);let i=Te(n,t.userId,t.finalText);return i?{status:200,data:i}:Y()},Qe=()=>({status:200,data:Pe()}),$e=()=>({status:200,data:Fe()}),et=()=>({status:200,data:{status:`OK`,mandanten:`1`}}),tt=({query:e})=>({status:200,data:xe({benutzerId:e.benutzerId,page:e.page===void 0?0:q(e.page),size:e.size===void 0?50:q(e.size)})}),nt=({params:e,query:t})=>({status:200,data:Se(t.benutzerId),headers:{"content-type":`text/csv; charset=UTF-8`,"content-disposition":`attachment; filename="auditlog-mandant-${e.mandantId}-${me()}.csv"`}}),rt=()=>({status:200,data:Ee()}),it=({params:e})=>De(q(e.id))?{status:204,data:null}:Y(),at=()=>({status:200,data:Me()}),ot=({body:e})=>({status:200,data:{gespeichert:!0,...Ne({bevorzugtesModellId:e?e.bevorzugtesModellId:null})}}),st=()=>({status:200,data:K()}),ct=({query:e})=>({status:200,data:Oe(e.q)}),lt=({body:e})=>{let t=e||{};return!t.titel||!t.inhalt?X(400,`Titel und Inhalt sind erforderlich.`):{status:201,data:ke({titel:t.titel,inhalt:t.inhalt,tags:t.tags})}},ut=({params:e,body:t})=>{let n=t||{};if(!n.titel||!n.inhalt)return X(400,`Titel und Inhalt sind erforderlich.`);let r=Ae(q(e.id),{titel:n.titel,inhalt:n.inhalt,tags:n.tags});return r?{status:200,data:r}:Y()},dt=({params:e})=>je(q(e.id))?{status:204,data:null}:Y(),Z=`(?<mandantId>\\d+)`,Q=`(?<mailId>\\d+)`,$=`(?<id>\\d+)`,ft=[{methode:`post`,muster:`/auth/login`,handler:Ue},{methode:`post`,muster:`/auth/register`,handler:J},{methode:`post`,muster:`/auth/register-firma`,handler:J},{methode:`post`,muster:`/auth/passwort-vergessen`,handler:J},{methode:`post`,muster:`/auth/passwort-zuruecksetzen`,handler:J},{methode:`get`,muster:`/auth/verifizieren`,handler:J},{methode:`post`,muster:`/auth/verifizierung-senden`,handler:J},{methode:`get`,muster:`/mandanten/${Z}/mails`,handler:We},{methode:`get`,muster:`/mandanten/${Z}/mails/${Q}`,handler:Ge},{methode:`post`,muster:`/mandanten/${Z}/mails/${Q}/entwurf`,handler:Je},{methode:`get`,muster:`/mandanten/${Z}/mails/${Q}/entwurf`,handler:Ye},{methode:`put`,muster:`/mandanten/${Z}/mails/${Q}/entwurf`,handler:Xe},{methode:`post`,muster:`/mandanten/${Z}/mails/${Q}/versenden`,handler:Ze},{methode:`post`,muster:`/mandanten/${Z}/mails/${Q}/versenden-mit-anhang`,handler:Ze},{methode:`get`,muster:`/mandanten/${Z}/mails/${Q}/anhaenge`,handler:qe},{methode:`get`,muster:`/mandanten/${Z}/mails/${Q}/thread`,handler:Ke},{methode:`get`,muster:`/mandanten/${Z}/wissensbasis/suche`,handler:ct},{methode:`get`,muster:`/mandanten/${Z}/wissensbasis`,handler:st},{methode:`post`,muster:`/mandanten/${Z}/wissensbasis`,handler:lt},{methode:`put`,muster:`/mandanten/${Z}/wissensbasis/${$}`,handler:ut},{methode:`delete`,muster:`/mandanten/${Z}/wissensbasis/${$}`,handler:dt},{methode:`get`,muster:`/mandanten/${Z}/auditlog/export`,handler:nt},{methode:`get`,muster:`/mandanten/${Z}/auditlog`,handler:tt},{methode:`get`,muster:`/mandanten/${Z}/postfaecher/verbinden/google`,handler:J},{methode:`get`,muster:`/mandanten/${Z}/postfaecher/verbinden/outlook`,handler:J},{methode:`post`,muster:`/mandanten/${Z}/postfaecher/generisch`,handler:J},{methode:`get`,muster:`/mandanten/${Z}/postfaecher`,handler:rt},{methode:`delete`,muster:`/mandanten/${Z}/postfaecher/${$}`,handler:it},{methode:`get`,muster:`/autodiscover`,handler:J},{methode:`get`,muster:`/admin/kosten/verlauf`,handler:$e},{methode:`get`,muster:`/admin/kosten`,handler:Qe},{methode:`get`,muster:`/admin/health`,handler:et},{methode:`get`,muster:`/admin/mandanten/${Z}/einstellungen`,handler:at},{methode:`put`,muster:`/admin/mandanten/${Z}/einstellungen`,handler:ot},{methode:`post`,muster:`/billing/checkout-session`,handler:J}].map(e=>({...e,regex:RegExp(`^${e.muster}/?$`)}));function pt(e,t){return ft.find(n=>n.methode===e&&n.regex.test(t))||null}var mt={200:`OK`,201:`Created`,204:`No Content`,400:`Bad Request`,403:`Forbidden`,404:`Not Found`};function ht(t,n){let r=n.data&&n.data.error||`Request failed with status code ${n.status}`;if(typeof e.AxiosError==`function`)return new e.AxiosError(r,String(n.status),t,{},n);let i=Error(r);return i.isAxiosError=!0,i.config=t,i.response=n,i}function gt(){return async function(e){let t=(e.method||`get`).toLowerCase(),n=String(e.url||``).split(`?`)[0],r=pt(t,n),i=r?r.regex.exec(n):null,a;if(!r||!i)a={status:404,data:{error:`Demo-Adapter: kein Handler für ${t.toUpperCase()} ${n}`}};else{let t=await Ve(e);try{a=await r.handler({config:e,params:i.groups||{},body:t,query:He(e)})}catch(e){a={status:500,data:{error:e.message||`Demo-Adapter-Fehler`}}}}let o=a.status||200,s={data:o===204?null:a.data,status:o,statusText:mt[o]||``,headers:a.headers||{},config:e,request:{}};if(e.validateStatus?e.validateStatus(o):o>=200&&o<300)return s;throw ht(e,s)}}export{gt as createDemoAdapter,gt as default,ge as resetDemo};