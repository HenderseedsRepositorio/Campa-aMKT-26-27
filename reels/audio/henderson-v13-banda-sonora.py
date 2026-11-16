"""Banda sonora original para el reel V11 "Calle por calle" (Henderson 117 años).

96 BPM (negra = 0,625 s · compás = 2,5 s), Re mayor. Cada compás coincide con una escena:
  c1 0–2,5    intro: pad suave + un clic mecánico por cada número que pasa en el contador
  c2 2,5–5    golpe "117" + D + piano; brillo cuando se llena el número
  c3 5–7,5    Bm + shaker suave; "pop" cuando aparece el punto (6,0 s)
  c4 7,5–10   G + whoosh del anillo; entra la guitarra punteada
  c5 10–12,5  A A F#m G: bombo + chasquido + rasgueo en cada palabra
  c6 12,5–15  Em7 → A, guitarra arpegiada, riser hacia el final
  c7-8 15–20  D: golpe suave, una campana por letra de HENDERSON, brillo del título, final
Uso: python3 henderson-v10-banda-sonora.py salida.wav
"""
import sys, wave
import numpy as np

SR = 48000
DUR = 20.0
N = int(SR * DUR)
BEAT = 0.625
rng = np.random.default_rng(2611)

DRY_L = np.zeros(N); DRY_R = np.zeros(N)
WET_L = np.zeros(N); WET_R = np.zeros(N)


def hz(name):
    names = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    n, o = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((12 * (o + 1) + names[n] - 69) / 12)


def add(sig, start, pan=0.0, gain=1.0, wet=0.3):
    i0 = int(round(start * SR))
    if i0 < 0:
        sig = sig[-i0:]; i0 = 0
    n = min(len(sig), N - i0)
    if n <= 0:
        return
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    s = sig[:n] * gain
    DRY_L[i0:i0 + n] += s * l * (1 - 0.5 * wet); DRY_R[i0:i0 + n] += s * r * (1 - 0.5 * wet)
    WET_L[i0:i0 + n] += s * l * wet;             WET_R[i0:i0 + n] += s * r * wet


def fft_filter(x, fn):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * fn(f), len(x))


def lowpass(x, fc, order=2):
    return fft_filter(x, lambda f: 1 / np.sqrt(1 + (f / fc) ** (2 * order)))


def highpass(x, fc, order=2):
    return fft_filter(x, lambda f: 1 / np.sqrt(1 + (fc / np.maximum(f, 1e-3)) ** (2 * order)))


def bandpass(x, lo, hi):
    return highpass(lowpass(x, hi, 2), lo, 2)


