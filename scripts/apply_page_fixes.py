from pathlib import Path

root = Path(__file__).resolve().parents[1]

def one(text, old, new, label):
    if old not in text:
        raise RuntimeError(f"Missing {label}")
    return text.replace(old, new, 1)

# Homepage
p = root / "index.html"
t = p.read_text()
t = t.replace('display:flex;justify-content:space-between;flex-wrap:gap;gap:14px;flex-wrap:wrap', 'display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap')
t = t.replace('ai:{t:"AI-Embedded Marketing",d:"The teams winning right now have AI inside their processes. Let\'s get yours there — practically, not hype-first.",u:"/solutions/ai-marketing"}', 'ai:{t:"AI-Embedded Marketing",d:"The teams winning right now have AI inside their processes. Let\'s get yours there — practically, not hype-first.",u:"/#scorecard",c:"Start a conversation →"}')
t = t.replace('href="${R.u}">Explore ${R.t} →</a>', 'href="${R.u}">${R.c||(`Explore ${R.t} →`)}</a>')
p.write_text(t)

# AEO clickable tabs
p = root / "solutions/seo-aeo-visibility/index.html"
t = p.read_text()
t = one(t, '<span class="chat-tab on">ChatGPT</span><span class="chat-tab">Gemini</span><span class="chat-tab">Claude</span><span class="chat-tab">Perplexity</span>', '<button type="button" class="chat-tab on" aria-selected="true">ChatGPT</button><button type="button" class="chat-tab" aria-selected="false">Gemini</button><button type="button" class="chat-tab" aria-selected="false">Claude</button><button type="button" class="chat-tab" aria-selected="false">Perplexity</button>', 'AEO tabs')
t = t.replace('.chat-tab{font-size:12px;', '.chat-tab{appearance:none;border:0;background:transparent;cursor:pointer;font-size:12px;', 1)
old = '''const qEl=document.getElementById("q"),aEl=document.getElementById("a"),arow=document.getElementById("arow"),tabs=document.querySelectorAll(".chat-tab");
let sc=0;
function playScene(){
 const s=SCENES[sc];
 tabs.forEach((t,i)=>t.classList.toggle("on",i===s.tab));
 qEl.innerHTML='<span class="caret"></span>';aEl.innerHTML="";arow.style.opacity=0;
 let i=0;
 (function tq(){i++;qEl.innerHTML=s.q.slice(0,i)+'<span class="caret"></span>';
  if(i<s.q.length)setTimeout(tq,38);
  else{qEl.innerHTML=s.q;setTimeout(()=>{arow.style.opacity=1;let j=0;
   (function ta(){j+=3;aEl.innerHTML=s.a.slice(0,j);
    if(j<s.a.length)setTimeout(ta,18);
    else{aEl.innerHTML=s.a;setTimeout(()=>{sc=(sc+1)%SCENES.length;playScene()},3400)}})();},500)}})();
}
playScene();'''
new = '''const qEl=document.getElementById("q"),aEl=document.getElementById("a"),arow=document.getElementById("arow"),tabs=document.querySelectorAll(".chat-tab");
let sc=0,sceneRun=0;
function renderScene(index,animate=true){
 const run=++sceneRun,s=SCENES[index];
 tabs.forEach((t,i)=>{const active=i===s.tab;t.classList.toggle("on",active);t.setAttribute("aria-selected",String(active));});
 qEl.innerHTML="";aEl.innerHTML="";arow.style.opacity=animate?0:1;
 if(!animate){qEl.textContent=s.q;aEl.innerHTML=s.a;return;}
 let i=0;
 (function tq(){if(run!==sceneRun)return;i++;qEl.innerHTML=s.q.slice(0,i)+'<span class="caret"></span>';
  if(i<s.q.length)setTimeout(tq,38);
  else{qEl.textContent=s.q;setTimeout(()=>{if(run!==sceneRun)return;arow.style.opacity=1;let j=0;
   (function ta(){if(run!==sceneRun)return;j+=3;aEl.innerHTML=s.a.slice(0,j);
    if(j<s.a.length)setTimeout(ta,18);
    else{aEl.innerHTML=s.a;setTimeout(()=>{if(run!==sceneRun||document.hidden)return;sc=(sc+1)%SCENES.length;renderScene(sc,true)},3400)}})();},500)}})();
}
tabs.forEach((tab,index)=>tab.addEventListener("click",()=>{sc=index;renderScene(sc,window.siteMotionOK);}));
renderScene(sc,window.siteMotionOK);'''
t = one(t, old, new, 'AEO tab script')
t = t.replace('new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){loopScenes();o.disconnect()}},{threshold:.4}).observe(document.querySelector(".ai-stage"));', 'new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){if(window.siteMotionOK)loopScenes();else{s1q.textContent="best b2b digital marketing partner uk?";s1rows.classList.add("show");}o.disconnect()}},{threshold:.4}).observe(document.querySelector(".ai-stage"));')
t = t.replace('new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){playChecks();o.disconnect()}},{threshold:.3}).observe(document.getElementById("checks"));', 'new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){if(window.siteMotionOK)playChecks();else checks.forEach(c=>c.classList.add("on"));o.disconnect()}},{threshold:.3}).observe(document.getElementById("checks"));')
p.write_text(t)

