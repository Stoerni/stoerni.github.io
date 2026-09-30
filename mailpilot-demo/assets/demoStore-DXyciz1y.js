var e=new Date,t=e=>String(e).padStart(2,`0`);function n(e){return`${e.getFullYear()}-${t(e.getMonth()+1)}-${t(e.getDate())}T${t(e.getHours())}:${t(e.getMinutes())}:${t(e.getSeconds())}`}function r(e){return`${e.getFullYear()}-${t(e.getMonth()+1)}-${t(e.getDate())}`}function i(t){let n=new Date(e);return n.setDate(n.getDate()-t),n}function a(t){let n=new Date(e);return n.setDate(n.getDate()+t),n}function o(t){return n(new Date(e.getTime()-t*3600*1e3))}function s(e){return n(i(e))}function c(t){return n(new Date(e.getTime()+t*60*1e3))}function l(e){return`${t(e.getDate())}.${t(e.getMonth()+1)}.${e.getFullYear()}`}function u(e){return e.toLocaleDateString(`de-DE`,{weekday:`long`})}function d(e){return`RE-${e.getFullYear()}-${t(e.getMonth()+1)}${t(e.getDate())}`}var f={id:1,firmenname:`Demo GmbH`,monatlichesLimitUsd:25,limitVerhalten:`HARD_STOP`,fallbackModellId:null,bevorzugtesModellId:null,demoModus:!0,tonalitaet:`FREUNDLICH`,aboStatus:`AKTIV`,trialEndeAm:null,plan:`STANDARD`},p=1,m=f.id,h={token:``,email:`admin@example.com`,vorname:`Anna`,nachname:`Adler`,rolle:`ADMIN`,mandantId:m,firmenname:f.firmenname,demoModus:!0,emailVerifiziert:!0,aboStatus:f.aboStatus,trialEndeAm:f.trialEndeAm,plan:f.plan};function ee(){let e={sub:String(p),email:h.email,mandantId:m,rolle:h.rolle,demoModus:h.demoModus,emailVerifiziert:h.emailVerifiziert,aboStatus:h.aboStatus,trialEndeAm:h.trialEndeAm};return`demo-header.${btoa(JSON.stringify(e)).replace(/=+$/,``)}.demo-signatur`}h.token=ee();var g={id:1,emailAdresse:`demo@mailpilot.de`,provider:`GMAIL`,aktiv:!0,letzterAbruf:o(1)},_={bestellung:l(i(9)),bestellungErsatz:l(i(7)),lieferung:l(i(2)),rechnung:d(i(11)),vertrag:l(i(60)),forderung:d(i(24)),forderungFrist:l(a(7)),termin1:a(6),termin2:a(7),termin3:a(8),kooperation:`Q${Math.ceil((e.getMonth()+1)/3)} ${e.getFullYear()}`},v={anfrage:`Sehr geehrte Damen und Herren,

ich bin auf der Suche nach einem IT-Beratungsunternehmen, das uns bei der Einführung eines neuen CRM-Systems unterstützen kann. Wir sind ein mittelständisches Unternehmen mit ca. 50 Mitarbeitern. Könnten Sie mir ein unverbindliches Angebot für eine Erstberatung sowie eine grobe Kostenabschätzung zusenden?

Mit freundlichen Grüßen,
Max Mustermann
Geschäftsführer
max.mustermann@example.com`,reklamation:`Sehr geehrte Damen und Herren,

am ${_.bestellung} habe ich bei Ihnen ein Bürogerät (Modell: PrintMaster X200) bestellt. Die Lieferung erfolgte am ${_.lieferung}, jedoch ist das Gerät leider defekt. Der Druckkopf blockiert und es erscheint eine Fehlermeldung, die einen internen Hardware-Fehler anzeigt.

Da ich das Gerät dringend für meinen Geschäftsbetrieb benötige, bitte ich um umgehenden Austausch oder Reparatur. Ich erwarte eine Rückmeldung innerhalb von 24 Stunden.

Mit freundlichen Grüßen,
Anna Schmidt
anna.schmidt@example.com`,bestellung:`Guten Tag,

hiermit bestelle ich verbindlich ein Bürogerät Modell PrintMaster X200 (Bestellnummer: BP-${e.getFullYear()}-1043) zum Angebotspreis. Bitte bestätigen Sie mir den Liefertermin per E-Mail.

Mit freundlichen Grüßen,
Anna Schmidt
anna.schmidt@example.com`,rueckfrage:`Guten Tag,

ich hatte am ${_.bestellung} ein Bürogerät bestellt und noch keine Versandbestätigung erhalten. Können Sie mir den aktuellen Status nennen?

Mit freundlichen Grüßen,
Anna Schmidt
anna.schmidt@example.com`,rechnungEingang:`Guten Tag,

ich habe soeben Ihre Rechnung Nr. ${_.rechnung} über 2.450,00 € erhalten. Leider kann ich die Rechnung nicht ganz nachvollziehen:

- Position 1: IT-Beratung (10h) = 1.800,00 €
- Position 2: Lizenzgebühren (3 Monate) = 650,00 €

Laut unserer Vereinbarung vom ${_.vertrag} sollte der Stundensatz bei 160,00 € liegen, nicht bei 180,00 €. Könnten Sie dies bitte prüfen und korrigieren?

Mit freundlichen Grüßen,
Sabine Wagner
Buchhaltung`,termin:`Sehr geehrte Damen und Herren,

hiermit möchte ich einen Wartungstermin für unsere Serverinfrastruktur vereinbaren. Die letzte Wartung liegt bereits 6 Monate zurück.

Folgende Zeiträume wären bei uns möglich:
- ${u(_.termin1)}, ${l(_.termin1)} ab 10:00 Uhr
- ${u(_.termin2)}, ${l(_.termin2)} ab 14:00 Uhr
- ${u(_.termin3)}, ${l(_.termin3)} ganztägig

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

hiermit fordere ich Sie als bevollmächtigter Rechtsanwalt der Firma Lieferant KG letztmalig auf, die offene Forderung in Höhe von 12.750,00 € aus Rechnung Nr. ${_.forderung} binnen 7 Tagen zu begleichen.

Sollte der Zahlungseingang bis zum ${_.forderungFrist} nicht erfolgen, werde ich ohne weitere Ankündigung gerichtliche Mahnverfahren einleiten und Strafanzeige wegen Untreue stellen.

Des Weiteren behalten wir uns vor, Schadensersatzforderungen sowie Verzugszinsen in Höhe von 9 Prozentpunkten über dem Basiszinssatz geltend zu machen.

Hochachtungsvoll,
RA Dr. Meyer
Fachanwalt für Wirtschaftsrecht
rechtsanwalt@example.org
Tel: +49 30 0000000`,sonstiges:`Guten Tag,

ich bin auf Ihr Unternehmen durch eine Empfehlung von Herrn Klaus Weber aufmerksam geworden. Wir sind eine auf digitale Transformation spezialisierte Unternehmensberatung und suchen für das ${_.kooperation} einen Kooperationspartner im Bereich E-Mail-Automation und KI-gestützter Kundenkommunikation.

Hätten Sie Interesse an einem unverbindlichen Austausch? Ich würde mich freuen, von Ihnen zu hören.

Mit freundlichen Grüßen,
Dr. Julia Richter
Partner Consulting GmbH
info@example.com`},y={anfrage:`Sehr geehrter Herr Mustermann,

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

vielen Dank für Ihre Rückmeldung zur Rechnung Nr. ${_.rechnung}.

Sie haben vollkommen recht – der vereinbarte Stundensatz beträgt 160,00 €. Es handelt sich hier um einen internen Übertragungsfehler. Ich habe die Korrektur bereits veranlasst und sende Ihnen die berichtigte Rechnung per E-Mail zu.

Der korrekte Betrag lautet:
- Position 1: IT-Beratung (10h × 160,00 €) = 1.600,00 €
- Position 2: Lizenzgebühren (3 Monate) = 650,00 €
- Gesamt: 2.250,00 €

Wir bitten den Fehler zu entschuldigen.

Mit freundlichen Grüßen,
Ihr MailPilot-Team`,termin:`Sehr geehrter Herr König,

vielen Dank für Ihre Terminanfrage bezüglich der Serverwartung.

Gerne bestätige ich Ihnen den Termin am ${u(_.termin3)}, den ${l(_.termin3)}, ab 09:00 Uhr. Unser Techniker wird voraussichtlich ca. 4 Stunden vor Ort sein.

Sollte sich bei Ihnen etwas ändern, bitten wir um rechtzeitige Benachrichtigung.

Mit freundlichen Grüßen,
Ihr MailPilot-Team`},b=`deepseek/deepseek-v4.1-flash`;function x(e,t,n,r,i={}){return{id:e,mailId:t,entwurfText:n,llmModellVerwendet:b,erstelltAm:r,bearbeitetVonUserId:null,finalText:null,versendetAm:null,autoGeneriert:!0,...i}}var S={1:{id:1,absender:`max.mustermann@example.com`,betreff:`Angebot für IT-Beratung`,inhaltRoh:v.anfrage,empfangenAm:o(2),gelesenAm:o(1),status:`ENTWURF_ERSTELLT`,postfachEmail:g.emailAdresse,provider:g.provider,kategorie:`ANFRAGE`,dringlichkeit:`NIEDRIG`,extrahierteDaten:JSON.stringify({Kundenname:`Max Mustermann`,Firma:`Mustermann GmbH`,Anliegen:`Angebot CRM-Beratung`,Referenz:``}),eskalationNoetig:!1,eskalationGrund:null,entwurf:x(1,1,y.anfrage,o(1)),anhangAnzahl:0},2:{id:2,absender:`anna.schmidt@example.com`,betreff:`Defektes Gerät - sofortige Lösung erforderlich`,inhaltRoh:v.reklamation,empfangenAm:o(5),gelesenAm:o(4),status:`ENTWURF_ERSTELLT`,postfachEmail:g.emailAdresse,provider:g.provider,kategorie:`REKLAMATION`,dringlichkeit:`HOCH`,extrahierteDaten:JSON.stringify({Kundenname:`Anna Schmidt`,Firma:``,Anliegen:`Defektes Gerät PrintMaster X200`,Referenz:`Bestellung ${_.bestellung}`}),eskalationNoetig:!1,eskalationGrund:null,entwurf:x(2,2,y.reklamation,o(4)),anhangAnzahl:2},3:{id:3,absender:`buchhaltung@example.org`,betreff:`Frage zu Rechnung Nr. ${_.rechnung}`,inhaltRoh:v.rechnungEingang,empfangenAm:o(8),gelesenAm:o(6),status:`ENTWURF_ERSTELLT`,postfachEmail:g.emailAdresse,provider:g.provider,kategorie:`RECHNUNG`,dringlichkeit:`MITTEL`,extrahierteDaten:JSON.stringify({Kundenname:`Sabine Wagner`,Firma:`Musterfirma GmbH`,Anliegen:`Rechnungskorrektur ${_.rechnung}`,Referenz:`Rechnung ${_.rechnung}`}),eskalationNoetig:!1,eskalationGrund:null,entwurf:x(3,3,y.rechnung,o(6)),anhangAnzahl:1},4:{id:4,absender:`s.koenig@example.com`,betreff:`Terminvereinbarung für Wartung`,inhaltRoh:v.termin,empfangenAm:o(3),gelesenAm:o(2),status:`ENTWURF_ERSTELLT`,postfachEmail:g.emailAdresse,provider:g.provider,kategorie:`TERMIN`,dringlichkeit:`MITTEL`,extrahierteDaten:JSON.stringify({Kundenname:`Stefan König`,Firma:`IT-Service König`,Anliegen:`Wartungstermin Server`,Referenz:``,Vorschlaege:[`${l(_.termin1)} 10:00`,`${l(_.termin2)} 14:00`,`${l(_.termin3)}`]}),eskalationNoetig:!1,eskalationGrund:null,entwurf:x(4,4,y.termin,o(2)),anhangAnzahl:0},5:{id:5,absender:`winner@example.org`,betreff:`Sie haben gewonnen! 1.000.000 €`,inhaltRoh:v.spam,empfangenAm:s(1),gelesenAm:null,status:`ANALYSIERT`,postfachEmail:g.emailAdresse,provider:g.provider,kategorie:`SPAM`,dringlichkeit:`NIEDRIG`,extrahierteDaten:JSON.stringify({Klassifizierung:`Betrugsversuch / Vorschussbetrug`,Gefahrenstufe:`HOCH`}),eskalationNoetig:!1,eskalationGrund:null,entwurf:null,anhangAnzahl:0},6:{id:6,absender:`rechtsanwalt@example.org`,betreff:`Letzte Mahnung vor rechtlichen Schritten`,inhaltRoh:v.eskaliert,empfangenAm:o(12),gelesenAm:o(10),status:`ESKALIERT`,postfachEmail:g.emailAdresse,provider:g.provider,kategorie:`SONSTIGES`,dringlichkeit:`HOCH`,extrahierteDaten:JSON.stringify({Kundenname:`RA Dr. Meyer`,Firma:`Kanzlei Meyer`,Anliegen:`Zahlungsforderung / rechtliche Schritte`,Referenz:`Rechnung ${_.forderung}`,Betrag:`12750.00`,Forderung:`Lieferant KG`}),eskalationNoetig:!0,eskalationGrund:`Rechtliche Drohung / Anwaltskontakt - sofortige Prüfung durch Vorgesetzten erforderlich. Stichworte: gerichtliches Mahnverfahren, Strafanzeige, Schadensersatzforderungen.`,entwurf:null,anhangAnzahl:0},7:{id:7,absender:`info@example.com`,betreff:`Kooperationsanfrage für ${_.kooperation}`,inhaltRoh:v.sonstiges,empfangenAm:c(30),gelesenAm:null,status:`NEU`,postfachEmail:g.emailAdresse,provider:g.provider,kategorie:null,dringlichkeit:null,extrahierteDaten:null,eskalationNoetig:!1,eskalationGrund:null,entwurf:null,anhangAnzahl:0},8:{id:8,absender:`anna.schmidt@example.com`,betreff:`Bestellung Bürogerät PrintMaster X200`,inhaltRoh:v.bestellung,empfangenAm:s(9),gelesenAm:s(9),status:`VERSENDET`,postfachEmail:g.emailAdresse,provider:g.provider,kategorie:`ANFRAGE`,dringlichkeit:`NIEDRIG`,extrahierteDaten:JSON.stringify({Kundenname:`Anna Schmidt`,Firma:``,Anliegen:`Bestellung Bürogerät PrintMaster X200`,Referenz:`BP-${e.getFullYear()}-1043`}),eskalationNoetig:!1,eskalationGrund:null,entwurf:x(8,8,`Guten Tag Frau Schmidt,

vielen Dank für Ihre Bestellung. Gerne bestätigen wir Ihnen ein Bürogerät Modell PrintMaster X200.

Der Versand erfolgt voraussichtlich innerhalb von fünf Werktagen. Sobald das Gerät unser Lager verlassen hat, erhalten Sie eine separate Versandbestätigung mit Sendungsnummer.

Mit freundlichen Grüßen,
Ihr MailPilot-Team`,s(9),{finalText:`Guten Tag Frau Schmidt,

vielen Dank für Ihre Bestellung. Gerne bestätigen wir Ihnen ein Bürogerät Modell PrintMaster X200.

Der Versand erfolgt voraussichtlich innerhalb von fünf Werktagen. Sobald das Gerät unser Lager verlassen hat, erhalten Sie eine separate Versandbestätigung mit Sendungsnummer.

Mit freundlichen Grüßen,
Ihr MailPilot-Team`,versendetAm:s(9),bearbeitetVonUserId:p}),anhangAnzahl:0},9:{id:9,absender:`anna.schmidt@example.com`,betreff:`Rückfrage zur Lieferung`,inhaltRoh:v.rueckfrage,empfangenAm:s(2),gelesenAm:s(2),status:`GEPRUEFT`,postfachEmail:g.emailAdresse,provider:g.provider,kategorie:`ANFRAGE`,dringlichkeit:`MITTEL`,extrahierteDaten:JSON.stringify({Kundenname:`Anna Schmidt`,Firma:``,Anliegen:`Status Lieferung PrintMaster X200`,Referenz:`Bestellung ${_.bestellung}`}),eskalationNoetig:!1,eskalationGrund:null,entwurf:x(9,9,`Guten Tag Frau Schmidt,

vielen Dank für Ihre Nachricht. Ihre Bestellung ist bei uns eingegangen und für den Versand vorgemerkt.

Sie erhalten die Versandbestätigung mit Sendungsnummer, sobald das Gerät unser Lager verlassen hat. Bei Rückfragen stehen wir Ihnen gerne zur Verfügung.

Mit freundlichen Grüßen,
Ihr MailPilot-Team`,s(2),{bearbeitetVonUserId:p}),anhangAnzahl:0}},te=`thread-demo-reklamation-1`,ne=Object.values(S).map(e=>({id:e.id,postfachId:g.id,absender:e.absender,betreff:e.betreff,empfangenAm:e.empfangenAm,gelesenAm:e.gelesenAm,status:e.status,kategorie:e.kategorie,dringlichkeit:e.dringlichkeit,eskalationNoetig:e.eskalationNoetig,eskalationGrund:e.eskalationGrund,hatEntwurf:e.entwurf!==null,entwurfId:e.entwurf?e.entwurf.id:null})).sort((e,t)=>t.empfangenAm.localeCompare(e.empfangenAm)),C={2:{threadId:te,mails:[8,9,2].map(e=>{let t=S[e],n=t.inhaltRoh||``;return{id:t.id,absender:t.absender,betreff:t.betreff,empfangenAm:t.empfangenAm,inhaltVorschau:n.length>150?`${n.substring(0,150)}...`:n,status:t.status}})},8:null,9:null};C[8]=C[2],C[9]=C[2];var re={2:[{id:1,dateiname:`foto-druckkopf-defekt.png`,contentType:`image/png`,groesseBytes:184320,erstelltAm:o(5)},{id:2,dateiname:`lieferschein-printmaster-x200.pdf`,contentType:`application/pdf`,groesseBytes:96512,erstelltAm:o(5)}],3:[{id:3,dateiname:`rechnung-${_.rechnung}.pdf`,contentType:`application/pdf`,groesseBytes:131072,erstelltAm:o(8)}]},w=[{id:1,mandantId:m,titel:`Wie sind die Geschäftszeiten des Supports?`,inhalt:`Unser Support ist montags bis freitags von 08:00 bis 17:00 Uhr erreichbar. Anfragen, die außerhalb dieser Zeiten eingehen, beantworten wir am nächsten Werktag. An Feiertagen bleibt das Büro geschlossen.`,tags:`FAQ, Support, Erreichbarkeit`,erstelltAm:s(40),aktualisiertAm:s(12)},{id:2,mandantId:m,titel:`Wie lange dauert die Lieferung?`,inhalt:`Standardlieferungen innerhalb Deutschlands dauern in der Regel drei bis fünf Werktage ab Bestellbestätigung. Bei Artikeln auf Lager erfolgt der Versand innerhalb von 24 Stunden. Sobald die Ware unser Lager verlässt, erhalten Sie eine Versandbestätigung mit Sendungsnummer.`,tags:`FAQ, Lieferung, Versand`,erstelltAm:s(38),aktualisiertAm:s(9)},{id:3,mandantId:m,titel:`Wie läuft eine Reklamation ab?`,inhalt:`Melden Sie defekte oder falsch gelieferte Artikel bitte innerhalb von 14 Tagen nach Erhalt. Wir senden Ihnen ein Rücksendelabel zu und prüfen das Gerät anschließend in unserer Werkstatt. Ist der Mangel bestätigt, erhalten Sie kostenlos ein Austauschgerät oder eine Erstattung.`,tags:`FAQ, Reklamation, Rückgabe`,erstelltAm:s(35),aktualisiertAm:s(7)},{id:4,mandantId:m,titel:`Welche Zahlungsarten bieten wir an?`,inhalt:`Wir akzeptieren Überweisung, Kauf auf Rechnung (14 Tage netto), Kreditkarte und Lastschrift. Bei Neukunden behalten wir uns eine Vorkasse vor. Alle Preise verstehen sich zuzüglich der gesetzlichen Umsatzsteuer.`,tags:`FAQ, Zahlung, Rechnung`,erstelltAm:s(30),aktualisiertAm:s(15)},{id:5,mandantId:m,titel:`Wie hoch ist der Stundensatz für Beratung?`,inhalt:`Der reguläre Stundensatz für Beratungs- und Servicedienstleistungen beträgt 160,00 € netto. Für Wartungspakete mit jährlicher Laufzeit gewähren wir 10 % Nachlass. Abweichende Satzvereinbarungen gelten nur, wenn sie schriftlich in einem Angebot bestätigt wurden.`,tags:`FAQ, Preise, Beratung, Stundensatz`,erstelltAm:s(28),aktualisiertAm:s(5)},{id:6,mandantId:m,titel:`Antwort auf verdächtige Mails (Phishing/Spam)`,inhalt:`E-Mails, die persönliche Daten, Bankverbindungen oder Vorauszahlungen verlangen, beantworten wir nicht inhaltlich. Wir dokumentieren den Vorgang intern, markieren die Nachricht als Spam und informieren bei Verdacht auf Betrug die zuständige Stelle. Keine Anhänge solcher Mails öffnen.`,tags:`FAQ, Spam, Sicherheit`,erstelltAm:s(20),aktualisiertAm:s(3)}];function ie(e){let t=e;return function(){t|=0,t=t+1831565813|0;let e=Math.imul(t^t>>>15,1|t);return e=e+Math.imul(e^e>>>7,61|e)^e,((e^e>>>14)>>>0)/4294967296}}var T=(e,t)=>{let n=10**t;return Math.round(e*n)/n},E=ie(20260929),D=Array.from({length:30},(e,t)=>{let n=i(29-t),a=n.getDay(),o=a===0,s=0,c=0;return o||(s=T((a===6?.11:.22)+E()*.24,4),c=Math.max(1,Math.round(s/.008))),{tag:r(n),mandantId:m,firmenname:f.firmenname,kosten:s,anzahlCalls:c}}),O=D.filter(n=>n.tag.startsWith(`${e.getFullYear()}-${t(e.getMonth()+1)}`)),k=T(O.reduce((e,t)=>e+t.kosten,0),4),A=O.reduce((e,t)=>e+t.anzahlCalls,0),j=[{mandantId:m,firmenname:f.firmenname,monatlichesLimitUsd:f.monatlichesLimitUsd,limitVerhalten:f.limitVerhalten,fallbackModellId:f.fallbackModellId,gesamtKostenMonat:k,anzahlApiCalls:A,totalInputTokens:A*1180,totalOutputTokens:A*430,limitAuslastungProzent:T(k/f.monatlichesLimitUsd*100,1),schwellenwertErreicht:k>=f.monatlichesLimitUsd*.8}],M=[{id:6,userId:p,zeitpunkt:o(1),aktion:`ENTWURF_ERSTELLT`,details:`KI-Antwortentwurf für Mail 1 (Angebot für IT-Beratung) erstellt`,userName:`${h.vorname} ${h.nachname}`,mailId:1,mailBetreff:S[1].betreff},{id:5,userId:p,zeitpunkt:o(4),aktion:`ENTWURF_GESPEICHERT`,details:`Entwurf 2 manuell bearbeitet und gespeichert`,userName:`${h.vorname} ${h.nachname}`,mailId:2,mailBetreff:S[2].betreff},{id:4,userId:p,zeitpunkt:s(2),aktion:`VERSANDT`,details:`Entwurf 9 versendet an anna.schmidt@example.com via GMAIL (demo@mailpilot.de) [DEMO-MODUS - simulierter Versand]`,userName:`${h.vorname} ${h.nachname}`,mailId:9,mailBetreff:S[9].betreff},{id:3,userId:p,zeitpunkt:s(9),aktion:`VERSANDT`,details:`Entwurf 8 versendet an anna.schmidt@example.com via GMAIL (demo@mailpilot.de) [DEMO-MODUS - simulierter Versand]`,userName:`${h.vorname} ${h.nachname}`,mailId:8,mailBetreff:S[8].betreff},{id:2,userId:p,zeitpunkt:s(12),aktion:`WISSENSBASIS_ANGELEGT`,details:`Wissensbasis-Eintrag "Wie läuft eine Reklamation ab?" angelegt`,userName:`${h.vorname} ${h.nachname}`,mailId:null,mailBetreff:null},{id:1,userId:p,zeitpunkt:s(45),aktion:`POSTFACH_VERBUNDEN`,details:`Postfach demo@mailpilot.de (GMAIL) erfolgreich verbunden`,userName:`${h.vorname} ${h.nachname}`,mailId:null,mailBetreff:null}],ae={content:M,page:{size:50,number:0,totalElements:M.length,totalPages:1},totalElements:M.length,totalPages:1,size:50,number:0,numberOfElements:M.length,first:!0,last:!0,empty:M.length===0},oe=b,N=b,P={mandant:f,benutzer:h,postfach:g,mails:ne,mailDetails:S,threads:C,anhaenge:re,wissensbasis:w,kostenUebersicht:j,kostenVerlauf:D,auditLog:ae,einstellungen:{mandantId:m,firmenname:f.firmenname,bevorzugtesModellId:f.bevorzugtesModellId,globalClassifyModel:oe,globalDraftModel:N}},F=`mailpilot-demo-state`,I=1,L=null,R=e=>e===void 0?void 0:JSON.parse(JSON.stringify(e)),z=e=>String(e).padStart(2,`0`);function B(){let e=new Date;return`${e.getFullYear()}-${z(e.getMonth()+1)}-${z(e.getDate())}T${z(e.getHours())}:${z(e.getMinutes())}:${z(e.getSeconds())}`}function se(){let e=new Date;return`${e.getFullYear()}-${z(e.getMonth()+1)}-${z(e.getDate())}`}function V(e,t=e=>e.id){return e.reduce((e,n)=>Math.max(e,t(n)||0),0)}function H(){let e=Object.values(P.mailDetails).map(e=>e.entwurf).filter(Boolean),t=Object.values(P.anhaenge).flat().filter(Boolean);return{version:I,benutzer:R(P.benutzer),postfaecher:[R(P.postfach)],mailDetails:R(P.mailDetails),threads:R(P.threads),anhaenge:R(P.anhaenge),wissensbasis:R(P.wissensbasis),einstellungen:R(P.einstellungen),kostenUebersicht:R(P.kostenUebersicht),kostenVerlauf:R(P.kostenVerlauf),auditLog:R(P.auditLog.content),naechsteIds:{entwurf:V(e)+1,wissensbasis:V(P.wissensbasis)+1,auditLog:V(P.auditLog.content)+1,anhang:V(t)+1}}}function U(){try{let e=window.sessionStorage.getItem(F);if(!e)return null;let t=JSON.parse(e);return!t||t.version!==I||!t.mailDetails||!t.benutzer||!t.naechsteIds?null:t}catch{return null}}function W(){try{window.sessionStorage.setItem(F,JSON.stringify(L))}catch{}}function G(){return L||=U()||H(),L}function K(){return L=H(),W(),L}function q(e){let t=e(G());return W(),t}function ce(){let e=G();return e.postfaecher[0]?e.postfaecher[0].id:P.postfach.id}function le(e){return{id:e.id,postfachId:ce(),absender:e.absender,betreff:e.betreff,empfangenAm:e.empfangenAm,gelesenAm:e.gelesenAm,status:e.status,kategorie:e.kategorie,dringlichkeit:e.dringlichkeit,eskalationNoetig:e.eskalationNoetig,eskalationGrund:e.eskalationGrund,hatEntwurf:e.entwurf!==null&&e.entwurf!==void 0,entwurfId:e.entwurf?e.entwurf.id:null}}function J(e){let t=G(),n=e?String(e).toUpperCase():null;return R(Object.values(t.mailDetails).map(le).filter(e=>!n||e.status===n).sort((e,t)=>t.empfangenAm.localeCompare(e.empfangenAm)))}function ue(e){let t=G().mailDetails[e];return t?R(t):null}function Y(e){let t=e.inhaltRoh||``;return{id:e.id,absender:e.absender,betreff:e.betreff,empfangenAm:e.empfangenAm,inhaltVorschau:t.length>150?`${t.substring(0,150)}...`:t,status:e.status}}function de(e){let t=G(),n=t.mailDetails[e];if(!n)return null;let r=t.threads[e];if(!r)return{threadId:null,mails:[Y(n)]};let i=r.mails.map(e=>t.mailDetails[e.id]).filter(Boolean).map(Y);return{threadId:r.threadId,mails:i}}function X(e,t,n){let r=G(),i=n?r.mailDetails[n]:null,a={id:r.naechsteIds.auditLog,userId:1,zeitpunkt:B(),aktion:e,details:t,userName:`${r.benutzer.vorname} ${r.benutzer.nachname}`,mailId:i?i.id:null,mailBetreff:i?i.betreff:null};return r.naechsteIds.auditLog+=1,r.auditLog.push(a),a}function fe({benutzerId:e,page:t=0,size:n=50}={}){let r=G().auditLog.filter(t=>!e||t.userId===Number(e)).slice().sort((e,t)=>t.zeitpunkt.localeCompare(e.zeitpunkt)),i=Number(n)>0?Number(n):50,a=Number(t)>0?Number(t):0,o=Math.max(1,Math.ceil(r.length/i)),s=r.slice(a*i,a*i+i);return{content:R(s),page:{size:i,number:a,totalElements:r.length,totalPages:o},totalElements:r.length,totalPages:o,size:i,number:a,numberOfElements:s.length,first:a===0,last:a>=o-1,empty:s.length===0}}function pe(e){let t=G().auditLog.filter(t=>!e||t.userId===Number(e)).slice().sort((e,t)=>t.zeitpunkt.localeCompare(e.zeitpunkt)),n=e=>`"${String(e??``).replace(/"/g,`""`)}"`,r=(...e)=>e.map(n).join(`;`);return[`\uFEFF${r(`Zeitpunkt`,`Benutzer`,`Aktion`,`Details`,`Mail-Betreff`)}`,...t.map(e=>r(e.zeitpunkt.replace(`T`,` `),e.userName,e.aktion,e.details,e.mailBetreff))].join(`\r
`)+`\r
`}function me(e,t,n){return q(r=>{let i=r.mailDetails[e];if(!i)return null;let a={id:r.naechsteIds.entwurf,mailId:i.id,entwurfText:t,llmModellVerwendet:n,erstelltAm:B(),bearbeitetVonUserId:null,finalText:null,versendetAm:null,autoGeneriert:!0};return r.naechsteIds.entwurf+=1,i.entwurf=a,i.status=`ENTWURF_ERSTELLT`,X(`ENTWURF_ERSTELLT`,`KI-Antwortentwurf für Mail ${i.id} (${i.betreff}) erstellt`,i.id),R(a)})}function he(e,t){return q(n=>{let r=n.mailDetails[e];return!r||!r.entwurf?null:(r.entwurf.entwurfText=t,r.entwurf.bearbeitetVonUserId=1,X(`ENTWURF_GESPEICHERT`,`Entwurf ${r.entwurf.id} manuell bearbeitet und gespeichert`,r.id),R(r.entwurf))})}function ge(e,t,n){return q(r=>{let i=r.mailDetails[e];if(!i||!i.entwurf)return null;let a=n&&n.trim()?n:i.entwurf.entwurfText,o=r.postfaecher[0]||P.postfach,s=B();return i.entwurf.finalText=a,i.entwurf.versendetAm=s,i.entwurf.bearbeitetVonUserId=Number(t)||1,i.status=`VERSENDET`,i.gelesenAm=s,X(`VERSANDT`,`Entwurf ${i.entwurf.id} versendet an ${i.absender} via ${o.provider} (${o.emailAdresse}) [DEMO-MODUS - simulierter Versand]`,i.id),R(i.entwurf)})}function _e(){return R(G().postfaecher)}function ve(e){return q(t=>{let n=t.postfaecher.find(t=>t.id===Number(e));return n?(n.aktiv=!1,R(n)):null})}function Z(){return R(G().wissensbasis)}function ye(e){let t=String(e||``).trim().toLowerCase();return t?Z().filter(e=>[e.titel,e.inhalt,e.tags].filter(Boolean).some(e=>String(e).toLowerCase().includes(t))):Z()}function be({titel:e,inhalt:t,tags:n}){return q(r=>{let i=B(),a={id:r.naechsteIds.wissensbasis,mandantId:r.benutzer.mandantId,titel:e,inhalt:t,tags:n||null,erstelltAm:i,aktualisiertAm:i};return r.naechsteIds.wissensbasis+=1,r.wissensbasis.push(a),X(`WISSENSBASIS_ANGELEGT`,`Wissensbasis-Eintrag "${e}" angelegt`,null),R(a)})}function xe(e,{titel:t,inhalt:n,tags:r}){return q(i=>{let a=i.wissensbasis.find(t=>t.id===Number(e));return a?(a.titel=t,a.inhalt=n,a.tags=r||null,a.aktualisiertAm=B(),R(a)):null})}function Se(e){return q(t=>{let n=t.wissensbasis.findIndex(t=>t.id===Number(e));if(n===-1)return!1;let[r]=t.wissensbasis.splice(n,1);return X(`WISSENSBASIS_GELOESCHT`,`Wissensbasis-Eintrag "${r.titel}" gelöscht`,null),!0})}function Q(){let e=G();return{mandantId:e.benutzer.mandantId,firmenname:e.benutzer.firmenname,bevorzugtesModellId:e.einstellungen.bevorzugtesModellId,globalClassifyModel:e.einstellungen.globalClassifyModel,globalDraftModel:e.einstellungen.globalDraftModel}}function Ce({bevorzugtesModellId:e}){return q(t=>{let n=typeof e==`string`&&e.trim()?e.trim():null;return t.einstellungen.bevorzugtesModellId=n,Q()})}function we(){return R(G().kostenUebersicht)}function Te(){return R(G().kostenVerlauf)}function $(){let e=G(),t={sub:`1`,email:e.benutzer.email,mandantId:e.benutzer.mandantId,rolle:e.benutzer.rolle,demoModus:e.benutzer.demoModus===!0,emailVerifiziert:e.benutzer.emailVerifiziert===!0,aboStatus:e.benutzer.aboStatus,trialEndeAm:e.benutzer.trialEndeAm,firmenname:e.benutzer.firmenname,vorname:e.benutzer.vorname,nachname:e.benutzer.nachname};return`demo-header.${btoa(JSON.stringify(t)).replace(/=+$/,``)}.demo-signatur`}function Ee(){let e=G();return{token:$(),email:e.benutzer.email,vorname:e.benutzer.vorname,nachname:e.benutzer.nachname,rolle:e.benutzer.rolle,mandantId:e.benutzer.mandantId,firmenname:e.benutzer.firmenname,demoModus:e.benutzer.demoModus===!0,emailVerifiziert:e.benutzer.emailVerifiziert===!0,aboStatus:e.benutzer.aboStatus,trialEndeAm:e.benutzer.trialEndeAm,plan:e.benutzer.plan}}export{de as C,ye as E,K as S,Z as T,Se as _,fe as a,_e as b,ve as c,be as d,G as f,Te as g,we as h,pe as i,Q as l,B as m,he as n,$ as o,se as p,xe as r,Ee as s,Ce as t,me as u,ue as v,ge as w,X as x,J as y};