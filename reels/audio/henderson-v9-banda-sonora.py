"""Banda sonora original para el reel V9 (Henderson 117 años).

Síntesis aditiva + ruido filtrado + reverb por convolución, todo en numpy.
Sincronizada con la línea de tiempo del video (20 s):
  0–6.4 s   viento de altura, pad aéreo, "ping" del marcador y tipeo del nombre, whoosh al atravesar la nube
  6.4–13.6  Re mayor: pads, bajo y piano (D add9 → Bm7 → G maj9)
  12.4–13.6 riser hacia la noche; 13.6 golpe grave + destellos cuando se encienden las luces
  13.6–20   A sus → A → D; grillos; una campana por cada letra de HENDERSON; brillo del título; final
Uso: python3 henderson-v9-banda-sonora.py salida.wav
"""
import sys, wave
import numpy as np

SR = 48000
DUR = 20.0
N = int(SR * DUR)
rng = np.random.default_rng(1909)

DRY_L = np.zeros(N); DRY_R = np.zeros(N)
WET_L = np.zeros(N); WET_R = np.zeros(N)


def hz(name):
    names = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    n, o = name[:-1], int(name[-1])
    midi = 12 * (o + 1) + names[n]
    return 440.0 * 2 ** ((midi - 69) / 12)


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
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * fn(f), len(x))


def lowpass(x, fc, order=2):
    return fft_filter(x, lambda f: 1 / np.sqrt(1 + (f / fc) ** (2 * order)))


def highpass(x, fc, order=2):
    return fft_filter(x, lambda f: 1 / np.sqrt(1 + (fc / np.maximum(f, 1e-3)) ** (2 * order)))


def shaped_noise(t0, dur, gain_fn, seed, wet=0.35, pan=0.0, gain=1.0, stereo=0.0):
    """Ruido con filtro variable en el tiempo (STFT). gain_fn(t_abs, freqs) -> ganancia por bin."""
    n = int(dur * SR); hop, win = 512, 2048
    w = np.hanning(win)
    for ch, pn in enumerate([pan - stereo, pan + stereo] if stereo > 0 else [pan]):
        x = np.random.default_rng(seed + ch).standard_normal(n + win)
        out = np.zeros(len(x))
        freqs = np.fft.rfftfreq(win, 1 / SR)
        frames = 1 + (len(x) - win) // hop
        for i in range(frames):
            seg = x[i * hop:i * hop + win] * w
            X = np.fft.rfft(seg) * gain_fn(t0 + (i * hop + win / 2) / SR, freqs)
            out[i * hop:i * hop + win] += np.fft.irfft(X) * w
        add(out[:n] / 1.5, t0, pn, gain / (1.4 if stereo > 0 else 1.0), wet)


# ---------------- instrumentos ----------------
def pad(notes, t0, t1, att=1.4, rel=2.2, bright=0.5, gain=0.05, spread=0.7, wet=0.6):
    dur = t1 - t0 + rel
    n = int(dur * SR); tt = np.arange(n) / SR
    hold = t1 - t0
    env = np.clip(tt / att, 0, 1) ** 1.6
    env *= np.where(tt < hold, 1.0, np.exp(-(tt - hold) / (rel / 3.2)))
    for idx, name in enumerate(notes):
        f = hz(name)
        sig = np.zeros(n)
        for det in (-0.0032, 0.0, 0.0039):
            ff = f * (1 + det); ph = rng.random() * 6.283
            for k in range(1, 9):
                if ff * k > 8000:
                    break
                amp = (1 / k ** 1.7) * np.exp(-(k - 1) * (1 - bright) * 0.9)
                sig += amp * np.sin(2 * np.pi * ff * k * tt + ph * k)
        sig *= 1 + 0.12 * np.sin(2 * np.pi * (0.11 + 0.04 * idx) * tt + idx)
        pn = ((idx / max(1, len(notes) - 1)) - 0.5) * 2 * spread
        add(sig * env / 3.0, t0, pn, gain, wet)