def shaped_noise(t0, dur, gain_fn, seed, wet=0.35, pan=0.0, gain=1.0, stereo=0.0):
    n = int(dur * SR); hop, win = 512, 2048; w = np.hanning(win)
    for ch, pn in enumerate([pan - stereo, pan + stereo] if stereo > 0 else [pan]):
        x = np.random.default_rng(seed + ch).standard_normal(n + win)
        out = np.zeros(len(x)); freqs = np.fft.rfftfreq(win, 1 / SR)
        for i in range(1 + (len(x) - win) // hop):
            X = np.fft.rfft(x[i * hop:i * hop + win] * w) * gain_fn(t0 + (i * hop + win / 2) / SR, freqs)
            out[i * hop:i * hop + win] += np.fft.irfft(X) * w
        add(out[:n] / 1.5, t0, pn, gain / (1.4 if stereo > 0 else 1.0), wet)


# ---------------- instrumentos ----------------
def pad(notes, t0, t1, att=1.2, rel=2.0, bright=0.5, gain=0.045, spread=0.7, wet=0.6):
    dur = t1 - t0 + rel; n = int(dur * SR); tt = np.arange(n) / SR; hold = t1 - t0
    env = np.clip(tt / att, 0, 1) ** 1.6 * np.where(tt < hold, 1.0, np.exp(-(tt - hold) / (rel / 3.2)))
    for idx, name in enumerate(notes):
        f = hz(name); sig = np.zeros(n)
        for det in (-0.0032, 0.0, 0.0039):
            ff = f * (1 + det); ph = rng.random() * 6.283
            for k in range(1, 9):
                if ff * k > 8000:
                    break
                sig += (1 / k ** 1.7) * np.exp(-(k - 1) * (1 - bright) * 0.9) * np.sin(2 * np.pi * ff * k * tt + ph * k)
        sig *= 1 + 0.1 * np.sin(2 * np.pi * (0.11 + 0.04 * idx) * tt + idx)
        low = 0.45 if f < 110 else (0.75 if f < 180 else 1.0)
        add(sig * env / 3.0 * low, t0, ((idx / max(1, len(notes) - 1)) - 0.5) * 2 * spread, gain, wet)


def bass(name, t0, t1, gain=0.042):
    f = hz(name); n = int((t1 - t0 + 0.6) * SR); tt = np.arange(n) / SR
    env = np.clip(tt / 0.04, 0, 1) * np.where(tt < t1 - t0, np.exp(-tt / 3.0), np.exp(-(t1 - t0) / 3.0) * np.exp(-(tt - (t1 - t0)) / 0.18))
    sig = np.sin(2 * np.pi * f * tt) + 0.22 * np.sin(4 * np.pi * f * tt) + 0.08 * np.sin(6 * np.pi * f * tt)
    add(sig * env, t0, 0.0, gain, 0.1)


def piano(name, t0, vel=0.55, dur=3.4, pan=0.0, gain=0.15, wet=0.38):
    f = hz(name); n = int(dur * SR); tt = np.arange(n) / SR; sig = np.zeros(n); B = 0.00035
    for k in range(1, 13):
        fk = f * k * np.sqrt(1 + B * k * k)
        if fk > 11000:
            break
        amp = (1 / k ** 1.15) * np.exp(-0.2 * (k - 1)) * (1.0 if k == 1 else 0.65 + 0.35 * vel)
        tau = 1.9 / (1 + 0.38 * (k - 1)) * (1.0 if f < 700 else 0.75)
        sig += amp * np.sin(2 * np.pi * fk * tt + rng.random() * 6.283) * (0.75 * np.exp(-tt / tau) + 0.25 * np.exp(-tt / (tau * 3.5)))
    sig *= np.clip(tt / 0.004, 0, 1)
    sig += lowpass(rng.standard_normal(n) * np.exp(-tt / 0.01), 2500) * 0.05
    add(sig * vel, t0, pan, gain, wet)


def pluck(name, t0, vel=0.6, dur=2.6, pan=0.0, gain=0.11, wet=0.3, bright=0.55):
    """Cuerda pulsada (Karplus-Strong), procesada por períodos."""
    f = hz(name); n = int(dur * SR); P = int(round(SR / f))
    y = np.zeros(n + P + 2)
    burst = rng.uniform(-1, 1, P)
    burst = lowpass(np.concatenate([burst, np.zeros(P)]), 1500 + 6000 * bright)[:P]
    y[:P] = burst
    damp = 0.996 - 0.004 * (1 - bright)
    i = P
    while i < n:
        j = min(i + P, n)
        y[i:j] = damp * 0.5 * (y[i - P:j - P] + y[i - P - 1:j - P - 1]) if i - P - 1 >= 0 else damp * y[i - P:j - P]
        i = j
    sig = y[:n]
    sig = highpass(sig, 70, 1) * np.clip(np.arange(n) / (0.002 * SR), 0, 1)
    body = lowpass(sig, 900, 1) * 0.35                                # cuerpo de la guitarra
    add((sig + body) * vel, t0, pan, gain, wet)


def strum(notes, t0, vel=0.6, down=True, spacing=0.018, gain=0.10, dur=2.4):
    seq = notes if down else notes[::-1]
    for i, nm in enumerate(seq):
        pluck(nm, t0 + i * spacing, vel=vel * (0.85 + 0.15 * (i / max(1, len(seq) - 1))), dur=dur, pan=-0.35 + 0.7 * i / max(1, len(seq) - 1), gain=gain)


def bell(name_or_f, t0, dur=4.0, gain=0.05, pan=0.0, wet=0.55):
    f = hz(name_or_f) if isinstance(name_or_f, str) else name_or_f
    n = int(dur * SR); tt = np.arange(n) / SR
    ratios = [1.0, 2.0, 2.76, 4.07, 5.40, 6.80]; amps = [1.0, 0.5, 0.38, 0.22, 0.16, 0.08]; taus = [2.8, 1.9, 1.2, 0.8, 0.55, 0.4]
    sig = sum(a * np.sin(2 * np.pi * f * r * tt + rng.random() * 6.283) * np.exp(-tt / tau) for r, a, tau in zip(ratios, amps, taus) if f * r < 16000)
    add(sig * np.clip(tt / 0.002, 0, 1), t0, pan, gain, wet)


def boom(t0, gain=0.5, f0=26, f1=37):
    n = int(3.0 * SR); tt = np.arange(n) / SR
    f = f1 + f0 * np.exp(-tt / 0.2)
    sig = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.9) * np.clip(tt / 0.005, 0, 1)
    add(sig + 0.8 * lowpass(rng.standard_normal(n) * np.exp(-tt / 0.03), 150, 3), t0, 0.0, gain, 0.25)


