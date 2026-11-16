(function(){
  var $=function(id){return document.getElementById(id)};
  var pt=function(n,d){return n.toLocaleString('pt-BR',{minimumFractionDigits:d||0,maximumFractionDigits:d||0})};
  var brl=function(n){return 'R$ '+pt(n)};

  /* tema */
  var root=document.documentElement, btn=$('theme-btn'), ico=$('theme-ico'), txt=$('theme-txt');
  var SUN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  var MOON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
  function apply(t){ if(t==='dark'){root.setAttribute('data-theme','dark');ico.innerHTML=SUN;txt.textContent='Modo claro';} else {root.setAttribute('data-theme','light');ico.innerHTML=MOON;txt.textContent='Modo escuro';} }
  var saved=null; try{saved=localStorage.getItem('guia-marxismo-theme')}catch(e){}
  apply(saved==='dark'?'dark':'light');
  btn.addEventListener('click',function(){ var next=root.getAttribute('data-theme')==='dark'?'light':'dark'; apply(next); try{localStorage.setItem('guia-marxismo-theme',next)}catch(e){} });

  /* sumário */
  var det=$('toc-details'), mob=window.matchMedia('(max-width:900px)');
  if(mob.matches){ det.open=false; }
  var links=[].slice.call(document.querySelectorAll('nav.toc a'));
  var map={}; links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a; a.addEventListener('click',function(){ if(mob.matches) det.open=false; })});
  if('IntersectionObserver' in window){
    var heads=[].slice.call(document.querySelectorAll('main h2[id], main h3[data-toc]'));
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ links.forEach(function(l){l.classList.remove('active')}); var a=map[e.target.id]; if(a){a.classList.add('active');} } });
    },{rootMargin:'-80px 0px -70% 0px'});
    heads.forEach(function(h){io.observe(h)});
  }

  /* 1. valor de uso x troca */
  var EX={
    pao:{u:'Alimenta. O pão feito em casa existe só por isso: alguém tem fome.',t:'Na padaria, o pão só chega a quem paga. Se não vende até o fim do dia, a sobra pode ser descartada, mesmo havendo gente com fome.'},
    casa:{u:'Abriga, dá segurança e um lugar para viver.',t:'Um imóvel comprado para valorizar ou alugar pode ficar vazio à espera de comprador, enquanto há famílias sem moradia ou pagando aluguel que não cabe no orçamento.'},
    bolsa:{u:'Uma bolsa artesanal e uma bolsa de grife cumprem, em geral, a mesma função: carregar objetos. Para esse uso, o nome da marca não acrescenta nada.',t:'A de grife pode custar muitas vezes mais do que a artesanal. O preço extra vem da marca, e não de a bolsa carregar mais coisas. A seção 3 mostra como esse preço é construído.'},
    agua:{u:'A água é indispensável à vida. O diamante serve para pouca coisa essencial.',t:'O diamante vale muito mais do que a água. O valor de troca não mede a utilidade. Para Marx, ele mede o trabalho socialmente necessário (seção 2).'}
  };
  var wu=$('w-uso');
  function showEx(k){ $('wu-u').textContent=EX[k].u; $('wu-t').textContent=EX[k].t; [].forEach.call(wu.querySelectorAll('button'),function(b){b.setAttribute('aria-pressed',String(b.getAttribute('data-k')===k))}); }
  [].forEach.call(wu.querySelectorAll('button'),function(b){b.addEventListener('click',function(){showEx(b.getAttribute('data-k'))})});
  showEx('pao');


  /* 6. mais-valia */
  var wj=$('wm-j'), wn=$('wm-n'), HV=30;
  function mv(){
    var j=+wj.value, n=+wn.value; if(n>j){n=j; wn.value=n;}
    var val=HV*j, sal=HV*n, m=val-sal, t=Math.round((m/sal)*100);
    $('wm-jo').textContent=j+' h'; $('wm-no').textContent=n+' h';
    $('wm-bn').style.width=(n/14*100)+'%'; $('wm-bn').textContent=n+' h necessárias';
    $('wm-be').style.width=((j-n)/14*100)+'%'; $('wm-be').textContent=(j-n)>0?(j-n)+' h excedentes':'';
    $('wm-v').textContent=brl(val); $('wm-s').textContent=brl(sal); $('wm-m').textContent=brl(m); $('wm-t').textContent=t+'%';
    $('wm-x').textContent=m===0
      ? 'Toda a jornada paga o salário: não sobra excedente, e sem excedente não há capital.'
      : 'De cada '+brl(val)+' que o trabalhador cria por dia, ele recebe o equivalente a '+brl(sal)+'. Os outros '+brl(m)+' ficam com o capitalista. Taxa de mais-valia: '+t+'% (excedente dividido pelo trabalho necessário).';
  }
  wj.addEventListener('input',mv); wn.addEventListener('input',mv); mv();

  /* 7. acumulação */
  var wr=$('wa-r'), L=0.2, T=10;
  function series(share){ var a=[100]; for(var i=1;i<=T;i++){a.push(a[i-1]*(1+L*share));} return a; }
  function niceStep(max){ var s=[50,100,200,250,500,1000]; for(var i=0;i<s.length;i++){ if(max/s[i]<=5) return s[i]; } return 1000; }
  function acum(){
    var r=+wr.value/100, A=series(1), B=series(r);
    $('wa-o').textContent=Math.round(r*100)+'%';
    var W=620,H=290,ml=46,mr=70,mt=16,mb=34, max=A[T], step=niceStep(max), top=Math.ceil(max/step)*step;
    var x=function(i){return ml+(W-ml-mr)*i/T}, y=function(v){return H-mb-(H-mt-mb)*v/top};
    var s='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Capital das empresas A e B ao longo de 10 ciclos">';
    for(var v=0;v<=top;v+=step){ s+='<line x1="'+ml+'" x2="'+(W-mr)+'" y1="'+y(v)+'" y2="'+y(v)+'" style="stroke:var(--line);stroke-width:1"/><text x="'+(ml-8)+'" y="'+(y(v)+4)+'" text-anchor="end" class="m">'+v+'</text>'; }
    for(var i=0;i<=T;i+=2){ s+='<text x="'+x(i)+'" y="'+(H-12)+'" text-anchor="middle" class="m">'+i+'</text>'; }
    s+='<text x="'+((ml+W-mr)/2)+'" y="'+(H-0)+'" text-anchor="middle" class="m" style="font-size:11px">ciclos</text>';
    var pa=A.map(function(v,i){return x(i)+','+y(v)}).join(' '), pb=B.map(function(v,i){return x(i)+','+y(v)}).join(' ');
    s+='<polyline points="'+pb+'" style="fill:none;stroke:var(--c2);stroke-width:2.5"/><polyline points="'+pa+'" style="fill:none;stroke:var(--brand);stroke-width:2.5"/>';
    s+='<circle cx="'+x(T)+'" cy="'+y(A[T])+'" r="4" style="fill:var(--brand)"/><circle cx="'+x(T)+'" cy="'+y(B[T])+'" r="4" style="fill:var(--c2)"/>';
    s+='<text x="'+(x(T)+8)+'" y="'+(y(A[T])+4)+'" class="b hot">A</text><text x="'+(x(T)+8)+'" y="'+(y(B[T])+4)+'" class="b cool">B</text></svg>';
    $('wa-chart').innerHTML=s;
    $('wa-a').textContent=pt(A[T]); $('wa-b').textContent=pt(B[T]); $('wa-p').textContent=Math.round(B[T]/A[T]*100)+'%';
  }
  wr.addEventListener('input',acum); acum();

  /* 7b. exército industrial de reserva */
  var weO=$('we-o'), weP=$('we-p'), dots=$('we-dots');
  for(var d=0;d<100;d++){ dots.appendChild(document.createElement('i')); }
  function er(){
    var o=+weO.value, p=+weP.value, emp=Math.min(100,Math.round(100*o/p)), res=100-emp, it=dots.children;
    $('we-oo').textContent=pt(o,1)+'×'; $('we-po').textContent=pt(p,1)+'×';
    for(var i=0;i<100;i++){ it[i].className = i<emp ? '' : 'res'; }
    $('we-e').textContent=emp; $('we-r').textContent=res;
    $('we-v').textContent = res===0
      ? 'Sobram vagas: as empresas disputam trabalhadores, e quem trabalha tem força para pedir aumento. É o cenário em que o exército de reserva quase desaparece.'
      : res<15
        ? 'Há uma fila pequena de desempregados. Quem está empregado ainda negocia, mas já sente a pressão.'
        : 'Com '+res+'% de desempregados, cada vaga tem vários candidatos. O patrão pode pagar menos e exigir mais, e quem trabalha teme perder o lugar.';
  }
  weO.addEventListener('input',er); weP.addEventListener('input',er); er();

  /* 8. oligopólio */
  var SH=[[14,12,11,10,9,8,7,7,6,6,5,5],[26,21,17,14,12,10],[47,31,22],[69,31]], ws=$('wo-s');
  function oli(){
    var s=SH[+ws.value]; $('wo-o').textContent=ws.value;
    var h=s.reduce(function(a,v){return a+v*v},0), bar=$('wo-bar'); bar.innerHTML='';
    s.forEach(function(v){ var d=document.createElement('div'); d.className='s-brand'; d.style.width=v+'%'; d.textContent=v>=6?v+'%':''; bar.appendChild(d); });
    $('wo-n').textContent=s.length; $('wo-m').textContent=Math.max.apply(null,s)+'%'; $('wo-h').textContent=pt(h);
  }
  ws.addEventListener('input',oli); oli();

  /* 9. classes */
  var CL={
    burg:['Burguesia (média ou grande)','Vive do capital e do trabalho alheio. Sua posição é de apropriar mais-valia.'],
    pbe:['Pequena burguesia empregadora','Tem um negócio pequeno e contrata poucos funcionários, mas ainda trabalha nele. A concorrência dos grandes e a dívida a empurram para um lado ou para o outro: crescer ou cair.'],
    pba:['Pequena burguesia autônoma','Tem meios de produção pequenos e vive do próprio trabalho. É a posição mais pressionada pela concentração de capital e tende à proletarização.'],
    trab:['Classe trabalhadora assalariada','Vende a força de trabalho por salário. Um salário alto não muda essa posição: o que define a classe é a relação com os meios de produção.'],
    pc:['Trabalhador por conta própria sem capital','Sem meios de produção relevantes, vende o próprio trabalho por conta própria. É uma zona de fronteira: formalmente autônomo, na prática próximo do assalariado, como muitos motoristas de aplicativo.'],
    rent:['Rentista de pequena escala','Vive de aluguéis ou aplicações sem ter meios de produção relevantes. É uma posição intermediária: depende do tamanho do patrimônio.'],
    mix:['Posição intermediária','Sua combinação mistura critérios. Marx classificaria pela fonte principal da renda e pela relação com os meios de produção.']
  };
  function cls(){
    var a=$('wc-1').value, b=$('wc-2').value, c=$('wc-3').value, k;
    if(a==='gde'||b==='muitos') k='burg';
    else if(a==='peq'&&b==='poucos') k='pbe';
    else if(a==='peq'&&b==='nao'&&c==='proprio') k='pba';
    else if(a==='nao'&&b==='nao'&&c==='salario') k='trab';
    else if(a==='nao'&&b==='nao'&&c==='proprio') k='pc';
    else if(a==='nao'&&c==='lucro') k='rent';
    else k='mix';
    $('wc-r').innerHTML='<b>'+CL[k][0]+'.</b> '+CL[k][1];
  }
  ['wc-1','wc-2','wc-3'].forEach(function(i){$(i).addEventListener('change',cls)}); cls();

  /* 10. taxa de lucro */
  var wc=$('wl-c'), wm=$('wl-m');
  function lu(){
    var cv=+wc.value, mvr=+wm.value, r=mvr/(cv+1)*100, tot=cv+1, maxTot=7;
    $('wl-co').textContent=pt(cv,1); $('wl-mo').textContent=Math.round(mvr*100)+'%';
    $('wl-bc').style.width=(cv/maxTot*100)+'%'; $('wl-bc').textContent=cv>=1.5?'c':'';
    $('wl-bv').style.width=(1/maxTot*100)+'%'; $('wl-bv').textContent='v';
    $('wl-bm').textContent='m = '+pt(mvr,1)+' para v = 1';
    $('wl-r').textContent=pt(r,1)+'%';
    $('wl-x').textContent=cv<=1&&mvr===1
      ? 'Com c/v = 1 e exploração de 100%, a taxa de lucro é 50%. Aumente as máquinas por trabalhador (c/v) e veja a taxa cair.'
      : 'Para cada R$ 1 de salário há R$ '+pt(cv,1)+' em máquinas e matérias-primas, e a mais-valia é R$ '+pt(mvr,1)+'. A taxa de lucro é '+pt(mvr,1)+' ÷ '+pt(tot,1)+' = '+pt(r,1)+'%.';
  }
  wc.addEventListener('input',lu); wm.addEventListener('input',lu); lu();
})();
