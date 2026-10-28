/**
 * Middle Market website forms: report downloads, the general contact form and email preferences.
 *
 * Lives in the "MMT Report Downloads" Google Sheet (Extensions > Apps Script), writing to that sheet (SHEET_ID).
 * Deploy > New deployment > Web app, Execute as: Me, Who has access: Anyone. Put the /exec address it gives into
 * REPORT_FORM_URL in _build/build.py and rebuild the site. After pasting a new version of this file: run
 * authorize() once from the editor, then Deploy > Manage deployments > edit > Version: New version > Deploy (the
 * /exec address stays the same).
 *
 * Tabs (all with the same columns):
 *   All Submissions   every form submission and unsubscribe request
 *   General Form      the contact form on the site
 *   Report Downloads  every industry report download
 *   Industrials, Business Services, Consumer, Healthcare, Technology   downloads of that industry's reports
 * Columns: First Name | Last Name | Email | Newsletter Opt-In | Report Opt-In | Newsletter Opt-Out | Report Opt-Out | Date | Notes
 *
 * The site posts:
 *   download     first_name, last_name, email, reports, newsletter (yes/no), terms_version, report, page
 *                (a returning visitor sends returning=yes and the email it gave before)
 *   contact      first_name, last_name, email, details, page
 *   unsubscribe  email, reports, newsletter (yes = stop sending)
 *
 * Lead research: each new download and contact form submission is queued. About a minute later, processQueue()
 * asks Claude (Anthropic API, with web search) to research the person and the company from public business
 * sources, adds the findings to that row's Notes in every tab it was written to, and emails the submission and the
 * research to NOTIFY_TO. Repeat downloads and unsubscribes get a short email without research.
 * Script properties (Project Settings > Script properties): ANTHROPIC_API_KEY (required for research),
 * NOTIFY_TO (optional; default mmt@benchmarkintl.com).
 */
var SHEET_ID = '1ZwPmuSspyIsl2TQvP-emN2PXx062m26St7d5CnkSlbE';
var TZ = 'America/New_York';
var ALL = 'All Submissions', GENERAL = 'General Form', DOWNLOADS = 'Report Downloads';
var INDUSTRIES = ['Industrials', 'Business Services', 'Consumer', 'Healthcare', 'Technology'];
var HEADER = ['First Name', 'Last Name', 'Email', 'Newsletter Opt-In', 'Report Opt-In', 'Newsletter Opt-Out',
              'Report Opt-Out', 'Date', 'Notes'];
var NOTES_COL = 9;
var MODEL = 'claude-opus-5-5';
var FREE_MAIL = /^(gmail|googlemail|yahoo|ymail|hotmail|outlook|live|msn|aol|icloud|me|mac|proton|protonmail|gmx|zoho|comcast|att|verizon|sbcglobal|bellsouth|cox|charter|earthlink)\./;

function doPost(e) {
  var p = (e && e.parameter) || {};
  if (p.company_website) return done();                       // filled in only by spam bots
  var email = String(p.email || '').trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 160) return done();

  var book = SpreadsheetApp.openById(SHEET_ID);
  var now = Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm');
  var job = null;
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    if (p.action === 'unsubscribe') {
      var found = unsubscribe(book, email, p.newsletter === 'yes', p.reports === 'yes', now);
      job = {kind: 'unsubscribe', email: email, newsletter: p.newsletter === 'yes', reports: p.reports === 'yes',
             found: found, date: now};
    } else if (p.action === 'contact') {
      var row = [clean(p.first_name), clean(p.last_name), email, '', '', '', '', now,
                 clean('General form' + (p.details ? ': ' + p.details : '') + '. Page: ' + p.page, 2000)];
      job = {kind: 'contact', first: row[0], last: row[1], email: email, details: clean(p.details, 2000),
             page: clean(p.page), date: now, rows: add(book, [ALL, GENERAL], row)};
    } else {
      var report = clean(p.report), tabs = [ALL, DOWNLOADS], industry = industryOf(report);
      if (industry) tabs.push(industry);
      if (p.returning === 'yes') {
        add(book, tabs, ['', '', email, '', '', '', '', now, clean('Repeat download: ' + report + '. Page: ' + p.page)]);
        job = {kind: 'repeat', email: email, report: report, date: now};
      } else {
        var row = [clean(p.first_name), clean(p.last_name), email,
                   p.newsletter === 'yes' ? 'Yes' : 'No', p.reports === 'yes' ? 'Yes' : 'No', '', '', now,
                   clean('Downloaded: ' + report + '. Agreed to Report Terms (version ' + p.terms_version + '). Page: ' + p.page)];
        job = {kind: 'download', first: row[0], last: row[1], email: email, report: report, industry: industry,
               newsletter: row[3], reports: row[4], date: now, rows: add(book, tabs, row)};
      }
    }
    if (job) enqueue(job);
  } finally {
    lock.releaseLock();
  }
  if (job) schedule();
  return done();
}