def kick(t0, gain=0.42):
    n = int(0.5 * SR); tt = np.arange(n) / SR
    f = 46 + 95 * np.exp(-tt / 0.035)
    sig = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.22)
    sig += lowpass(rng.standard_normal(n) * np.exp(-tt / 0.004), 3000) * 0.25
    add(sig, t0, 0.0, gain, 0.06)


def snap(t0, gain=0.12, pan=0.05):
    n = int(0.35 * SR); tt = np.arange(n) / SR
    x = rng.standard_normal(n)
    env = np.exp(-tt / 0.11) * 0.7
    for d in (0.0, 0.009, 0.018):
        env += np.exp(-np.maximum(tt - d, 0) / 0.006) * (tt >= d)
    add(bandpass(x, 900, 5000) * env, t0, pan, gain, 0.35)


def shaker(t0, gain=0.03, pan=0.3):
    n = int(0.12 * SR); tt = np.arange(n) / SR
    x = highpass(rng.standard_normal(n), 5000, 2) * (np.clip(tt / 0.012, 0, 1) * np.exp(-tt / 0.035))
    add(x, t0, pan, gain, 0.2)


def tick(t0, gain=0.03, pan=0.0, tone=3200):
    n = int(0.03 * SR); tt = np.arange(n) / SR
    x = bandpass(rng.standard_normal(n), tone * 0.6, tone * 1.6) * np.exp(-tt / 0.0022)
    x += np.sin(2 * np.pi * tone * 0.5 * tt) * np.exp(-tt / 0.004) * 0.3
    add(x, t0, pan, gain, 0.12)


def pop(t0, gain=0.10):
    n = int(0.4 * SR); tt = np.arange(n) / SR
    f = 520 + 520 * np.exp(-tt / 0.03)
    add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.09) * np.clip(tt / 0.002, 0, 1), t0, 0.0, gain, 0.4)


def whoosh(tc, width=0.45, f0=300, oct_=2.6, gain=0.35, seed=1):
    t0 = tc - 2.2 * width; dur = 4.4 * width
    shaped_noise(t0, dur, lambda ta, f: np.exp(-0.5 * (np.log(np.maximum(f, 20) / (f0 * 2 ** (oct_ * np.exp(-((ta - tc) / width) ** 2)))) / 0.6) ** 2)
                 * np.exp(-((ta - tc) / (width * 1.1)) ** 2) / np.sqrt(1 + (f / 8000) ** 4), seed, wet=0.35, gain=gain, stereo=0.6)



# ---------------- arreglo V13 (desde arriba → el pueblo real) ----------------
def eIO(x): return np.where(x < 0.5, 4 * x ** 3, 1 - (-2 * x + 2) ** 3 / 2)
import json, os
_js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos', 'henderson-osm-v13.js')).read()
OSM = json.loads(_js[len('window.OSM='):_js.index(';\nwindow.REG')])
STREETS = [(s['t'], s['n']) for s in OSM['streets']]
PLACES = [(p['t'], p['n']) for p in OSM['places']]

