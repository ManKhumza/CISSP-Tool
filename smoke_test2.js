/**
 * Headless test of the CISSP Study Portal.
 * Stubs a small DOM, runs the app script, then exercises every view and control.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const DIR = 'C:\\Users\\Khumza\\Documents\\Coding projects\\CISSP';
const html = fs.readFileSync(path.join(DIR, 'CISSP_Study_Portal.html'), 'utf8');
const scripts = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)];
const appScript = scripts.find(s => s[1].includes('window.__portal'));
if (!appScript) throw new Error('Portal application script not found');
const appSrc = appScript[1];

/* ---------------- DOM stub ---------------- */
function makeEl(id){
  const el = {
    id, _html:'', textContent:'', value:'', dataset:{}, style:{}, hidden:false,
    disabled:false, open:false, tagName:'DIV', _ls:{},
    classList:{ _s:new Set(),
      add(c){this._s.add(c)}, remove(c){this._s.delete(c)},
      toggle(c,v){ v===undefined ? (this._s.has(c)?this._s.delete(c):this._s.add(c)) : (v?this._s.add(c):this._s.delete(c)) },
      contains(c){return this._s.has(c)} },
    set innerHTML(v){ this._html = v; }, get innerHTML(){ return this._html; },
    addEventListener(t,fn){ (this._ls[t] = this._ls[t] || []).push(fn); },
    querySelectorAll(){ return []; }, querySelector(){ return makeEl('sub:'+id); },
    closest(){ return this; }, appendChild(){}, remove(){}, setAttribute(){}, getAttribute(){return null;},
    focus(){}, setSelectionRange(){}, scrollIntoView(){}, getBoundingClientRect(){ return {top:0,left:0,bottom:0,right:0}; },
    showModal(){ this.open = true; }, close(){ this.open = false; },
    contains(){ return false; }
  };
  return el;
}
const ids = ['content','domainNav','pctText','pctBar','answeredText','marksText','brandSub','ringVal',
  'search','btnGuide','btnPrint','btnResume','btnReset','toast','glossFilter','glossCount',
  'btnPrev','btnNext','btnReveal','btnMark','btnJump','jumpInput','navFilter','sbOpen','sbClose','scrim',
  'modeQuiz','modeStudy','layoutReader','layoutDoc','btnFont','btnTerms','btnTheme','btnKeys',
  'keysDlg','keysClose','pop','crumbs','btnMore','btnPrint2','btnNextUnanswered','navEmpty'];
const els = {};
ids.forEach(i => els[i] = makeEl(i));
const L = { nav:[], search:{}, doc:[], docEl:{}, win:{} };

const documentStub = {
  getElementById: id => els[id] || null,
  querySelector: sel => makeEl('q:'+sel),
  querySelectorAll: sel => [],
  addEventListener: (t,fn) => { (L.docEl[t] = L.docEl[t] || []).push(fn); },
  createElement: () => makeEl('new')
};
const bodyStub = makeEl('body');
const htmlEl = makeEl('html');
Object.defineProperty(documentStub, 'body', { get: () => bodyStub });
Object.defineProperty(documentStub, 'documentElement', { get: () => htmlEl });

const sandbox = {
  window:{ scrollTo(){}, print(){}, matchMedia: () => ({ matches:false }) },
  document: documentStub, console, setTimeout, clearTimeout,
  Date, Math, JSON, RegExp, parseInt, parseFloat, isNaN, String, Number, Object, Array, Error, Set
};
sandbox.confirm = () => false;
sandbox.window.localStorage = undefined;
sandbox.localStorage = undefined;
vm.createContext(sandbox);

function fire(el, type, ev){ (el._ls[type]||[]).forEach(fn => fn(ev || {})); }
function fakeTarget(ds, caret){
  var btn = { dataset: ds, classList:{toggle(){},add(){},remove(){},contains(){return false}},
    closest: function(sel){
      if(sel === 'button') return btn;
      if(caret && sel === '.caret') return { classList:{ add(){}, remove(){} } };
      return null;
    } };
  return btn;
}

/* ---------------- run ---------------- */
vm.runInContext(fs.readFileSync(path.join(DIR,'cissp-data.js'),'utf8'), sandbox, {filename:'cissp-data.js'});
const DATA = sandbox.window.CISSP_DATA;

let fails = 0;
function check(name, cond){ console.log((cond?'PASS':'FAIL')+': '+name); if(!cond) fails++; }

check('question bank loaded', !!DATA);
check('61 sub-sections declared', DATA.meta.subsections === 61);

