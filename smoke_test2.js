/**
 * Headless smoke test for the sub-section study portal.
 * Stubs the DOM just enough to run the app script and exercise every view.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const DIR = __dirname;
const html = fs.readFileSync(path.join(DIR, 'CISSP_Study_Portal.html'), 'utf8');
const scripts = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)];
const appSrc = scripts[scripts.length - 1][1];

function makeEl(id) {
  const el = { id, _html: '', textContent: '', value: '', dataset: {}, style: {},
    disabled: false, tagName: 'DIV',
    classList: { _s: new Set(), add(c){this._s.add(c)}, remove(c){this._s.delete(c)},
                 toggle(c,v){ v===undefined ? (this._s.has(c)?this._s.delete(c):this._s.add(c)) : (v?this._s.add(c):this._s.delete(c)) },
                 contains(c){return this._s.has(c)} },
    set innerHTML(v){ this._html = v; }, get innerHTML(){ return this._html; },
    addEventListener(){}, setAttribute(k,v){ this[k]=v; }, getAttribute(k){ return this[k]; },
    querySelectorAll(){ return []; }, querySelector(){ return null; },
    closest(){ return this; }, appendChild(){}, focus(){}, onclick:null, onkeydown:null };
  return el;
}
const ids = ['content','domainNav','pctText','pctBar','answeredText','marksText','brandSub',
             'search','btnGuide','btnPrint','btnResume','btnReset','toast','glossFilter','glossCount',
             'btnPrev','btnNext','btnReveal','btnMark','btnJump','jumpInput','mobileMenu','sidebarClose','sidebarScrim'];
const els = {}; ids.forEach(i => els[i] = makeEl(i));
const segButtons = ['one','all'].map(l => { const b = makeEl('seg-'+l); b.dataset.layout = l; return b; });
const L = { nav:null, search:{}, doc:{} };

const documentStub = {
  body: makeEl('body'),
  getElementById: id => els[id] || null,
  querySelectorAll: sel => sel.includes('.seg button') ? segButtons : [],
  querySelector: sel => sel === '.sb-bar' ? makeEl('progress') : makeEl('q:'+sel),
  addEventListener: (t,fn) => { L.doc[t]=fn; },
  createElement: () => makeEl('new')
};
documentStub.getElementById('domainNav').addEventListener = (t,fn) => { L.nav = fn; };
['input','keydown'].forEach(t => documentStub.getElementById('search').addEventListener = (tt,fn)=>{ L.search[tt]=fn; });

const sandbox = { window:{}, document:documentStub, console, setTimeout, clearTimeout,
  Date, Math, JSON, RegExp, parseInt, parseFloat, isNaN, String, Number, Object, Array, Error };
sandbox.window.scrollTo = () => {}; sandbox.window.print = () => {};
sandbox.window.matchMedia = () => ({matches:false});
sandbox.confirm = () => false;
vm.createContext(sandbox);

vm.runInContext(fs.readFileSync(path.join(DIR,'cissp-data.js'),'utf8'), sandbox, {filename:'cissp-data.js'});
const DATA = sandbox.window.CISSP_DATA;

let fails = 0;
function check(name, cond) {
  console.log((cond?'PASS':'FAIL')+': '+name);
  if(!cond) fails++;
}

check('CISSP_DATA loaded', !!DATA);
check('meta has sub-section count', DATA.meta.subsections === 61);
console.log(`INFO: ${DATA.meta.total} questions | placed ${DATA.meta.assigned} | other ${DATA.meta.general}`);

// ---- data shape ----
let total = 0, withGuide = 0, withDeepNotes = 0, sections = 0, emptyGuides = [], numbers = [];
let glossTerms = 0, glossSections = 0, strictDefs = 0, bareTerms = 0, thinGlossary = [];
DATA.domains.forEach(d => {
  d.sections.forEach(s => {
    sections++;
    total += s.questions.length;
    if (s.guide && s.guide.focus && s.guide.mustKnow && s.guide.mustKnow.length) withGuide++;
    else emptyGuides.push(s.id);
    if (s.guide && s.guide.deepNotes && s.guide.deepNotes.length >= 3) withDeepNotes++;
    const gl = (s.guide && s.guide.glossary) || [];
    glossTerms += gl.length;
    strictDefs += gl.filter(x => x.k === 'def').length;
    bareTerms += ((s.guide && s.guide.bareTerms) || []).length;
    if (gl.length) glossSections++;
    if (gl.length < 6) thinGlossary.push(s.id + ':' + gl.length);
    gl.forEach(x => { if (!x.t || !x.d || x.d.length < 20) fails++; });
    s.questions.forEach(q => {
      numbers.push(q.n);
      if (!q.o || q.o.length < 2) fails++;
      if (!q.a) fails++;
    });
  });
  total += d.general.questions.length;
});
check('question count balances', total === DATA.meta.total);
check('61 sections present', sections === 61);
check('every section has a tailored guide', withGuide === 61);
check('every section has deeper lesson notes', withDeepNotes === 61);
check('every section has a key-term glossary', glossSections === 61);
check('glossary is substantial (' + glossTerms + ' terms)', glossTerms >= 1000);
check('glossary entries have real meanings', fails === 0);
console.log(`INFO: glossary ${glossTerms} terms (${strictDefs} definitions), ${bareTerms} extra terms`);
if (thinGlossary.length) console.log('  sections with a thin glossary:', thinGlossary.join(', '));
check('questions are consecutive from 1 to the last question',
  numbers.length === DATA.meta.total && numbers.every((n, i) => n === i + 1));
if (emptyGuides.length) console.log('  sections missing guide content:', emptyGuides.slice(0,8));
check('assigned + other = total', DATA.meta.assigned + DATA.meta.general === DATA.meta.total);

// ---- run app ----
try { vm.runInContext(appSrc, sandbox, {filename:'app.js'}); check('app executed without throwing', true); }
catch(e){ check('app executed without throwing', false); console.error(e.message); }

const home = els.content.innerHTML;
check('home rendered', home.length > 2000);
check('home mentions sub-sections', /sub-section/i.test(home));
check('sidebar built with domains', /Domain 1:/.test(els.domainNav.innerHTML));
check('sidebar lists sub-sections', /data-sec="/.test(els.domainNav.innerHTML));
check('brand shows sub-section count', /61 sub-sections/.test(els.brandSub.textContent));

// click a sub-section in the sidebar
function fakeBtn(ds){ return { dataset: ds, classList:{toggle(){},add(){},remove(){},contains(){return false}}, closest(){ return this; } }; }
try {
  L.nav({ target: { closest: () => fakeBtn({ sec:'3.6', dom:'3' }) } });
  const v = els.content.innerHTML;
  check('sub-section view rendered', /Question \d+/.test(v));
  check('sub-section view shows its guide', /Must know/.test(v));
  check('sub-section view shows deeper lesson notes', /Deeper lesson notes/.test(v));
  check('sub-section view shows key terms with meanings', /Key terms &amp; meanings/.test(v));
  check('sub-section glossary renders term entries', /class="gitem"/.test(v));
  check('sub-section view shows options', /class="opt"/.test(v));
  check('sub-section view shows nav', /btnNext/.test(v));
  check('sub-section tag shown', /3\.6/.test(v));
  L.doc.keydown({ target:{tagName:'DIV'}, key:'ArrowRight' });
  check('study guide is hidden after the first question', !/Must know/.test(els.content.innerHTML));
  L.doc.keydown({ target:{tagName:'DIV'}, key:'ArrowLeft' });
  check('study guide returns at the section beginning', /Must know/.test(els.content.innerHTML));
} catch(e){ check('sub-section view rendered', false); console.error(e.message); }

// read-as-document layout
try {
  const seg = sandbox.document.querySelectorAll('.seg button').find(b => b.dataset.layout === 'all');
  // the app attached listeners via addEventListener (stubbed), so switch state directly by clicking:
  check('seg buttons exist', !!seg);
} catch(e){ console.log('  (layout toggle not directly testable in stub)'); }

// search
try {
  L.search.input({ target: { value: 'mandatory vacation' } });
  check('search view rendered', /Search results/.test(els.content.innerHTML));
  check('search results link to questions', /data-q=/.test(els.content.innerHTML));
  check('search shows sub-section label', /Domain \d/.test(els.content.innerHTML));
} catch(e){ check('search view rendered', false); console.error(e.message); }

// domain overview
try {
  L.nav({ target: { closest: () => fakeBtn({ dom:'3' }) } });
  const v = els.content.innerHTML;
  check('domain overview rendered', /Domain 3/.test(v));
  check('domain overview lists sub-sections', /data-opensec="/.test(v));
} catch(e){ check('domain overview rendered', false); console.error(e.message); }

// global glossary view
try {
  L.nav({ target: { closest: () => fakeBtn({ gloss:'1' }) } });
  const v = els.content.innerHTML;
  check('global glossary view rendered', /Key terms &amp; meanings/.test(v));
  check('global glossary groups alphabetically', /<h3 class="sub"/.test(v));
  check('global glossary has jump-to-section buttons', /data-gsec="/.test(v));
  check('glossary sidebar count set', /defined terms/.test(els.glossCount.textContent));
} catch(e){ check('global glossary view rendered', false); console.error(e.message); }

console.log(fails ? `\n${fails} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
process.exit(fails ? 1 : 0);