# Success Stories chart accessibility and motion
p = root / "success-stories/index.html"
t = p.read_text()
t = t.replace('<svg class="linechart" viewBox="0 0 520 210" xmlns="http://www.w3.org/2000/svg">', '<svg class="linechart" viewBox="0 0 520 210" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="citation-chart-title citation-chart-desc"><title id="citation-chart-title">Owned domain citation rate compared with competitors</title><desc id="citation-chart-desc">The client rises to 8.1 percent, the highest rate in its category, while two competitors decline over the same period.</desc>', 1)
t = t.replace('<svg class="linechart" viewBox="0 0 900 240" xmlns="http://www.w3.org/2000/svg">', '<svg class="linechart" viewBox="0 0 900 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="weekly-chart-title weekly-chart-desc"><title id="weekly-chart-title">Weekly prompt visibility rate</title><desc id="weekly-chart-desc">Visibility rises from 3 percent in week one to a peak of 41.7 percent in week six, ending at 39 percent in week seven.</desc>', 1)
needle = '<text class="axlab" x="40" y="226" text-anchor="middle">week 1</text><text class="axlab" x="173" y="226" text-anchor="middle">week 2</text><text class="axlab" x="306" y="226" text-anchor="middle">week 3</text><text class="axlab" x="439" y="226" text-anchor="middle">week 4</text><text class="axlab" x="572" y="226" text-anchor="middle">week 5</text><text class="axlab" x="705" y="226" text-anchor="middle">week 6</text><text class="axlab" x="838" y="226" text-anchor="middle">week 7</text>\n        </svg>'
t = one(t, needle, needle + '\n        <details class="chart-data"><summary>View the weekly values as text</summary><p>Week 1: 3%. Week 2: 6%. Week 3: 9%. Week 4: 32%. Week 5: 36%. Week 6: 41.7%. Week 7: 39%.</p></details>', 'chart data')
t = t.replace('function playG(){gaio.classList.remove("show");', 'function playG(){if(document.hidden){setTimeout(playG,1000);return;}gaio.classList.remove("show");', 1)
t = t.replace('function pfLoop(){\n pf.classList.remove("done");', 'function pfLoop(){\n if(document.hidden){setTimeout(pfLoop,1000);return;}\n pf.classList.remove("done");', 1)
t = t.replace('function qualLoop(){\n qual.classList.remove("show");', 'function qualLoop(){\n if(document.hidden){setTimeout(qualLoop,1000);return;}\n qual.classList.remove("show");', 1)
t = t.replace('new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){playG();o.disconnect()}},{threshold:.35}).observe(document.querySelector(".gmock"));', 'new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){if(window.siteMotionOK)playG();else{gq.textContent=GQ;gaio.classList.add("show");gside.classList.add("show");}o.disconnect()}},{threshold:.35}).observe(document.querySelector(".gmock"));')
t = t.replace('new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){pf.style.position="relative";pfLoop();o.disconnect()}},{threshold:.35}).observe(pf);', 'new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){pf.style.position="relative";if(window.siteMotionOK)pfLoop();else{q(".pf-prods").style.display="grid";pf.classList.add("done");}o.disconnect()}},{threshold:.35}).observe(pf);')
t = t.replace('new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){qualLoop();o.disconnect()}},{threshold:.35}).observe(qual);', 'new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){if(window.siteMotionOK)qualLoop();else qual.classList.add("show");o.disconnect()}},{threshold:.35}).observe(qual);')
p.write_text(t)

# CRO motion
p = root / "solutions/website-optimisation-cro/index.html"
t = p.read_text()
t = t.replace('function qualLoop(){\n qual.classList.remove("show");', 'function qualLoop(){\n if(document.hidden){setTimeout(qualLoop,1000);return;}\n qual.classList.remove("show");', 1)
t = t.replace('new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){qualLoop();o.disconnect()}},{threshold:.35}).observe(qual);', 'new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){if(window.siteMotionOK)qualLoop();else qual.classList.add("show");o.disconnect()}},{threshold:.35}).observe(qual);')
p.write_text(t)

# Paid page motion
p = root / "solutions/paid-campaigns/index.html"
t = p.read_text()
t = t.replace('function typeQuery(){const q=QUERIES[qi];', 'function typeQuery(){if(document.hidden){setTimeout(typeQuery,1000);return;}const q=QUERIES[qi];', 1)
t = t.replace('typeQuery();\n\n// Funnels animate on view', 'if(window.siteMotionOK)typeQuery();else qEl.textContent=QUERIES[0];\n\n// Funnels animate on view', 1)
p.write_text(t)

print('Page-specific fixes applied')