def bass(name, t0, t1, gain=0.10):
    f = hz(name); dur = t1 - t0 + 0.8
    n = int(dur * SR); tt = np.arange(n) / SR
    env = np.clip(tt / 0.25, 0, 1) * np.where(tt < t1 - t0, 1.0, np.exp(-(tt - (t1 - t0)) / 0.25))
    sig = np.sin(2 * np.pi * f * tt) + 0.18 * np.sin(4 * np.pi * f * tt) + 0.05 * np.sin(6 * np.pi * f * tt)
    add(sig * env, t0, 0.0, gain, 0.12)


def piano(name, t0, vel=0.6, dur=3.8, pan=0.0, gain=0.16, wet=0.38):
    f = hz(name); n = int(dur * SR); tt = np.arange(n) / SR
    sig = np.zeros(n); B = 0.00035
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


def bell(name_or_f, t0, dur=4.5, gain=0.05, pan=0.0, wet=0.55):
    f = hz(name_or_f) if isinstance(name_or_f, str) else name_or_f
    n = int(dur * SR); tt = np.arange(n) / SR
    ratios = [1.0, 2.0, 2.76, 4.07, 5.40, 6.80]
    amps = [1.0, 0.5, 0.38, 0.22, 0.16, 0.08]
    taus = [2.8, 1.9, 1.2, 0.8, 0.55, 0.4]
    sig = sum(a * np.sin(2 * np.pi * f * r * tt + rng.random() * 6.283) * np.exp(-tt / tau) for r, a, tau in zip(ratios, amps, taus) if f * r < 16000)
    add(sig * np.clip(tt / 0.002, 0, 1), t0, pan, gain, wet)


def boom(t0, gain=0.55):
    n = int(3.2 * SR); tt = np.arange(n) / SR
    f = 37 + 26 * np.exp(-tt / 0.22)
    sig = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.95) * np.clip(tt / 0.006, 0, 1)
    thump = lowpass(rng.standard_normal(n) * np.exp(-tt / 0.035), 160, 3)
    add(sig + 0.8 * thump, t0, 0.0, gain, 0.28)


def tick(t0, gain=0.035, pan=0.0):
    n = int(0.02 * SR); tt = np.arange(n) / SR
    x = highpass(lowpass(rng.standard_normal(n), 5500), 1800) * np.exp(-tt / 0.0025)
    add(x, t0, pan, gain, 0.15)


def cricket(t0, t1, f, rate, gain, pan, seed):
    r = np.random.default_rng(seed)
    n = int((t1 - t0) * SR); tt = np.arange(n) / SR
    burst = (np.sin(2 * np.pi * rate * tt + r.random() * 6.283) > 0.55).astype(float)
    pulse = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * (26 + 6 * r.random()) * tt))
    env = lowpass(burst * pulse, 400, 2)
    env = np.clip(env, 0, None)
    sig = np.sin(2 * np.pi * f * tt) * env * (1 + 0.3 * np.sin(2 * np.pi * 0.3 * tt))
    fade = np.clip(tt / 1.8, 0, 1) * np.clip((t1 - t0 - tt) / 1.0, 0, 1)
    add(sig * fade, t0, pan, gain, 0.45)


# ---------------- arreglo ----------------
# Aire / introducción
pad(['A4', 'D5', 'E5', 'A5'], 0.2, 6.6, att=2.6, rel=2.5, bright=0.25, gain=0.035, spread=0.9, wet=0.75)
shaped_noise(0.0, 9.5, lambda ta, f: np.exp(-0.5 * (np.log(np.maximum(f, 20) / (380 + 220 * np.sin(0.4 * ta))) / 0.55) ** 2)
             * (0.55 + 0.45 * np.sin(0.9 * ta + 1.3) ** 2) * np.clip(ta / 1.2, 0, 1) * np.clip((9.5 - ta) / 3.0, 0, 1), 11, wet=0.25, gain=0.20, stereo=0.5)