function industryOf(report) {
  for (var i = 0; i < INDUSTRIES.length; i++) if (report.indexOf(INDUSTRIES[i]) === 0) return INDUSTRIES[i];
  return '';
}

function tab(book, name) {
  var sheet = book.getSheetByName(name);
  if (!sheet) {
    sheet = book.insertSheet(name);
    sheet.appendRow(HEADER);
    sheet.getRange(1, 1, 1, HEADER.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

// Appends the row to each tab and returns {tab name: row number}, so the research can be added to the same rows.
function add(book, names, row) {
  var at = {};
  names.forEach(function (n) {
    var sheet = tab(book, n);
    sheet.appendRow(row);
    at[n] = sheet.getLastRow();
  });
  return at;
}

// Dates the opt-out on every row for the address in every tab, and logs the request on All Submissions.
function unsubscribe(book, email, newsletter, reports, now) {
  var found = false;
  book.getSheets().forEach(function (sheet) {
    var rows = sheet.getDataRange().getValues();
    for (var r = 1; r < rows.length; r++) {
      if (String(rows[r][2]).trim().toLowerCase() !== email) continue;
      found = true;
      if (newsletter) sheet.getRange(r + 1, 6).setValue(now);
      if (reports) sheet.getRange(r + 1, 7).setValue(now);
    }
  });
  tab(book, ALL).appendRow(['', '', email, '', '', newsletter ? now : '', reports ? now : '', now,
    found ? 'Unsubscribe request (earlier rows updated)' : 'Unsubscribe request (address not on file)']);
  return found;
}

// ---- Queue: the form gets an immediate answer; research and email run a minute later in the background ----

function enqueue(job) {
  var props = PropertiesService.getScriptProperties();
  var queue = JSON.parse(props.getProperty('queue') || '[]');
  queue.push(job);
  props.setProperty('queue', JSON.stringify(queue));
}

function schedule() {
  var pending = ScriptApp.getProjectTriggers().some(function (t) { return t.getHandlerFunction() === 'processQueue'; });
  if (!pending) ScriptApp.newTrigger('processQueue').timeBased().after(60 * 1000).create();
}

function processQueue() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'processQueue') ScriptApp.deleteTrigger(t);
  });
  var props = PropertiesService.getScriptProperties();
  var started = Date.now();
  while (Date.now() - started < 4 * 60 * 1000) {             // stay well inside the 6-minute run limit
    var lock = LockService.getScriptLock();
    lock.waitLock(10000);
    var queue = JSON.parse(props.getProperty('queue') || '[]');
    var job = queue.shift();
    props.setProperty('queue', JSON.stringify(queue));
    lock.releaseLock();
    if (!job) return;
    try {
      handle(job);
    } catch (err) {
      notify('Website form: ' + (job.email || 'submission') + ' (research failed)',
             describe(job) + '\nResearch could not run: ' + err + '\n');
    }
  }
  schedule();                                                 // more left: pick up again in a minute
}