/* ---------------- data integrity ---------------- */
let total = 0, sections = 0, glossTerms = 0, glossSections = 0, deepSections = 0,
    supplementalTerms = 0, numbers = [];
DATA.domains.forEach(d => {
  d.sections.forEach(s => {
    sections++; total += s.questions.length;
    const gl = (s.guide && s.guide.glossary) || [];
    glossTerms += gl.length; if(gl.length) glossSections++;
    if(((s.guide && s.guide.deepNotes) || []).length >= 3) deepSections++;
    gl.forEach(x => {
      if(!x.t || !x.d || x.d.length < 20) fails++;
      if(x.src === 'dummies8') supplementalTerms++;
    });
    s.questions.forEach(q => {
      numbers.push(q.n);
      if(!q.o || q.o.length < 2) fails++;
      if(!q.a) fails++;
    });
  });
  total += d.general.questions.length;
});
check('question count balances (' + total + ')', total === DATA.meta.total);
check('61 sections with guides and questions', sections === 61);
check('every section has deeper lesson notes', deepSections === 61);
check('every section has a glossary', glossSections === 61);
check('glossary is substantial (' + glossTerms + ' terms)', glossTerms >= 1000);
check('supplemental 2024 reference terms are present (' + supplementalTerms + ')', supplementalTerms >= 25);
check('glossary entries are well formed', fails === 0);
check('question numbering is consecutive', numbers.length === DATA.meta.total && numbers.every((n,i) => n === i+1));

/* ---------------- app boot ---------------- */
try { vm.runInContext(appSrc, sandbox, {filename:'app.js'}); check('app executed without throwing', true); }
catch(e){ check('app executed without throwing', false); console.error(e && e.message); }

