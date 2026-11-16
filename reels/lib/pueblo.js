/* Generador del pueblo para los reels de Henderson.
   Estructura típica de pueblo ferroviario bonaerense (ilustrativa, no es el plano catastral):
   planta urbana en damero con plaza central, avenida estación → plaza, playa ferroviaria con
   galpones y silos, quintas alrededor y chacras con lotes, cortinas de árboles y molinos.
   Unidades ≈ metros. Eje x = este, eje y = sur. */
(function () {
  function rng(seed){ return function(){ seed|=0; seed=seed+0x6D2B79F5|0; var t=Math.imul(seed^seed>>>15,1|seed); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }

  function build() {
    var R = rng(1909);
    var B = 100, P = 120, NI = 6, NJ = 5, AVX = 70;
    var w = {
      B:B, P:P, AVX:AVX, RAIL:[-742,-754,-766],
      blocks:[], boxes:[], trees:[], cyl:[], patches:[], molinos:[], lamps:[], roads:[], cortinas:[],
      plaza:null, club:null, yard:null, pois:{}
    };
    function bx(i){ return i*P - B/2 + (i >= 1 ? 20 : 0); }      // la avenida (entre i=0 e i=1) es más ancha
    function addBox(x0,y0,x1,y1,h,kind,o){
      o = o || {};
      var cx = (x0+x1)/2, cy = (y0+y1)/2;
      var b = { x0:x0,y0:y0,x1:x1,y1:y1,h:h, kind:kind||'casa', d:Math.hypot(cx,cy), r:R(), win:o.win !== false && R() > 0.25, roof:o.roof||0 };
      w.boxes.push(b); return b;
    }
    function tree(x,y,r,kind){ w.trees.push({ x:x, y:y, r:r, d:Math.hypot(x,y), k:kind||0, s:R() }); }

    // ---------- planta urbana ----------
    var map = {};
    var CLUB = { '4,2':1,'5,2':1,'4,3':1,'5,3':1 };
    for (var i = -NI; i <= NI; i++) for (var j = -NJ; j <= NJ; j++) {
      var r = Math.sqrt(Math.pow(i/6.4,2) + Math.pow(j/5.4,2)) + (R()-.5)*0.22;
      var force = CLUB[i+','+j] || (i === 0 && j < 0) || (i === 1 && j < 0);
      if (r > 1.0 && !force) continue;
      var b = { i:i, j:j, x0:bx(i), x1:bx(i)+B, y0:j*P-B/2, y1:j*P+B/2, r:Math.max(0, Math.min(1.05, r)), type:'res' };
      if (i === 0 && j === 0) b.type = 'plaza';
      if (CLUB[i+','+j]) b.type = 'club';
      map[i+','+j] = b; w.blocks.push(b);
    }
    function has(i,j){ return !!map[i+','+j]; }

    function fillBlock(b){
      var occ = b.r < 0.35 ? 0.98 : b.r < 0.6 ? 0.9 : b.r < 0.82 ? 0.74 : 0.52;
      var dep = b.r < 0.5 ? 34 : 28, center = b.r < 0.38;
      var skip = b.skip || {};
      function side(x0,y0,x1,y1,horiz,which){
        if (skip[which]) return;
        var len = horiz ? x1-x0 : y1-y0, pos = 0;
        while (pos < len - 8) {
          var wd = center ? 11 + R()*9 : 14 + R()*14; if (pos + wd > len) wd = len - pos;
          if (R() < occ) {
            var dd = dep - R()*8, h = center ? (R() < 0.3 ? 16 + R()*20 : 9 + R()*6) : (b.r < 0.7 ? 7.5 + R()*5 : 6.5 + R()*3.5);
            var roof = (!center && R() < 0.45) ? 1 : 0;
            if (horiz) { var a0 = which === 'n' ? y0 : y1 - dd, a1 = which === 'n' ? y0 + dd : y1; addBox(x0+pos+0.8, a0+0.8, x0+pos+wd-0.8, a1-0.8, h, 'casa', { roof:roof }); }
            else { var c0 = which === 'w' ? x0 : x1 - dd, c1 = which === 'w' ? x0 + dd : x1; addBox(c0+0.8, y0+pos+0.8, c1-0.8, y0+pos+wd-0.8, h, 'casa', { roof:roof }); }
          }
          pos += wd + (center ? 0 : R()*4);
        }
      }
      side(b.x0, b.y0, b.x1, b.y0+dep, true, 'n');
      side(b.x0, b.y1-dep, b.x1, b.y1, true, 's');
      side(b.x0, b.y0+dep, b.x0+dep, b.y1-dep, false, 'w');
      side(b.x1-dep, b.y0+dep, b.x1, b.y1-dep, false, 'e');
      var nt = b.r < 0.35 ? (R() < 0.5 ? 1 : 0) : 1 + Math.floor(R()*3.5);
      for (var k = 0; k < nt; k++) tree(lerp(b.x0+dep+6, b.x1-dep-6, R()), lerp(b.y0+dep+6, b.y1-dep-6, R()), 6 + R()*6, 0);
    }
    function lerp(a,b,x){ return a + (b-a)*x; }

    // edificios singulares frente a la plaza
    var bn = map['0,-1'], bw = map['-1,0'], bs = map['0,1'], bne = map['1,-1'];
    if (bn) { bn.skip = { s:1 }; addBox(-17, bn.y1-74, 17, bn.y1-16, 24, 'iglesia', { win:false }); addBox(-8, bn.y1-18, 8, bn.y1-4, 64, 'torre', { win:false }); }
    if (bw) { bw.skip = { e:1 }; addBox(bw.x1-36, -42, bw.x1-4, 42, 17, 'muni'); addBox(bw.x1-24, -8, bw.x1-6, 8, 30, 'torre', { win:false }); }
    if (bs) { bs.skip = { n:1 }; addBox(bs.x0+10, bs.y0+4, bs.x1-10, bs.y0+30, 12, 'escuela'); }
    if (bne) { bne.skip = { s:1 }; addBox(bne.x0+2, bne.y1-32, bne.x0+34, bne.y1-2, 15, 'banco'); }
    var bh = map['-4,2'];
    if (bh) { bh.type = 'hosp'; addBox(bh.x0+15, bh.y0+25, bh.x1-15, bh.y1-25, 12, 'hospital'); for (var q = 0; q < 6; q++) tree(bh.x0 + 12 + q*15, bh.y1 - 10, 5.5, 0); }
    var bt = map['-3,-3'];
    if (bt) { bt.skip = { }; w.cyl.push({ x:(bt.x0+bt.x1)/2, y:(bt.y0+bt.y1)/2, r:9, z0:34, h:16, kind:'tanque' });
      var tx = (bt.x0+bt.x1)/2, ty = (bt.y0+bt.y1)/2;
      [[-6,-6],[6,-6],[6,6],[-6,6]].forEach(function(o){ addBox(tx+o[0]-1, ty+o[1]-1, tx+o[0]+1, ty+o[1]+1, 34, 'pata', { win:false }); });
      w.pois.tanque = { x:tx, y:ty, z:50 }; }

    w.blocks.forEach(function(b){ if (b.type === 'res') fillBlock(b); });

    // plaza
    var pz = map['0,0']; w.plaza = pz;
    for (var a = 0; a < 20; a++) { var an = a/20*Math.PI*2; tree(Math.cos(an)*42, Math.sin(an)*42, 6, 1); }
    for (var c = 0; c < 4; c++) tree((c<2?-1:1)*24, (c%2?-1:1)*24, 5, 1);
    addBox(-3, -3, 3, 3, 9, 'monumento', { win:false });
    w.pois.plaza = { x:0, y:0, z:10 };

    // club con cancha
    var cl = { x0:bx(4), x1:bx(5)+B, y0:2*P-B/2, y1:3*P+B/2 };
    w.club = cl; var ccx = (cl.x0+cl.x1)/2, ccy = (cl.y0+cl.y1)/2;
    cl.f = { x0:ccx-72, x1:ccx+72, y0:ccy-46, y1:ccy+46 };
    addBox(cl.x0+8, cl.y0+6, cl.x0+70, cl.y0+24, 9, 'club');
    [[cl.f.x0-8,cl.f.y0-8],[cl.f.x1+6,cl.f.y0-8],[cl.f.x0-8,cl.f.y1+6],[cl.f.x1+6,cl.f.y1+6]].forEach(function(o){ addBox(o[0], o[1], o[0]+2, o[1]+2, 26, 'torre-luz', { win:false }); });
    for (var e = 0; e < 14; e++) { tree(cl.x0 + 8 + e*16, cl.y1 - 6, 5, 0); }
    w.pois.cancha = { x:ccx, y:ccy, z:4 };

    // avenida: cantero central con árboles y luminarias
    var yS = -Infinity; w.blocks.forEach(function(b){ if (b.i === 0 || b.i === 1) yS = Math.max(yS, b.y1); });
    for (var y = -700; y < yS; y += 24) tree(AVX, y, 4.6, 2);
    for (var y2 = -690; y2 < yS; y2 += 48) w.lamps.push({ x:AVX, y:y2, d:Math.hypot(AVX,y2), k:1 });
    w.avenue = { x0:AVX-20, x1:AVX+20, y0:-726, y1:yS + 10 };

    // arbolado de veredas y luces de esquina
    var seen = {};
    w.blocks.forEach(function(b){
      if (b.type === 'plaza' || b.type === 'club') return;
      var pr = b.r < 0.38 ? 0.35 : 0.6;
      [[b.x0,b.y0,b.x1,b.y0,0,-1],[b.x0,b.y1,b.x1,b.y1,0,1],[b.x0,b.y0,b.x0,b.y1,-1,0],[b.x1,b.y0,b.x1,b.y1,1,0]].forEach(function(s){
        var len = Math.hypot(s[2]-s[0], s[3]-s[1]);
        for (var u = 9; u < len - 6; u += 21) if (R() < pr) {
          var f = u/len; tree(lerp(s[0],s[2],f) + s[4]*4.5, lerp(s[1],s[3],f) + s[5]*4.5, 4 + R()*2, 3);
        }
      });
      [[b.x0-10,b.y0-10],[b.x1+10,b.y0-10],[b.x0-10,b.y1+10],[b.x1+10,b.y1+10]].forEach(function(p){
        var key = Math.round(p[0]/5)+','+Math.round(p[1]/5); if (seen[key]) return; seen[key] = 1;
        w.lamps.push({ x:p[0], y:p[1], d:Math.hypot(p[0],p[1]), k:0, r:R() });
      });
    });

    // ---------- playa ferroviaria ----------
    w.yard = { x0:-420, x1:780, y0:-782, y1:-726 };
    w.platform = { x0:0, x1:180, y0:-737, y1:-729 };
    addBox(28, -727, 142, -705, 12, 'estacion', { roof:2 });
    addBox(220, -725, 400, -695, 16, 'galpon', { win:false, roof:1 });
    addBox(430, -725, 560, -702, 13, 'galpon', { win:false, roof:1 });
    for (var row = 0; row < 2; row++) for (var col = 0; col < 4; col++) w.cyl.push({ x:312 + col*31, y:-806 - row*31, r:14, z0:0, h:76, kind:'silo' });
    addBox(260, -838, 286, -790, 112, 'elevador', { win:false });
    addBox(452, -836, 660, -800, 15, 'galpon', { win:false, roof:1 });
    w.pois.estacion = { x:85, y:-716, z:14 };
    w.pois.silos = { x:360, y:-820, z:80 };

    // ---------- quintas ----------
    var QX0 = -1330, QX1 = 1470, QY0 = -1300, QY1 = 1200;
    var urb = { x0:-860, x1:900, y0:-700, y1:700 };
    w.blocks.forEach(function(b){ urb.x0 = Math.min(urb.x0, b.x0-30); urb.x1 = Math.max(urb.x1, b.x1+30); urb.y0 = Math.min(urb.y0, b.y0-30); urb.y1 = Math.max(urb.y1, b.y1+30); });
    w.urb = urb;
    var QS = 233;
    for (var gx = 0; gx < 12; gx++) for (var gy = 0; gy < 11; gy++) {
      var x0 = QX0 + gx*QS, y0 = QY0 + gy*(QY1-QY0)/11, x1 = x0 + QS, y1 = y0 + (QY1-QY0)/11;
      var cxq = (x0+x1)/2, cyq = (y0+y1)/2;
      if (x1 > urb.x0 && x0 < urb.x1 && y1 > urb.y0 && y0 < urb.y1) continue;
      if (y1 > -880 && y0 < -690 && x1 > -460 && x0 < 820) continue;
      if (Math.abs(cxq - AVX) < QS/2) { // la avenida sigue como camino: dejar la franja libre
        if (x0 < AVX && x1 > AVX) { var mid = AVX; addQuinta(x0, y0, mid-10, y1); addQuinta(mid+10, y0, x1, y1); continue; }
      }
      addQuinta(x0, y0, x1, y1);
    }
    function addQuinta(x0,y0,x1,y1){
      var p = { x0:x0+7, y0:y0+7, x1:x1-7, y1:y1-7, kind:'quinta', tone: R() < 0.5 ? 0 : 1, rows: R() < 0.45, sp:10, dir: R() < 0.5 };
      p.d = Math.hypot((x0+x1)/2, (y0+y1)/2); w.patches.push(p);
      if (R() < 0.62) {
        var hx = lerp(p.x0+30, p.x1-40, R()), hy = lerp(p.y0+30, p.y1-40, R());
        addBox(hx, hy, hx+16, hy+10, 6.5, 'casa', { roof:1 });
        var nt = 3 + Math.floor(R()*6);
        for (var k = 0; k < nt; k++) tree(hx + (R()-.3)*60, hy + (R()-.3)*50, 6 + R()*6, 0);
      }
      if (R() < 0.35) { // cortina en un borde
        var vert = R() < 0.5; var L = vert ? p.y1-p.y0 : p.x1-p.x0;
        for (var u = 6; u < L; u += 14) tree(vert ? p.x0+4 : p.x0+u, vert ? p.y0+u : p.y0+4, 5.5, 4);
      }
    }
    w.pois.quintas = { x:-1080, y:420, z:4 };

    // ---------- campo: chacras y lotes ----------
    var CW = 1400, CH = 1250;
    var TONES = ['trigo','siembra','pastura','alfalfa','rastrojo','siembra','trigo','pastura'];
    for (var c2 = -4; c2 <= 3; c2++) for (var r2 = -4; r2 <= 3; r2++) {
      var X0 = AVX + c2*CW, Y0 = -1300 + r2*CH, X1 = X0 + CW, Y1 = Y0 + CH;
      if ((c2 === -1 || c2 === 0) && (r2 === 0 || r2 === 1)) continue;
      w.roads.push([X0, Y0, X1, Y0], [X0, Y0, X0, Y1]);
      var nlot = 1 + Math.floor(R()*3.2), vert2 = R() < 0.5;
      for (var k2 = 0; k2 < nlot; k2++) {
        var fa = k2/nlot, fb = (k2+1)/nlot;
        var lp = vert2 ? { x0:lerp(X0,X1,fa)+8, x1:lerp(X0,X1,fb)-8, y0:Y0+10, y1:Y1-10 } : { x0:X0+10, x1:X1-10, y0:lerp(Y0,Y1,fa)+8, y1:lerp(Y0,Y1,fb)-8 };
        lp.kind = 'lote'; lp.tone = TONES[Math.floor(R()*TONES.length)]; lp.rows = lp.tone !== 'pastura'; lp.sp = 16 + R()*6; lp.dir = R() < 0.5;
        lp.d = Math.hypot((lp.x0+lp.x1)/2, (lp.y0+lp.y1)/2); w.patches.push(lp);
      }
      if (R() < 0.45) { // cortina rompevientos
        var alongX = R() < 0.5, off = R() < 0.5 ? 14 : (alongX ? CH-14 : CW-14), Lc = alongX ? CW : CH;
        for (var u2 = 10; u2 < Lc - 10; u2 += 26) tree(alongX ? X0+u2 : X0+off, alongX ? Y0+off : Y0+u2, 8 + R()*3, 4);
      }
      if (R() < 0.38) { // casco con molino
        var corner = Math.floor(R()*4), hx2 = corner%2 ? X1-110 : X0+60, hy2 = corner < 2 ? Y0+60 : Y1-110;
        addBox(hx2, hy2, hx2+22, hy2+12, 7, 'casa', { roof:1 });
        addBox(hx2+36, hy2-4, hx2+70, hy2+16, 9, 'galpon', { win:false, roof:1 });
        for (var k3 = 0; k3 < 12; k3++) tree(hx2 - 20 + R()*110, hy2 - 30 + R()*30 + (k3%2 ? 50 : 0), 7 + R()*5, 0);
        w.molinos.push({ x:hx2+90, y:hy2+40, h:22, ph:R()*6.28 });
        w.cyl.push({ x:hx2+104, y:hy2+52, r:7, z0:0, h:2.6, kind:'australiano' });
      }
    }
    w.roads.push([AVX, -726, AVX, -6300]);                 // la avenida sigue al norte como camino
    w.roads.push([AVX, w.avenue.y1, AVX, 4000]);
    w.roads.push([-6000, 0, urb.x0, 0], [urb.x1, 0, 6000, 0]);
    var mq = w.molinos.slice().sort(function(a,b){ return Math.hypot(a.x+2400,a.y-1700) - Math.hypot(b.x+2400,b.y-1700); })[0];
    w.pois.campo = mq ? { x:mq.x, y:mq.y, z:20 } : { x:-2400, y:1700, z:0 };
    return w;
  }
  window.Pueblo = { build:build, rng:rng };
})();