function handle(job) {
  if (job.kind === 'unsubscribe') {
    var what = [job.reports ? 'industry reports' : '', job.newsletter ? 'newsletter' : ''].filter(String).join(' and ');
    notify('Unsubscribe: ' + job.email,
           job.email + ' asked to stop receiving the ' + (what || 'emails') + ' on ' + job.date + '.\n' +
           (job.found ? 'Their rows in the sheet are marked with the opt-out date.' : 'The address was not on the sheet.') +
           '\nPlease also remove them from the sending list within 10 business days.\n');
    return;
  }
  if (job.kind === 'repeat') {
    notify('Repeat download: ' + job.report + ' (' + job.email + ')',
           job.email + ' downloaded the ' + job.report + ' again on ' + job.date + '.\n' +
           'Their earlier submission and research are on the sheet.\n');
    return;
  }
  var research = researchLead(job);
  var stamp = 'Research ' + Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd') + ': ';
  writeNotes(job.rows, stamp + research.replace(/\s*\n\s*/g, ' | '));
  var who = [job.first, job.last].filter(String).join(' ') || job.email;
  var subject = job.kind === 'contact'
    ? 'New contact form: ' + who
    : 'New report download: ' + who + ' (' + (job.industry || job.report) + ')';
  notify(subject, describe(job) + '\nRESEARCH\n\n' + research + '\n\n' +
         'Research by Claude from public sources; verify before relying on it.\n' +
         'Sheet: https://docs.google.com/spreadsheets/d/' + SHEET_ID + '/edit\n');
}

function describe(job) {
  var lines = ['SUBMISSION', ''];
  if (job.kind === 'contact') lines.push('Form: website contact form');
  else lines.push('Form: report download', 'Report: ' + (job.report || ''));
  lines.push('Name: ' + [job.first, job.last].filter(String).join(' '), 'Email: ' + job.email, 'Date: ' + job.date + ' ET');
  if (job.kind === 'download') {
    lines.push('Wants new industry reports: ' + job.reports, 'Wants the newsletter: ' + job.newsletter);
  }
  if (job.details) lines.push('Details: ' + job.details);
  if (job.page) lines.push('Page: ' + job.page);
  return lines.join('\n') + '\n';
}

function writeNotes(rows, text) {
  var book = SpreadsheetApp.openById(SHEET_ID);
  Object.keys(rows || {}).forEach(function (name) {
    var cell = book.getSheetByName(name).getRange(rows[name], NOTES_COL);
    var before = String(cell.getValue() || '');
    cell.setValue(clean((before ? before + ' || ' : '') + text, 45000));
  });
}

function notify(subject, body) {
  var to = PropertiesService.getScriptProperties().getProperty('NOTIFY_TO') || 'mmt@benchmarkintl.com';
  MailApp.sendEmail({to: to, subject: subject, body: body, name: 'Middle Market Website'});
}

// ---- Lead research (Anthropic Messages API with web search) ----

var RESEARCH_SYSTEM = [
  'You research inbound leads for the Middle Market team at Benchmark International, a sell-side M&A advisor for',
  'privately held US companies with $50M to $500M in enterprise value in five industries: Industrials, Business',
  'Services, Consumer, Healthcare, and Technology. Someone just downloaded one of our industry reports or filled in',
  'our contact form. Help the team respond intelligently.',
  '',
  'Use web search to look up the person and the company from public business sources: the company website, press',
  'releases and news, professional profiles, industry directories, and filings. The email domain usually names the',
  'company; a personal email domain (gmail and the like) means the company may be unknown, so say so and work from',
  'the name and anything in the form details.',
  '',
  'Stick to professional and business information. Do not look for or report home addresses, family members,',
  'health, personal social media, or anything else private. If you cannot confirm something, write "Not found"',
  'rather than guessing, and say when a match is uncertain (for example, several people with the same name).',
  '',
  'Reply in plain text, no markdown symbols, under 350 words, with these headings on their own lines:',
  'PERSON: role, company, background, professional profile URL if found.',
  'COMPANY: what it does, headquarters, founded, employees and revenue if public, ownership (founder-owned, family,',
  'private equity backed, public), recent news.',
  'FIT: which of our industries and sectors it fits, whether it looks like a potential seller, a buyer, an advisor or',
  'service provider, a competitor, or a student or researcher, and how likely it is to be in our $50M to $500M range.',
  'TALKING POINTS: two or three specific things to raise when we reach out.',
  'CONFIDENCE: high, medium, or low, with one line on why.',
  'SOURCES: the URLs you relied on, one per line.'
].join('\n');

