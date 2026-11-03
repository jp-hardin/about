/**
 * Middle Market website forms: report downloads, report subscriptions, the general contact form and email preferences.
 *
 * Lives as the "MMT Website Forms" Apps Script project in Drive, writing to the "MMT Report Downloads" sheet
 * (SHEET_ID). Deploy > Manage deployments > edit the web app > Version: New version, so the /exec address in
 * REPORT_FORM_URL (_build/build.py) stays the same. A first deployment is Deploy > New deployment > Web app,
 * Execute as: Me, Who has access: Anyone.
 *
 * Tabs (all with the same columns):
 *   All Submissions   every subscription, contact form and unsubscribe request
 *   General Form      the contact form on the site
 *   Subscriptions     every report subscription
 *   Report Downloads  every report download (the PDF downloads without a form, so most rows have no name)
 *   Industrials, Business Services, Consumer, Healthcare, Technology   subscribers to that industry's reports
 * Columns: First Name | Last Name | Email | Industrials | Business Services | Consumer | Healthcare | Technology |
 *          Newsletter Opt-In | Report Opt-In | Newsletter Opt-Out | Report Opt-Out | Date | Source | Report | Notes
 * An industry column reads Yes for a subscription to it, or "Opted out <date>" after an unsubscribe.
 *
 * The site posts:
 *   download     report, page (and email, when this browser subscribed before)
 *   subscribe    first_name, last_name, email, industries (comma separated), newsletter (yes/no), terms_version,
 *                report, page
 *   contact      first_name, last_name, email, details, page
 *   unsubscribe  email, reports (yes = all industry reports), industries (comma separated), newsletter (yes = stop)
 */
var SHEET_ID = '1ZwPmuSspyIsl2TQvP-emN2PXx062m26St7d5CnkSlbE';
var TZ = 'America/New_York';
var ALL = 'All Submissions', GENERAL = 'General Form', SUBS = 'Subscriptions', DOWNLOADS = 'Report Downloads';
var INDUSTRIES = ['Industrials', 'Business Services', 'Consumer', 'Healthcare', 'Technology'];
var HEADER = ['First Name', 'Last Name', 'Email'].concat(INDUSTRIES).concat(['Newsletter Opt-In', 'Report Opt-In',
              'Newsletter Opt-Out', 'Report Opt-Out', 'Date', 'Source', 'Report', 'Notes']);
var COL = {}; HEADER.forEach(function (h, i) { COL[h] = i + 1; });

function doPost(e) {
  var p = (e && e.parameter) || {};
  if (p.company_website) return done();                       // filled in only by spam bots
  var email = String(p.email || '').trim().toLowerCase();
  var validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) && email.length <= 160;
  if (p.action !== 'download' && !validEmail) return done();

  var book = SpreadsheetApp.openById(SHEET_ID);
  var now = Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm');
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    if (p.action === 'download') {
      add(book, [DOWNLOADS], row({email: validEmail ? email : '', date: now, source: 'Download',
        report: clean(p.report), notes: clean('Page: ' + p.page)}));
    } else if (p.action === 'subscribe') {
      var chosen = industriesOf(p.industries);
      var r = row({first: clean(p.first_name), last: clean(p.last_name), email: email, industries: chosen,
        newsletter: p.newsletter === 'yes' ? 'Yes' : 'No', reports: chosen.length ? 'Yes' : 'No', date: now,
        source: 'Subscribe form', report: clean(p.report),
        notes: clean('Agreed to Report Terms (version ' + p.terms_version + '). Page: ' + p.page)});
      add(book, [ALL, SUBS].concat(chosen), r);
    } else if (p.action === 'contact') {
      add(book, [ALL, GENERAL], row({first: clean(p.first_name), last: clean(p.last_name), email: email, date: now,
        source: 'General form', notes: clean((p.details ? p.details + '. ' : '') + 'Page: ' + p.page, 2000)}));
    } else if (p.action === 'unsubscribe') {
      unsubscribe(book, email, p.newsletter === 'yes', p.reports === 'yes', industriesOf(p.industries), now);
    }
  } finally {
    lock.releaseLock();
  }
  return done();
}

function industriesOf(list) {
  var asked = String(list || '').split(',').map(function (x) { return x.trim(); });
  return INDUSTRIES.filter(function (n) { return asked.indexOf(n) !== -1; });
}

function row(o) {
  var r = HEADER.map(function () { return ''; });
  r[COL['First Name'] - 1] = o.first || '';
  r[COL['Last Name'] - 1] = o.last || '';
  r[COL['Email'] - 1] = o.email || '';
  (o.industries || []).forEach(function (n) { r[COL[n] - 1] = 'Yes'; });
  r[COL['Newsletter Opt-In'] - 1] = o.newsletter || '';
  r[COL['Report Opt-In'] - 1] = o.reports || '';
  r[COL['Newsletter Opt-Out'] - 1] = o.newsletterOut || '';
  r[COL['Report Opt-Out'] - 1] = o.reportsOut || '';
  r[COL['Date'] - 1] = o.date || '';
  r[COL['Source'] - 1] = o.source || '';
  r[COL['Report'] - 1] = o.report || '';
  r[COL['Notes'] - 1] = o.notes || '';
  return r;
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

function add(book, names, r) {
  names.forEach(function (n) { tab(book, n).appendRow(r); });
}

// Marks the opt-out on every row for the address in every tab, and logs the request on All Submissions.
// All reports: the Report Opt-Out date and every industry column. Some industries: only those columns.
function unsubscribe(book, email, newsletter, allReports, industries, now) {
  var stop = allReports ? INDUSTRIES : industries, found = false;
  book.getSheets().forEach(function (sheet) {
    var rows = sheet.getDataRange().getValues();
    for (var r = 1; r < rows.length; r++) {
      if (String(rows[r][COL['Email'] - 1]).trim().toLowerCase() !== email) continue;
      found = true;
      if (newsletter) sheet.getRange(r + 1, COL['Newsletter Opt-Out']).setValue(now);
      if (allReports) sheet.getRange(r + 1, COL['Report Opt-Out']).setValue(now);
      stop.forEach(function (n) {
        if (rows[r][COL[n] - 1] === 'Yes') sheet.getRange(r + 1, COL[n]).setValue('Opted out ' + now);
      });
    }
  });
  var what = [];
  if (newsletter) what.push('newsletter');
  if (allReports) what.push('all industry reports'); else if (industries.length) what.push(industries.join(', ') + ' reports');
  tab(book, ALL).appendRow(row({email: email, newsletterOut: newsletter ? now : '', reportsOut: allReports ? now : '',
    date: now, source: 'Unsubscribe', notes: 'Unsubscribe from ' + (what.join(' and ') || 'nothing selected') +
    (found ? ' (earlier rows updated)' : ' (address not on file)')}));
}

// Plain text only, and nothing a spreadsheet would read as a formula.
function clean(v, max) {
  var s = String(v == null ? '' : v).replace(/[\r\n\t]+/g, ' ').trim().slice(0, max || 300);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function done() {
  return ContentService.createTextOutput('ok');
}
