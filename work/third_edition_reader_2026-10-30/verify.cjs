const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=String.raw`C:\Work\JobsBody\outputs\Third_Edition_Reader_2026-10-30`;
const html=fs.readFileSync(path.join(root,'index.html'),'utf8'),script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script);
const data=JSON.parse(fs.readFileSync(path.join(root,'reader-data.json'),'utf8'));
assert.equal(data.blocks.length,5);
for(const voice of Object.values(data.voices)){
 assert.equal(voice.clips.length,5);
 for(const clip of voice.clips){assert.ok(fs.statSync(path.join(root,clip.src)).size>1000);assert.ok(clip.duration>1);}
 assert.ok(fs.existsSync(path.join(root,voice.download)));
}
const els=new Map();
class Element{
 constructor(){this.children=[];this.events={};this.value='1';this.checked=true;this.paused=true;this.currentTime=0;this.duration=100;this.classList={toggle(){}};}
 append(...x){this.children.push(...x);}
 setAttribute(){}
 addEventListener(type,fn,opts){(this.events[type]??=[]).push({fn,once:opts?.once});}
 fire(type){if(type==='ended')this.paused=true;for(const e of [...(this.events[type]??[])])e.fn();this.events[type]=(this.events[type]??[]).filter(e=>!e.once);}
 pause(){this.paused=true;this.fire('pause');}
 async play(){this.paused=false;this.fire('play');}
 load(){}
}
function el(id){if(!els.has(id))els.set(id,new Element());return els.get(id);}
const state=new Map(),context=vm.createContext({document:{getElementById:el,createElement(){return new Element();},querySelectorAll(){return[];},documentElement:{style:{setProperty(){}}}},localStorage:{getItem(k){return state.get(k)||null;},setItem(k,v){state.set(k,v);}}});
vm.runInContext(script,context);
assert.equal(el('author').children.length,3);assert.equal(el('comment').children.length,1);assert.equal(el('originals').children.length,2);
vm.runInContext('load(2,true)',context);assert.ok(el('audio').src.endsWith('dmitry_p2.mp3'));
el('voice').value='svetlana';el('voice').onchange();assert.ok(el('audio').src.endsWith('svetlana_p2.mp3'));
el('audio').fire('ended');assert.ok(el('audio').src.endsWith('svetlana_p3.mp3'));
el('withComment').checked=false;el('audio').fire('ended');assert.ok(el('status').textContent.startsWith('Фрагмент завершён'));
el('play').onclick();assert.ok(el('audio').src.endsWith('svetlana_heading.mp3'));
el('withComment').checked=true;vm.runInContext('load(3,true)',context);el('audio').fire('ended');assert.ok(el('audio').src.endsWith('svetlana_comment.mp3'));
assert.ok(!/https?:\/\//.test(script),'Reader must not call network');
console.log('PASS: offline data and assets; three full paragraphs; both voices; paragraph start; next; optional commentary; restart. No browser or UI automation used.');
fs.writeFileSync(path.join(__dirname,'reader_checks.json'),JSON.stringify({passed:true,browser_automated:false,checks:['offline assets','three complete paragraphs','voice switch preserves paragraph','next paragraph','optional commentary','restart'],human_listened:false},null,2));
