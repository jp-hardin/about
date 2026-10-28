/**
 * Middle Market website forms: report downloads, the general contact form and email preferences.
 *
 * Lives as the "MMT Website Forms" Apps Script project in Drive, writing to the "MMT Report Downloads" sheet
 * (SHEET_ID). Deploy > New deployment > Web app, Execute as: Me, Who has access: Anyone. Put the /exec address
 * it gives into REPORT_FORM_URL in _build/build.py and rebuild the site.
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
 */
var SHEET_ID = '1ZwPmuSspyIsl2TQvP-emN2PXx062m26St7d5CnkSlbE';
var TZ = 'America/New_York';
var ALL = 'All Submissions', GENERAL = 'General Form', DOWNLOADS = 'Report Downloads';
var INDUSTRIES = ['Industrials', 'Business Services', 'Consumer', 'Healthcare', 'Technology'];
var HEADER = ['First Name', 'Last Name', 'Email', 'Newsletter Opt-In', 'Report Opt-In', 'Newsletter Opt-Out',
              'Report Opt-Out', 'Date', 'Notes'];

function doPost(e) {
  var p = (e && e.parameter) || {};
  if (p.company_website) return done();                       // filled in only by spam bots
  var email = String(p.email || '').trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 160) return done();

  var book = SpreadsheetApp.openById(SHEET_ID);
  var now = Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm');
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    if (p.action === 'unsubscribe') {
      unsubscribe(book, email, p.newsletter === 'yes', p.reports === 'yes', now);
    } else if (p.action === 'contact') {
      var row = [clean(p.first_name), clean(p.last_name), email, '', '', '', '', now,
                 clean('General form' + (p.details ? ': ' + p.details : '') + '. Page: ' + p.page, 2000)];
      add(book, [ALL, GENERAL], row);
    } else {
      var report = clean(p.report), tabs = [ALL, DOWNLOADS], industry = industryOf(report);
      if (industry) tabs.push(industry);
      var row = p.returning === 'yes'
        ? ['', '', email, '', '', '', '', now, clean('Repeat download: ' + report + '. Page: ' + p.page)]
        : [clean(p.first_name), clean(p.last_name), email,
           p.newsletter === 'yes' ? 'Yes' : 'No', p.reports === 'yes' ? 'Yes' : 'No', '', '', now,
           clean('Downloaded: ' + report + '. Agreed to Report Terms (version ' + p.terms_version + '). Page: ' + p.page)];
      add(book, tabs, row);
    }
  } finally {
    lock.releaseLock();
  }
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

function add(book, names, row) {
  names.forEach(function (n) { tab(book, n).appendRow(row); });
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
}

// Plain text only, and nothing a spreadsheet would read as a formula.
function clean(v, max) {
  var s = String(v == null ? '' : v).replace(/[\r\n\t]+/g, ' ').trim().slice(0, max || 300);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function done() {
  return ContentService.createTextOutput('ok');
}