function researchLead(job) {
  var key = PropertiesService.getScriptProperties().getProperty('ANTHROPIC_API_KEY');
  if (!key) return 'Not researched: add ANTHROPIC_API_KEY under Project Settings > Script properties.';
  var domain = job.email.split('@')[1] || '';
  var facts = [
    'Name: ' + [job.first, job.last].filter(String).join(' '),
    'Email: ' + job.email + (FREE_MAIL.test(domain) ? ' (personal email provider)' : ' (company domain: ' + domain + ')'),
    job.kind === 'contact' ? 'Form: contact form' : 'Form: downloaded the ' + job.report,
    job.details ? 'Form details: ' + job.details : ''
  ].filter(String).join('\n');
  var messages = [{role: 'user', content: 'Research this lead:\n' + facts}];
  var payload = {
    model: MODEL,
    max_tokens: 8000,
    system: RESEARCH_SYSTEM,
    output_config: {effort: 'low'},
    fallbacks: 'default',
    tools: [{type: 'web_search_20260209', name: 'web_search', max_uses: 6}],
    messages: messages
  };
  var response;
  for (var turn = 0; turn < 3; turn++) {                     // resume if the server pauses a long search turn
    var res = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', {
      method: 'post',
      contentType: 'application/json',
      headers: {'x-api-key': key, 'anthropic-version': '2026-10-21', 'anthropic-beta': 'server-side-fallback-2026-07-01'},
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });
    if (res.getResponseCode() !== 200) {
      return 'Not researched: the research service returned ' + res.getResponseCode() + ' ' + res.getContentText().slice(0, 300);
    }
    response = JSON.parse(res.getContentText());
    if (response.stop_reason !== 'pause_turn') break;
    payload.messages = messages.concat([{role: 'assistant', content: response.content}]);
  }
  if (response.stop_reason === 'refusal') return 'Not researched: the research request was declined.';
  var text = [], sources = [];
  (response.content || []).forEach(function (block) {
    if (block.type !== 'text') return;
    text.push(block.text);
    (block.citations || []).forEach(function (c) { if (c.url && sources.indexOf(c.url) < 0) sources.push(c.url); });
  });
  var out = text.join('').trim() || 'Not found: the research returned no text.';
  if (sources.length && out.indexOf('SOURCES') < 0) out += '\n\nSOURCES\n' + sources.join('\n');
  return out;
}

// Run once from the editor after pasting this file, so Google asks for the permissions the research and email need.
function authorize() {
  SpreadsheetApp.openById(SHEET_ID).getName();
  ScriptApp.getProjectTriggers();
  MailApp.getRemainingDailyQuota();
  UrlFetchApp.fetch('https://api.anthropic.com', {muteHttpExceptions: true});
}

// Sends a test lead through the research and email without touching the sheet.
function testResearch() {
  var job = {kind: 'download', first: 'Jared', last: 'Hardin', email: 'j.hardin@benchmarkintl.com',
             report: 'Industrials Q4 2026 M&A Industry Report', industry: 'Industrials', newsletter: 'No',
             reports: 'No', date: Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm'), rows: {}};
  var research = researchLead(job);
  Logger.log(research);
  notify('TEST: lead research', describe(job) + '\nRESEARCH\n\n' + research + '\n');
}

// Plain text only, and nothing a spreadsheet would read as a formula.
function clean(v, max) {
  var s = String(v == null ? '' : v).replace(/[\r\n\t]+/g, ' ').trim().slice(0, max || 300);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function done() {
  return ContentService.createTextOutput('ok');
}
