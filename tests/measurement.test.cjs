const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const code = fs.readFileSync(require('node:path').join(__dirname,'../assets/measurement.js'),'utf8');
function browser(pref, hostname='dratifanyschmidt.com.br') {
  const head=[], listeners={}, buttons={}, storage=new Map(pref ? [['tifany.analytics.v1',pref]] : []);
  const document={readyState:'complete',title:'Consulta',referrer:'https://example.com/?private=secret',cookie:'',
    head:{appendChild:n=>head.push(n)},body:{appendChild(){}},
    addEventListener:(name,cb)=>{(listeners[name] ||= []).push(cb)},
    createElement:tag=>({tag,style:{},setAttribute(){},querySelectorAll(){return ['rejected','accepted'].map(choice=>({dataset:{choice},addEventListener:(name,cb)=>buttons[choice]=cb}))}})};
  const window={};
  const context=vm.createContext({window,document,localStorage:{getItem:k=>storage.get(k),setItem:(k,v)=>storage.set(k,v)},location:{hostname,origin:'https://'+hostname,pathname:'/avaliacao-facial-balneario-camboriu/',href:'https://'+hostname+'/?patient=private'},URL,Date});
  vm.runInContext(code,context);
  const click=(href)=>{const link={href,classList:{contains:n=>n==='hero-cta'}}; const target={closest:selector=>selector==='a[href]'?link:null};(listeners.click||[]).forEach(fn=>fn({target}));};
  const events=()=>Array.from(window.dataLayer||[],x=>Array.from(x));
  return {head,buttons,window,events,click,context};
}
test('no Analytics request before a choice or after rejection',()=>{
  for(const pref of [null,'rejected']){const b=browser(pref);assert.equal(b.head.filter(n=>n.tag==='script').length,0);b.click('https://wa.me/5547997722437?text=private');assert.equal(b.events().length,0);}
});
test('acceptance loads one tag and one page view, excluding query and full referrer',()=>{
  const b=browser();b.buttons.accepted();b.buttons.accepted();
  assert.equal(b.head.filter(n=>n.tag==='script').length,1);
  assert.equal(b.events().filter(x=>x[1]==='page_view').length,1);
  assert.ok(!JSON.stringify(b.events()).includes('private'));
  assert.ok(!JSON.stringify(b.events()).includes('secret'));
});
test('one WhatsApp click event, no message data and no unrelated links',()=>{
  const b=browser('accepted');vm.runInContext(code,b.context);
  b.click('https://wa.me/5547997722437?text=clinical-secret');
  b.click('https://example.com/wa.me');b.click('https://wa.me/123');
  const events=b.events().filter(x=>x[1]==='whatsapp_click');assert.equal(events.length,1);
  assert.ok(!JSON.stringify(events).includes('clinical-secret'));
});
test('revocation stops tracking and acceptance can resume it',()=>{
  const b=browser('accepted');b.buttons.rejected();b.click('https://wa.me/5547997722437');
  assert.equal(b.events().filter(x=>x[1]==='whatsapp_click').length,0);
  b.buttons.accepted();b.click('https://wa.me/5547997722437');
  assert.equal(b.events().filter(x=>x[1]==='whatsapp_click').length,1);
  assert.equal(b.head.filter(n=>n.tag==='script').length,1);
  assert.equal(b.events().filter(x=>x[0]==='consent').at(-1)[2].analytics_storage,'granted');
});
test('local preview does not load the production Analytics tag',()=>{
  const b=browser('accepted','127.0.0.1');assert.equal(b.head.filter(n=>n.tag==='script').length,0);
});