# c1 · arriba de las nubes: viento, aire, el marcador sobre el pueblo
shaped_noise(0.0, 5.6, lambda ta, f: (0.55 + 0.45 * np.sin(2 * np.pi * 0.23 * ta + 1.0)) * np.clip(ta / 0.6, 0, 1) * np.clip((5.6 - ta) / 1.6, 0, 1)
             / np.sqrt(1 + (f / (500 + 260 * np.sin(2 * np.pi * 0.17 * ta))) ** 4) / np.sqrt(1 + (80 / np.maximum(f, 1)) ** 2), 5, wet=0.5, gain=0.16, stereo=0.8)
pad(['D4', 'E4', 'A4', 'D5'], 0.0, 4.6, att=1.4, rel=1.6, bright=0.3, gain=0.034, spread=0.9, wet=0.75)
bell('A5', 1.3, gain=0.026, dur=3.5, pan=-0.1); bell('E6', 1.36, gain=0.014, pan=0.25)
for i in range(9):  tick(2.4 + (i + 0.5) / 9 * 0.5, gain=0.014, pan=0.3, tone=3400)
for i in range(19): tick(2.7 + (i + 0.5) / 19 * 0.6, gain=0.008, pan=0.35, tone=2600)
for nm, tt0 in [('F#5', 0.9), ('A5', 2.2), ('E5', 3.3)]:
    piano(nm, tt0, vel=0.32)
# las nubes pasan al bajar
shaped_noise(3.0, 2.4, lambda ta, f: np.sin(np.pi * np.clip((ta - 3.0) / 2.4, 0, 1)) ** 2 / np.sqrt(1 + (f / 1800) ** 2) / np.sqrt(1 + (200 / np.maximum(f, 1)) ** 2), 17, wet=0.5, gain=0.12, stereo=0.7)

# c2 · rodeado de campo: el pueblo real se dibuja desde la plaza
bell('D6', 4.3, gain=0.022, pan=0.0); bell('A6', 4.36, gain=0.012, pan=0.3)
pad(['D3', 'A3', 'D4', 'F#4', 'A4', 'E5'], 4.3, 7.6, att=1.0, gain=0.042)
bass('D2', 4.3, 7.6, gain=0.036)
for nm, tt0 in [('A4', 4.6), ('D5', 5.25), ('F#5', 5.9), ('E5', 6.55), ('D5', 7.2)]:
    piano(nm, tt0, vel=0.4)
arp = ['D4', 'A4', 'D5', 'F#5', 'G3', 'D4', 'G4', 'B4', 'A3', 'E4', 'A4', 'C#5']
for k in range(23):
    tt0 = 4.3 + k * BEAT / 2
    seg_ = 0 if tt0 < 7.6 else (1 if tt0 < 9.6 else 2)
    pluck(arp[seg_ * 4 + (k % 4)], tt0, vel=0.26 + 0.1 * min(1, k / 8), pan=-0.35 + 0.7 * ((k * 5) % 9) / 8, gain=0.036)
tt = 4.5
while tt < 9.4:
    bell(['D6', 'E6', 'F#6', 'A6', 'B6', 'D7'][int(rng.random() * 6)], tt, dur=1.4, gain=0.004 + 0.003 * rng.random(), pan=rng.uniform(-0.8, 0.8), wet=0.6)
    tt += 1.0 / (3 + 6 * np.sin(np.pi * (tt - 4.4) / 5.2) ** 2)

# c3 · desde adentro: cada calle y cada lugar real con su nota
pad(['G2', 'D3', 'G3', 'B3', 'D4', 'F#4', 'A4'], 7.6, 9.6, att=0.6, gain=0.042, bright=0.6)
pad(['A2', 'E3', 'A3', 'C#4', 'E4', 'B4'], 9.6, 11.6, att=0.5, gain=0.04, bright=0.6)
bass('G1', 7.6, 9.6); bass('A1', 9.6, 11.6)
for k in range(13):
    shaker(7.6 + k * BEAT / 2, gain=0.012 if k % 2 else 0.018, pan=0.35)