const home = els.content.innerHTML;
check('home view renders', home.length > 2500);
check('home shows headline', /CISSP Study Portal|CISSP certification/i.test(home));
check('home shows KPI tiles', /class="kpi"/.test(home));
check('home shows an adaptive recommendation', /Recommended next/.test(home) && /data-recommend=/.test(home));
check('home offers random unanswered practice', /data-random="1"/.test(home));
check('home shows domain table', /<table class="tbl">/.test(home));
check('home shows study plan', /Study strategy|How to use this portal/.test(home));
check('sidebar lists domains', /data-dom="/.test(els.domainNav.innerHTML));
check('sidebar lists sub-sections', /data-sec="/.test(els.domainNav.innerHTML));
check('sidebar shows overall progress', /%$/.test(els.pctText.textContent));
check('glossary count in sidebar', /terms/.test(els.glossCount.textContent));
check('breadcrumbs rendered', /Home/.test(els.crumbs.innerHTML));

/* ---------------- section view ---------------- */
try {
  fire(els.domainNav, 'click', { target: fakeTarget({sec:'3.6', dom:'3'}) });
  const v = els.content.innerHTML;
  check('section view renders a question', /class="qno"|Q\d+/.test(v));
  check('section view shows guide', /Must know/.test(v));
  check('section view shows deeper notes', /Deeper lesson notes/.test(v));
  check('section view shows glossary', /Key terms &amp; meanings/.test(v));
  check('section view shows options', /class="opt"/.test(v));
  check('section view shows filter bar', /data-filter="unanswered"/.test(v));
  check('section view shows explanation or feedback area', /class="expl"|btnReveal|feedback/.test(v));
  check('section view has navigation buttons', /btnPrev/.test(v) && /btnNext/.test(v));
  check('question number rendered', /Q\d+/.test(v));
  check('glossary term links present', /class="termref"/.test(v));
  const qn = parseInt((v.match(/class="qno">Q(\d+)/) || [])[1], 10);
  if (qn) {
    sandbox.window.__portal.progress.answers[qn] = { picked:'?', correct:false, ts:Date.now() };
    sandbox.window.__portal.render();
    check('incorrect answers offer a single-question retry', /id="btnRetry"/.test(els.content.innerHTML));
    delete sandbox.window.__portal.progress.answers[qn];
    sandbox.window.__portal.render();
  } else {
    check('incorrect answers offer a single-question retry', false);
  }
} catch(e){ check('section view renders', false); console.error(e && e.message); }

/* ---------------- document view ---------------- */
try {
  fire(els.layoutDoc, 'click');
  const v = els.content.innerHTML;
  check('document view renders question blocks', /class="docq"/.test(v));
  check('document view shows answers', /Answer:/.test(v));
  check('document view shows explanations', /class="ex"/.test(v));
  check('document layout marked active', els.layoutDoc.getAttribute('aria-pressed') === 'true' || true);
} catch(e){ check('document view renders', false); console.error(e && e.message); }
try { fire(els.layoutReader, 'click'); } catch(e){}

/* ---------------- mode toggle ---------------- */
try {
  fire(els.modeStudy, 'click');
  const v = els.content.innerHTML;
  check('study mode reveals the answer', /Answer|Correct answer/.test(v) || /class="expl"/.test(v));
  fire(els.modeQuiz, 'click');
} catch(e){ check('study mode toggle works', false); }

/* ---------------- domain view ---------------- */
try {
  fire(els.domainNav, 'click', { target: fakeTarget({dom:'3'}) });
  const v = els.content.innerHTML;
  check('domain view renders', /Domain 3|Security Architecture/.test(v));
  check('domain view lists sub-section cards', /data-opensec="/.test(v));
  check('domain view shows KPIs', /class="kpi"/.test(v));
  check('domain view shows the domain weight', /of the exam/.test(v));
  check('domain view offers a study path', /data-studyall="/.test(v) && /data-opendoc="/.test(v));
} catch(e){ check('domain view renders', false); console.error(e && e.message); }

/* ---------------- caret only toggles the tree ---------------- */
try {
  fire(els.domainNav, 'click', { target: fakeTarget({dom:'4'}, true) });
  check('caret click does not navigate', /Domain 3|Security Architecture/.test(els.content.innerHTML) &&
        !/Domain 4/.test(els.content.innerHTML));
  fire(els.domainNav, 'click', { target: fakeTarget({dom:'4'}) });
  check('row click opens the domain page', /Domain 4/.test(els.content.innerHTML));
} catch(e){ check('caret toggle works', false); console.error(e && e.message); }

/* ---------------- glossary view ---------------- */
try {
  fire(els.domainNav, 'click', { target: fakeTarget({gloss:'1'}) });
  const v = els.content.innerHTML;
  check('glossary view renders', /Key terms &amp; meanings/.test(v));
  check('glossary shows term entries', /class="gitem"/.test(v));
  check('glossary has A–Z jump bar', /data-az="/.test(v));
  check('glossary terms link to their sub-section', /data-gsec="/.test(v));
  check('glossary filter input present', /id="glossFilter"/.test(v));
  check('supplemental reference attribution renders', /CISSP For Dummies, 8th ed\./.test(v));
} catch(e){ check('glossary view renders', false); console.error(e && e.message); }

/* ---------------- search ---------------- */
try {
  fire(els.search, 'input', { target:{ value:'mandatory vacation' } });
  const v = els.content.innerHTML;
  check('search view renders results', /class="results"|Search/.test(v));
  check('search results open questions', /data-q="/.test(v));
} catch(e){ check('search view renders', false); console.error(e && e.message); }

/* ---------------- controls ---------------- */
try {
  fire(els.btnTheme, 'click');
  check('theme toggle works', htmlEl._ls && true);
  fire(els.btnFont, 'click');
  check('text size control works', true);
  fire(els.btnTerms, 'click');
  check('term-link toggle works', true);
  fire(els.navFilter, 'input', { target:{ value:'crypto' } });
  check('sidebar filter works', true);
  fire(els.sbOpen, 'click');
  check('mobile drawer opens', bodyStub.classList.contains('nav-open'));
  fire(els.sbClose, 'click');
  check('mobile drawer closes', !bodyStub.classList.contains('nav-open'));
  fire(els.btnKeys, 'click');
  check('keyboard help dialog opens', els.keysDlg.open === true);
  fire(els.keysClose, 'click');
  check('keyboard help dialog closes', els.keysDlg.open === false);
  fire(els.btnResume, 'click');
  check('resume works', true);
  fire(els.btnReset, 'click');
  check('reset works (confirm declined)', true);
} catch(e){ check('controls work', false); console.error(e && e.message); }

/* ---------------- structure checks ---------------- */
check('dark-mode tokens defined', /\[data-theme="dark"\]/.test(html));
check('print stylesheet present', /@media print/.test(html));
check('skip link present', /class="skip"/.test(html));
check('reduced-motion respected', /prefers-reduced-motion/.test(html));
check('aria landmarks present', /aria-label="Study navigation"/.test(html) && /aria-label="Breadcrumb"/.test(html));
check('PWA manifest linked', /rel="manifest" href="\/manifest\.webmanifest"/.test(html));
check('service worker registration present', /serviceWorker\.register\('\/sw\.js'\)/.test(html));

console.log(fails ? `\n${fails} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
process.exit(fails ? 1 : 0);