bell('E6', 2.25, gain=0.045, pan=0.15)                       # el anillo del marcador se cierra
bell('B6', 2.3, gain=0.02, pan=0.25)
for i in range(9):                                            # tipeo de HENDERSON
    tick(2.62 + i * 0.054, pan=0.25 + i * 0.03)
# atravesar la nube
shaped_noise(4.4, 2.8, lambda ta, f: np.exp(-0.5 * (np.log(np.maximum(f, 20) / (280 * 2 ** (2.6 * np.exp(-((ta - 5.9) / 0.55) ** 2)))) / 0.6) ** 2) / np.sqrt(1 + (f / 7000) ** 4)
             * np.exp(-((ta - 5.9) / 0.6) ** 2), 21, wet=0.35, gain=0.55, stereo=0.6)

# Re mayor
pad(['D3', 'A3', 'D4', 'F#4', 'A4', 'E5'], 6.1, 9.4, att=1.2, gain=0.050)
pad(['B2', 'F#3', 'B3', 'D4', 'F#4', 'A4'], 9.2, 11.1, att=0.9, gain=0.048)
pad(['G2', 'D3', 'G3', 'B3', 'D4', 'F#4', 'A4'], 10.9, 13.7, att=0.9, gain=0.046, bright=0.6)
pad(['A2', 'E3', 'A3', 'D4', 'E4', 'B4'], 13.5, 14.9, att=0.4, gain=0.050, bright=0.65)
pad(['A2', 'E3', 'A3', 'C#4', 'E4', 'B4'], 14.8, 16.5, att=0.6, gain=0.050, bright=0.65)
pad(['D2', 'A2', 'D3', 'F#3', 'A3', 'D4', 'F#4', 'A4', 'E5'], 16.3, 20.5, att=0.9, rel=2.0, gain=0.050, bright=0.7)
for name, a, b in [('D2', 6.4, 9.3), ('B1', 9.3, 11.0), ('G1', 11.0, 13.6), ('A1', 13.6, 16.3), ('D2', 16.3, 20.5)]:
    bass(name, a, b, gain=0.065)

melody = [('F#5', 6.7, 0.55), ('A5', 7.3, 0.5), ('E5', 8.0, 0.5), ('D5', 8.6, 0.45),
          ('D5', 9.4, 0.5), ('F#5', 10.0, 0.5), ('B5', 10.6, 0.55),
          ('B4', 11.1, 0.5), ('D5', 11.7, 0.5), ('G5', 12.3, 0.55), ('F#5', 12.9, 0.5),
          ('E5', 13.65, 0.6), ('C#5', 14.5, 0.45), ('E5', 15.2, 0.45), ('A5', 15.8, 0.5),
          ('D5', 16.45, 0.5), ('A4', 18.6, 0.4), ('F#5', 18.62, 0.38), ('D6', 18.65, 0.35)]
for i, (nm, tt0, v) in enumerate(melody):
    piano(nm, tt0, vel=v, pan=-0.2 + 0.4 * ((i * 7) % 5) / 4)

# Hacia la noche: riser, golpe y destellos
shaped_noise(12.2, 1.45, lambda ta, f: (1 / np.sqrt(1 + ((700 * 2 ** (3.0 * np.clip((ta - 12.2) / 1.4, 0, 1))) / np.maximum(f, 1)) ** 4))
             * np.clip((ta - 12.2) / 1.4, 0, 1) ** 2.2 / np.sqrt(1 + (f / 9000) ** 4), 31, wet=0.4, gain=0.26, stereo=0.5)
boom(13.62, gain=0.5)
for k, (nm, dt, pn) in enumerate([('A6', 0.0, -0.4), ('E6', 0.07, 0.35), ('C#7', 0.16, -0.1), ('E7', 0.27, 0.5), ('A6', 0.41, -0.6), ('B6', 0.55, 0.2)]):
    bell(nm, 13.66 + dt, gain=0.022, pan=pn)
for k in range(10):                                           # luces que titilan
    bell(['A6', 'E6', 'B6', 'C#7', 'E7'][k % 5], 14.1 + k * 0.21 + 0.05 * rng.random(), dur=2.5, gain=0.010, pan=rng.uniform(-0.8, 0.8))