sn = ['F#5', 'A5', 'B5', 'D6', 'E6', 'D6', 'B5', 'A5']
for k, (t0, nm) in enumerate(STREETS):
    pluck(sn[k % len(sn)], t0, vel=0.5, gain=0.055, pan=(-0.4 if k % 2 else 0.4), bright=0.65)
    bell(sn[k % len(sn)], t0 + 0.005, dur=1.4, gain=0.006, pan=(0.3 if k % 2 else -0.3), wet=0.6)
    for i in range(len(nm)):
        if nm[i] != ' ': tick(t0 + 0.04 + (i + 0.5) / len(nm) * 0.36, gain=0.008, pan=(-0.25 if k % 2 else 0.25), tone=3100)
pn_ = ['D5', 'E5', 'F#5', 'A5', 'B5', 'D6']
for k, (t0, nm) in enumerate(PLACES):
    pluck(pn_[k % len(pn_)], t0, vel=0.6, gain=0.075, pan=-0.3 + 0.12 * k)
    pop(t0 + 0.01, gain=0.04); kick(t0, gain=0.14)
    for i in range(len(nm)):
        if nm[i] != ' ': tick(t0 + 0.16 + (i + 0.5) / len(nm) * 0.30, gain=0.008, pan=0.2, tone=3000)
for nm, tt0 in [('D5', 7.6), ('B4', 8.55), ('C#5', 9.6), ('E5', 10.55)]:
    piano(nm, tt0, vel=0.38)
shaped_noise(10.5, 1.12, lambda ta, f: (1 / np.sqrt(1 + ((700 * 2 ** (3.0 * np.clip((ta - 10.5) / 1.1, 0, 1))) / np.maximum(f, 1)) ** 4))
             * np.clip((ta - 10.5) / 1.1, 0, 1) ** 2.2 / np.sqrt(1 + (f / 9000) ** 4), 71, wet=0.4, gain=0.16, stereo=0.5)

# c4 · cae la noche: se encienden las esquinas reales
boom(11.6, gain=0.4, f0=24, f1=36)
for k, (nm, dt, pn) in enumerate([('B5', 0.0, -0.4), ('F#6', 0.07, 0.35), ('D7', 0.16, -0.1), ('F#7', 0.27, 0.5)]):
    bell(nm, 11.62 + dt, gain=0.018, pan=pn)
for k in range(18):
    bell(['B6', 'F#6', 'D7', 'A6', 'E7', 'F#6'][k % 6], 11.9 + k * 0.075 + 0.03 * rng.random(), dur=2.2, gain=0.007, pan=rng.uniform(-0.8, 0.8))
pad(['B2', 'F#3', 'B3', 'D4', 'F#4', 'A4'], 11.6, 12.9, att=0.4, gain=0.04)
pad(['E2', 'B2', 'D3', 'G3', 'B3', 'E4'], 12.9, 13.6, att=0.3, gain=0.038)
pad(['A2', 'E3', 'A3', 'C#4', 'E4', 'B4'], 13.6, 14.2, att=0.3, gain=0.038, rel=0.8)
bass('B1', 11.6, 12.9); bass('E2', 12.9, 13.6); bass('A1', 13.6, 14.2)
for nm, tt0 in [('F#5', 11.6), ('D5', 12.25), ('E5', 12.9), ('C#5', 13.55)]:
    piano(nm, tt0, vel=0.42)
for c in range(5):
    r2 = np.random.default_rng(90 + c)
    n = int((20.0 - (12.2 + 0.3 * c)) * SR); tt2 = np.arange(n) / SR
    burst = (np.sin(2 * np.pi * (1.6 + 1.6 * r2.random()) * tt2 + r2.random() * 6.283) > 0.55).astype(float)
    pulse = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * (26 + 6 * r2.random()) * tt2))
    env = np.clip(lowpass(burst * pulse, 400, 2), 0, None) * np.clip(tt2 / 1.8, 0, 1) * np.clip((20.0 - (12.2 + 0.3 * c) - tt2) / 1.0, 0, 1)
    add(np.sin(2 * np.pi * (4200 + 700 * r2.random()) * tt2) * env, 12.2 + 0.3 * c, r2.uniform(-0.9, 0.9), 0.006 + 0.003 * r2.random(), 0.45)

