import{t as e}from"./axios-CIEBgY9x.js";import{C as t,E as n,T as r,_ as i,a,b as o,c as s,d as c,f as l,g as u,h as d,i as f,l as p,n as m,p as ee,r as te,s as ne,t as re,u as ie,v as h,w as g,y as _}from"./demoStore-DXyciz1y.js";var v=`deepseek/deepseek-v4.1-flash`,y={ANFRAGE:`Sehr geehrte Damen und Herren,

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
Kundenservice`};function b(e){return y[e]??y.SONSTIGES}var x=700,S=`In der Demo nicht verfügbar.`,C=e=>new Promise(t=>setTimeout(t,e)),w=e=>Number.parseInt(e,10),T=()=>({status:403,data:{error:S}}),E=()=>({status:404,data:null}),D=(e,t)=>({status:e,data:{error:t}});async function O(e){let t=e.data;if(t==null)return null;if(typeof t==`string`)try{return JSON.parse(t)}catch{return null}if(typeof FormData<`u`&&t instanceof FormData){let e=t.get(`request`);if(e&&typeof e.text==`function`)try{return JSON.parse(await e.text())}catch{return null}return null}return typeof t==`object`?t:null}function k(e){return e.params||{}}var A=()=>({status:200,data:ne()}),j=({query:e})=>({status:200,data:_(e.status)}),M=({params:e})=>{let t=h(w(e.mailId));return t?{status:200,data:t}:E()},N=({params:e})=>{let n=t(w(e.mailId));return n?{status:200,data:n}:E()},P=({params:e})=>({status:200,data:l().anhaenge?.[w(e.mailId)]||[]}),ae=async({params:e})=>{let t=w(e.mailId),n=h(t);if(!n)return E();if(n.status===`ESKALIERT`)return D(400,`Eskalierte E-Mails erhalten keinen automatischen Entwurf.`);await C(x+Math.random()*800);let r=ie(t,b(n.kategorie),v);return r?{status:201,data:r}:E()},F=({params:e})=>{let t=h(w(e.mailId));return t?t.entwurf?{status:200,data:t.entwurf}:{status:404,data:{error:`Kein Entwurf vorhanden.`}}:E()},I=({params:e,body:t})=>{let n=w(e.mailId),r=h(n);if(!r||!r.entwurf)return E();let i=t&&typeof t.entwurfText==`string`?t.entwurfText:``,a=m(n,i);return a?{status:200,data:a}:E()},L=({params:e,body:t})=>{let n=w(e.mailId),r=h(n);if(!r)return E();if(!t||t.userId===void 0||t.userId===null)return D(400,`userId ist erforderlich`);if(r.status===`VERSENDET`)return D(400,`E-Mail ${n} wurde bereits versendet.`);if(r.status===`ESKALIERT`)return D(400,`Eskalierte E-Mails können nicht versendet werden. Bitte manuell bearbeiten.`);if(!r.entwurf)return D(400,`Kein Entwurf für E-Mail ${n} vorhanden. Bitte zuerst einen Entwurf erstellen.`);let i=g(n,t.userId,t.finalText);return i?{status:200,data:i}:E()},R=()=>({status:200,data:d()}),z=()=>({status:200,data:u()}),B=()=>({status:200,data:{status:`OK`,mandanten:`1`}}),V=({query:e})=>({status:200,data:a({benutzerId:e.benutzerId,page:e.page===void 0?0:w(e.page),size:e.size===void 0?50:w(e.size)})}),H=({params:e,query:t})=>({status:200,data:f(t.benutzerId),headers:{"content-type":`text/csv; charset=UTF-8`,"content-disposition":`attachment; filename="auditlog-mandant-${e.mandantId}-${ee()}.csv"`}}),U=()=>({status:200,data:o()}),W=({params:e})=>s(w(e.id))?{status:204,data:null}:E(),G=()=>({status:200,data:p()}),K=({body:e})=>({status:200,data:{gespeichert:!0,...re({bevorzugtesModellId:e?e.bevorzugtesModellId:null})}}),q=()=>({status:200,data:r()}),J=({query:e})=>({status:200,data:n(e.q)}),oe=({body:e})=>{let t=e||{};return!t.titel||!t.inhalt?D(400,`Titel und Inhalt sind erforderlich.`):{status:201,data:c({titel:t.titel,inhalt:t.inhalt,tags:t.tags})}},se=({params:e,body:t})=>{let n=t||{};if(!n.titel||!n.inhalt)return D(400,`Titel und Inhalt sind erforderlich.`);let r=te(w(e.id),{titel:n.titel,inhalt:n.inhalt,tags:n.tags});return r?{status:200,data:r}:E()},ce=({params:e})=>i(w(e.id))?{status:204,data:null}:E(),Y=`(?<mandantId>\\d+)`,X=`(?<mailId>\\d+)`,Z=`(?<id>\\d+)`,le=[{methode:`post`,muster:`/auth/login`,handler:A},{methode:`post`,muster:`/auth/register`,handler:T},{methode:`post`,muster:`/auth/register-firma`,handler:T},{methode:`post`,muster:`/auth/passwort-vergessen`,handler:T},{methode:`post`,muster:`/auth/passwort-zuruecksetzen`,handler:T},{methode:`get`,muster:`/auth/verifizieren`,handler:T},{methode:`post`,muster:`/auth/verifizierung-senden`,handler:T},{methode:`get`,muster:`/mandanten/${Y}/mails`,handler:j},{methode:`get`,muster:`/mandanten/${Y}/mails/${X}`,handler:M},{methode:`post`,muster:`/mandanten/${Y}/mails/${X}/entwurf`,handler:ae},{methode:`get`,muster:`/mandanten/${Y}/mails/${X}/entwurf`,handler:F},{methode:`put`,muster:`/mandanten/${Y}/mails/${X}/entwurf`,handler:I},{methode:`post`,muster:`/mandanten/${Y}/mails/${X}/versenden`,handler:L},{methode:`post`,muster:`/mandanten/${Y}/mails/${X}/versenden-mit-anhang`,handler:L},{methode:`get`,muster:`/mandanten/${Y}/mails/${X}/anhaenge`,handler:P},{methode:`get`,muster:`/mandanten/${Y}/mails/${X}/thread`,handler:N},{methode:`get`,muster:`/mandanten/${Y}/wissensbasis/suche`,handler:J},{methode:`get`,muster:`/mandanten/${Y}/wissensbasis`,handler:q},{methode:`post`,muster:`/mandanten/${Y}/wissensbasis`,handler:oe},{methode:`put`,muster:`/mandanten/${Y}/wissensbasis/${Z}`,handler:se},{methode:`delete`,muster:`/mandanten/${Y}/wissensbasis/${Z}`,handler:ce},{methode:`get`,muster:`/mandanten/${Y}/auditlog/export`,handler:H},{methode:`get`,muster:`/mandanten/${Y}/auditlog`,handler:V},{methode:`get`,muster:`/mandanten/${Y}/postfaecher/verbinden/google`,handler:T},{methode:`get`,muster:`/mandanten/${Y}/postfaecher/verbinden/outlook`,handler:T},{methode:`post`,muster:`/mandanten/${Y}/postfaecher/generisch`,handler:T},{methode:`get`,muster:`/mandanten/${Y}/postfaecher`,handler:U},{methode:`delete`,muster:`/mandanten/${Y}/postfaecher/${Z}`,handler:W},{methode:`get`,muster:`/autodiscover`,handler:T},{methode:`get`,muster:`/admin/kosten/verlauf`,handler:z},{methode:`get`,muster:`/admin/kosten`,handler:R},{methode:`get`,muster:`/admin/health`,handler:B},{methode:`get`,muster:`/admin/mandanten/${Y}/einstellungen`,handler:G},{methode:`put`,muster:`/admin/mandanten/${Y}/einstellungen`,handler:K},{methode:`post`,muster:`/billing/checkout-session`,handler:T}].map(e=>({...e,regex:RegExp(`^${e.muster}/?$`)}));function ue(e,t){return le.find(n=>n.methode===e&&n.regex.test(t))||null}var Q={200:`OK`,201:`Created`,204:`No Content`,400:`Bad Request`,403:`Forbidden`,404:`Not Found`};function de(t,n){let r=n.data&&n.data.error||`Request failed with status code ${n.status}`;if(typeof e.AxiosError==`function`)return new e.AxiosError(r,String(n.status),t,{},n);let i=Error(r);return i.isAxiosError=!0,i.config=t,i.response=n,i}function $(){return async function(e){let t=(e.method||`get`).toLowerCase(),n=String(e.url||``).split(`?`)[0],r=ue(t,n),i=r?r.regex.exec(n):null,a;if(!r||!i)a={status:404,data:{error:`Demo-Adapter: kein Handler für ${t.toUpperCase()} ${n}`}};else{let t=await O(e);try{a=await r.handler({config:e,params:i.groups||{},body:t,query:k(e)})}catch(e){a={status:500,data:{error:e.message||`Demo-Adapter-Fehler`}}}}let o=a.status||200,s={data:o===204?null:a.data,status:o,statusText:Q[o]||``,headers:a.headers||{},config:e,request:{}};if(e.validateStatus?e.validateStatus(o):o>=200&&o<300)return s;throw de(e,s)}}export{$ as createDemoAdapter,$ as default};