# grillos de la noche pampeana
for c in range(6):
    cricket(13.9 + 0.3 * c, 20.0, 4200 + 700 * rng.random(), 1.6 + 1.6 * rng.random(), 0.006 + 0.004 * rng.random(), rng.uniform(-0.9, 0.9), 50 + c)

# Título: una campana por letra, brillo del barrido
for i, nm in enumerate(['D5', 'E5', 'F#5', 'A5', 'B5', 'D6', 'E6', 'F#6', 'A6']):
    bell(nm, 16.82 + i * 0.055 + 0.18, dur=3.0, gain=0.020, pan=-0.6 + i * 0.15)
shaped_noise(17.9, 1.3, lambda ta, f: np.exp(-0.5 * (np.log(np.maximum(f, 20) / (3500 * 2 ** (1.3 * np.clip((ta - 17.9) / 1.1, 0, 1)))) / 0.5) ** 2)
             * np.exp(-((ta - 18.5) / 0.32) ** 2), 41, wet=0.5, gain=0.16, stereo=0.7)
bell('D7', 18.5, gain=0.012, pan=0.3)

# ---------------- reverb ----------------
def make_ir(dur=3.4, seed=7):
    n = int(dur * SR); tt = np.arange(n) / SR
    irs = []
    for ch in range(2):
        r = np.random.default_rng(seed + ch).standard_normal(n)
        ir = r * np.exp(-tt / 0.9) * np.clip(tt / 0.012, 0, 1)
        lp1, lp2 = lowpass(ir, 4200), lowpass(ir, 1300)
        mw = np.clip(tt / 1.6, 0, 1)
        ir = (ir * 0.35 + lp1 * 0.65) * (1 - mw) + lp2 * mw
        for d, g in [(0.011, 0.5), (0.019, 0.38), (0.031, 0.3), (0.043, 0.24), (0.061, 0.18)]:
            ir[int((d + 0.0027 * ch) * SR)] += g
        irs.append(ir / np.sqrt(np.sum(ir ** 2)))
    return irs


def conv(x, h):
    m = len(x) + len(h) - 1
    nfft = 1 << (m - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(h, nfft), nfft)[:len(x)]


irL, irR = make_ir()
wl, wr = conv(WET_L, irL), conv(WET_R, irR)
mixL = DRY_L + 0.85 * wl
mixR = DRY_R + 0.85 * wr

# ---------------- master ----------------
mixL = highpass(mixL, 28, 2); mixR = highpass(mixR, 28, 2)
env = np.sqrt(lowpass((mixL ** 2 + mixR ** 2) / 2, 6, 1).clip(1e-9))
thr = 0.12
g = np.where(env > thr, (thr / env) ** 0.35, 1.0)             # compresión suave ~1.5:1
g = lowpass(g, 4, 1)
mixL *= g; mixR *= g
fade = np.clip(np.arange(N) / (0.5 * SR), 0, 1) * np.clip((N - np.arange(N)) / (1.2 * SR), 0, 1)
mixL *= fade; mixR *= fade
peak = max(np.max(np.abs(mixL)), np.max(np.abs(mixR)))
mixL *= 0.84 / peak; mixR *= 0.84 / peak
mixL = np.tanh(mixL * 1.05) / np.tanh(1.05); mixR = np.tanh(mixR * 1.05) / np.tanh(1.05)
peak = max(np.max(np.abs(mixL)), np.max(np.abs(mixR)))
mixL *= 0.84 / peak; mixR *= 0.84 / peak

out = sys.argv[1] if len(sys.argv) > 1 else 'henderson-v9.wav'
pcm = (np.stack([mixL, mixR], axis=1) * 32767).astype(np.int16)
with wave.open(out, 'wb') as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
rms = np.sqrt(np.mean((mixL ** 2 + mixR ** 2) / 2))
print('ok', out, 'rms dBFS %.1f' % (20 * np.log10(rms)))