# c5 · final: Feliz cumpleaños, HENDERSON · Del campo al pueblo
boom(14.2, gain=0.3, f0=20, f1=36)
strum(['D3', 'A3', 'D4', 'F#4', 'A4', 'D5'], 14.22, vel=0.72, gain=0.09, dur=4.0)
pad(['D2', 'A2', 'D3', 'F#3', 'A3', 'D4', 'F#4', 'A4', 'E5'], 14.2, 20.5, att=0.7, rel=2.0, gain=0.048, bright=0.7)
bass('D2', 14.2, 20.5, gain=0.04)
for i, nm in enumerate(['D5', 'E5', 'F#5', 'A5', 'B5', 'D6', 'E6', 'F#6', 'A6']):
    bell(nm, 14.5 + i * 0.05 + 0.1, dur=3.0, gain=0.019, pan=-0.6 + i * 0.15)
whoosh(16.3, width=0.32, f0=3200, oct_=1.2, gain=0.1, seed=81)
bell('D7', 16.3, gain=0.012, pan=0.3)
pop(16.45, gain=0.05); bell('A6', 16.47, gain=0.014, pan=0.0); bell('F#6', 16.55, gain=0.01, pan=-0.3)
for nm, tt0 in [('A4', 15.2), ('D5', 15.55), ('F#5', 16.2), ('E5', 16.85), ('D5', 17.5), ('A5', 18.3)]:
    piano(nm, tt0, vel=0.4)

# ---------------- reverb y master ----------------
def make_ir(dur=3.0, seed=7):
    n = int(dur * SR); tt = np.arange(n) / SR; irs = []
    for ch in range(2):
        r = np.random.default_rng(seed + ch).standard_normal(n)
        ir = r * np.exp(-tt / 0.8) * np.clip(tt / 0.012, 0, 1)
        lp1, lp2 = lowpass(ir, 4200), lowpass(ir, 1300); mw = np.clip(tt / 1.5, 0, 1)
        ir = (ir * 0.35 + lp1 * 0.65) * (1 - mw) + lp2 * mw
        for d, g in [(0.011, 0.5), (0.019, 0.38), (0.031, 0.3), (0.043, 0.24), (0.061, 0.18)]:
            ir[int((d + 0.0027 * ch) * SR)] += g
        irs.append(ir / np.sqrt(np.sum(ir ** 2)))
    return irs


def conv(x, h):
    m = len(x) + len(h) - 1; nfft = 1 << (m - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(h, nfft), nfft)[:len(x)]


irL, irR = make_ir()
mixL = DRY_L + 0.8 * conv(WET_L, irL)
mixR = DRY_R + 0.8 * conv(WET_R, irR)
mixL = highpass(mixL, 42, 2); mixR = highpass(mixR, 42, 2)
env = np.sqrt(lowpass((mixL ** 2 + mixR ** 2) / 2, 8, 1).clip(1e-9))
g = lowpass(np.where(env > 0.16, (0.16 / env) ** 0.25, 1.0), 5, 1)
mixL *= g; mixR *= g
fade = np.clip(np.arange(N) / (0.08 * SR), 0, 1) * np.clip((N - np.arange(N)) / (1.3 * SR), 0, 1)
mixL *= fade; mixR *= fade
peak = max(np.max(np.abs(mixL)), np.max(np.abs(mixR)))
mixL *= 0.84 / peak; mixR *= 0.84 / peak
peak = max(np.max(np.abs(mixL)), np.max(np.abs(mixR)))
mixL *= 0.84 / peak; mixR *= 0.84 / peak

out = sys.argv[1] if len(sys.argv) > 1 else 'henderson-v13.wav'
pcm = (np.stack([mixL, mixR], axis=1) * 32767).astype(np.int16)
with wave.open(out, 'wb') as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
print('ok', out)
