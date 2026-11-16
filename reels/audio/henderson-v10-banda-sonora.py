"""Banda sonora original para el reel V10 tipográfico (Henderson 117 años).

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
rng = np.random.default_rng(2026)

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


# ---------------- arreglo ----------------
# c1 · intro y contador
pad(['D4', 'E4', 'A4', 'D5'], 0.0, 2.6, att=1.6, rel=1.4, bright=0.3, gain=0.035, spread=0.9, wet=0.7)
def eIO(x): return np.where(x < 0.5, 4 * x ** 3, 1 - (-2 * x + 2) ** 3 / 2)
A_, B_, SPIN = [1, 9, 0, 9], [2, 0, 2, 6], [0, 1, 1, 2]
tg = np.arange(0, 2.6, 0.0005)
for d in range(4):                                          # un clic por cada número que pasa
    steps = 1 if d == 0 else (B_[d] - A_[d] + 10) % 10 + 10 * SPIN[d]
    a0, a1 = 0.5 + 0.07 * d, 1.45 + 0.13 * d
    v = A_[d] + steps * eIO(np.clip((tg - a0) / (a1 - a0), 0, 1))
    cross = np.where(np.diff(np.floor(v)) != 0)[0]
    for c in cross:
        tick(tg[c], gain=0.022 + 0.006 * d, pan=-0.45 + 0.3 * d, tone=2600 + 350 * d)
shaped_noise(1.4, 1.15, lambda ta, f: (1 / np.sqrt(1 + ((500 * 2 ** (3.2 * np.clip((ta - 1.4) / 1.1, 0, 1))) / np.maximum(f, 1)) ** 4))
             * np.clip((ta - 1.4) / 1.1, 0, 1) ** 2 / np.sqrt(1 + (f / 9000) ** 4), 31, wet=0.4, gain=0.18, stereo=0.5)

# c2 · 117
boom(2.5, gain=0.5)
for nm, dt, pn in [('D6', 0.0, -0.3), ('A6', 0.05, 0.3), ('F#6', 0.12, 0.0)]:
    bell(nm, 2.5 + dt, gain=0.03, pan=pn)
whoosh(3.35, width=0.3, f0=1800, oct_=1.4, gain=0.12, seed=41)  # brillo al llenarse
pad(['D3', 'A3', 'D4', 'F#4', 'A4', 'E5'], 2.5, 5.0, att=0.5, gain=0.045)
bass('D2', 2.5, 5.0)
for nm, tt0 in [('A4', 3.125), ('D5', 3.75), ('F#5', 4.375)]:
    piano(nm, tt0, vel=0.5)

# c3 · un punto en el mapa
pad(['B2', 'F#3', 'B3', 'D4', 'F#4', 'A4'], 5.0, 7.5, att=0.6, gain=0.043)
bass('B1', 5.0, 7.5)
for nm, tt0 in [('F#5', 5.0), ('E5', 5.625), ('D5', 6.25), ('B4', 6.875)]:
    piano(nm, tt0, vel=0.5)
pop(5.98, gain=0.09); bell('B6', 6.0, gain=0.018, pan=0.2)
for k in range(8):
    shaker(5.0 + k * BEAT / 2 + 0.003 * k, gain=0.018 if k % 2 else 0.026, pan=0.35)

# c4 · desde adentro
whoosh(7.62, width=0.32, f0=320, oct_=2.2, gain=0.22, seed=21)
pad(['G2', 'D3', 'G3', 'B3', 'D4', 'F#4', 'A4'], 7.5, 10.0, att=0.6, gain=0.042, bright=0.6)
bass('G1', 7.5, 10.0)
for nm, tt0 in [('D5', 7.5), ('G5', 8.125), ('F#5', 8.75), ('E5', 9.375)]:
    piano(nm, tt0, vel=0.5)
for k, nm in enumerate(['G3', 'D4', 'G4', 'B4', 'D4', 'G4', 'B4', 'D5']):
    pluck(nm, 7.5 + k * BEAT / 2, vel=0.45, pan=-0.3 + 0.08 * k, gain=0.07)
for k in range(8):
    shaker(7.5 + k * BEAT / 2, gain=0.018 if k % 2 else 0.026, pan=0.35)
kick(7.5, gain=0.25); kick(8.75, gain=0.25)

# c5 · lista rítmica (un golpe por palabra)
chords = [['A2', 'E3', 'A3', 'C#4', 'E4'], ['A2', 'E3', 'A3', 'C#4', 'E4'], ['F#2', 'C#3', 'F#3', 'A3', 'C#4', 'F#4'], ['G2', 'B2', 'D3', 'G3', 'B3', 'G4']]
for k, ch in enumerate(chords):
    t0 = 10.0 + k * BEAT
    kick(t0, gain=0.42); snap(t0 + 0.005, gain=0.10)
    strum(ch, t0 - 0.02, vel=0.7, down=(k % 2 == 0), gain=0.085)
    whoosh(t0 - 0.03, width=0.08, f0=900, oct_=1.6, gain=0.07, seed=60 + k)
    for h in range(2):
        shaker(t0 + h * BEAT / 2, gain=0.022, pan=0.35)
pad(['A2', 'E3', 'A3', 'C#4', 'E4', 'B4'], 10.0, 12.5, att=0.3, gain=0.03, bright=0.65)
bass('A1', 10.0, 11.25); bass('F#1', 11.25, 11.875); bass('G1', 11.875, 12.5)

# c6 · 117 años de gente
pad(['E2', 'B2', 'D3', 'G3', 'B3', 'E4'], 12.5, 13.75, att=0.4, gain=0.04)
pad(['A2', 'E3', 'A3', 'D4', 'E4', 'B4'], 13.75, 14.4, att=0.3, gain=0.04)
pad(['A2', 'E3', 'A3', 'C#4', 'E4', 'B4'], 14.3, 15.0, att=0.3, gain=0.04, rel=0.8)
bass('E2', 12.5, 13.75); bass('A1', 13.75, 15.0)
for k, nm in enumerate(['E3', 'B3', 'D4', 'G4', 'B4', 'G4', 'D4', 'B3', 'A3', 'E4', 'A4', 'C#5', 'E5', 'C#5', 'A4', 'E4']):
    pluck(nm, 12.5 + k * BEAT / 4 * 1.0, vel=0.42, pan=-0.4 + 0.05 * k, gain=0.065)
for nm, tt0 in [('B4', 12.5), ('D5', 13.125), ('E5', 13.75), ('C#5', 14.375)]:
    piano(nm, tt0, vel=0.45)
kick(12.5, gain=0.3); kick(13.75, gain=0.3); snap(13.125, gain=0.06); snap(14.375, gain=0.06)
shaped_noise(13.9, 1.12, lambda ta, f: (1 / np.sqrt(1 + ((700 * 2 ** (3.0 * np.clip((ta - 13.9) / 1.1, 0, 1))) / np.maximum(f, 1)) ** 4))
             * np.clip((ta - 13.9) / 1.1, 0, 1) ** 2.2 / np.sqrt(1 + (f / 9000) ** 4), 71, wet=0.4, gain=0.22, stereo=0.5)

# c7-8 · final
boom(15.0, gain=0.42, f0=22, f1=36)
strum(['D3', 'A3', 'D4', 'F#4', 'A4', 'D5'], 14.99, vel=0.75, gain=0.09, dur=4.5)
pad(['D2', 'A2', 'D3', 'F#3', 'A3', 'D4', 'F#4', 'A4', 'E5'], 15.0, 20.5, att=0.6, rel=2.0, gain=0.048, bright=0.7)
bass('D2', 15.0, 20.5, gain=0.04)
for i, nm in enumerate(['D5', 'E5', 'F#5', 'A5', 'B5', 'D6', 'E6', 'F#6', 'A6']):
    bell(nm, 15.62 + i * 0.06 + 0.12, dur=3.0, gain=0.019, pan=-0.6 + i * 0.15)
whoosh(17.5, width=0.32, f0=3200, oct_=1.2, gain=0.10, seed=81)
bell('D7', 17.5, gain=0.012, pan=0.3)
for nm, tt0, v in [('A4', 16.25, 0.45), ('D5', 16.875, 0.45), ('F#5', 17.5, 0.45), ('A5', 18.125, 0.4), ('D6', 18.75, 0.35)]:
    piano(nm, tt0, vel=v)
for k, nm in enumerate(['D4', 'A4', 'D5', 'F#5', 'A4', 'D5']):
    pluck(nm, 16.25 + k * BEAT / 2, vel=0.38, pan=0.3 - 0.1 * k, gain=0.055)

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

out = sys.argv[1] if len(sys.argv) > 1 else 'henderson-v10.wav'
pcm = (np.stack([mixL, mixR], axis=1) * 32767).astype(np.int16)
with wave.open(out, 'wb') as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
print('ok', out)
