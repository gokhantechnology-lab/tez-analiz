# CLAUDE.md — tez-analiz

Bu dosya, projeyi ilk kez gören yapay zeka araçlarına (Claude, Copilot, Cursor vb.) tam bağlam sağlamak için yazılmıştır.

---

## Proje Özeti

Fen bilimleri eğitimi alanında hazırlanan yüksek lisans tezinin istatistik analiz pipeline'ı.

**Araştırma deseni:** Tek grup, ön test – son test  
**Katılımcılar:** ~50 öğrenci (her ölçekte eşleşen N değişir)  
**Amaç:** Uygulanan eğitim programının iletişim becerileri ve problem çözme becerileri üzerindeki etkisini ölçmek  

İki ölçek analiz edilmektedir:
1. **İBDÖ** — İletişim Becerileri Ölçeği (Korkut Owen & Bugay, 2014)
2. **PÇBÖ** — Problem Çözme Becerileri Ölçeği / PSI (Şahin, Şahin & Heppner, 1993)

---

## Repo Yapısı

```
tez-analiz/
├── iletisim_analiz.py          # İBDÖ analiz scripti
├── iletisim_notebook.ipynb     # İBDÖ görselleştirme notebook'u (çalıştırılmış)
├── problem_cozme_analiz.py     # PÇBÖ analiz scripti
├── problem_cozme_notebook.ipynb # PÇBÖ görselleştirme notebook'u (çalıştırılmış)
├── pyproject.toml              # uv proje bağımlılıkları
├── uv.lock                     # Kilitli bağımlılık versiyonları
├── .venv/                      # Python 3.12 sanal ortamı (uv)
└── data/
    ├── olcek_yapilari.md       # Her iki ölçeğin madde-alt boyut eşleşmesi, ters maddeler
    ├── İletişim_Becerileri/
    │   ├── öntest/             # İBDÖ ön test Excel dosyası
    │   └── sontest/            # İBDÖ son test Excel dosyası
    └── Problem_Çözme_Becerileri/
        ├── öntest/             # PÇBÖ ön test Excel dosyası
        └── sontest/            # PÇBÖ son test Excel dosyası
```

---

## Veri Yapısı (Excel Dosyaları)

### İBDÖ (25 madde)

| Dosya | Sütun Düzeni |
|-------|-------------|
| Ön test (50 satır, 29 sütun) | `[0]` zaman damgası → `[1:26]` 25 madde → `[26]` isim → `[27]` numara → `[28]` e-posta |
| Son test (52 satır, 28 sütun) | `[0]` zaman damgası → `[1]` isim → `[2]` numara → `[3:28]` 25 madde |

### PÇBÖ (35 madde)

| Dosya | Sütun Düzeni |
|-------|-------------|
| Ön test (50 satır, 38 sütun) | `[0]` zaman damgası → `[1:36]` 35 madde → `[36]` isim → `[37]` numara |
| Son test (47 satır, 38 sütun) | `[0]` zaman damgası → `[1]` isim → `[2]` numara → `[3:38]` 35 madde |

> **Dikkat:** Ön test ve son test dosyalarında isim/numara sütunlarının yeri farklıdır. `yukle_ve_temizle()` fonksiyonundaki `isim_ontest: bool` parametresi bu farkı yönetir.

### Katılımcı Eşleştirme

Ön test ve son test, **öğrenci numarası** üzerinden eşleştirilir. Yinelenen numara varsa son giriş alınır (`drop_duplicates(keep='last')`). Son test dosyasında tespit edilen bir yineleme vardı (İBDÖ: `100623009`).

Eşleşen N: **İBDÖ = 44**, **PÇBÖ = 40**

---

## Ölçek Puanlama Mantığı

### İBDÖ — 5'li Likert

```python
LIKERT_MAP = {
    "Hiçbir zaman": 1,
    "Nadiren":       2,
    "Bazen":         3,
    "Sık sık":       4,
    "Her zaman":     5,
}
```

- Ters puanlı madde **yok**
- Yüksek puan = daha iyi iletişim becerisi
- Alt boyut puanı = ilgili maddelerin **ortalaması** (1–5 arası)

### PÇBÖ — 6'lı Likert

```python
LIKERT_MAP = {
    "Hep böyle davranırım":           1,
    "Çoğunlukla böyle davranırım":    2,
    "Sıklıkla böyle davranırım":      3,
    "Arada sırada böyle davranırım":  4,
    "Ender olarak böyle davranırım":  5,
    "Hiç böyle davranmam":            6,
}
```

- **17 ters puanlı madde** → düzeltme formülü: `7 − ham_puan`
- Ters maddeler: `[1, 2, 3, 4, 9, 13, 14, 15, 17, 21, 22, 25, 26, 29, 30, 32, 34]`
- Düzeltme sonrası yön: **düşük ortalama = daha iyi problem çözme becerisi** (orijinal PSI yönü)
- Maddeler 9, 12, 22 dolgu (filler) maddeleridir — toplama dahil, alt boyutlara dahil değil

---

## Alt Boyut Yapıları

### İBDÖ (4 alt boyut)

| Kod | Alt Boyut | Maddeler | α (bu çalışma) |
|-----|-----------|----------|----------------|
| F1_İİTB | İletişim İlkeleri ve Temel Beceriler | 1,3,6,13,15,16,21,23,24,25 | ~.79 |
| F2_KİE | Kendini İfade Etme | 2,5,17,20 | ~.72 |
| F3_EDSÖİ | Etkin Dinleme ve Sözel Olmayan İletişim | 10,11,12,18,19,22 | ~.64 |
| F4_İKİ | İletişim Kurmaya İsteklilik | 4,7,8,9,14 | ~.71 |
| — | **İBDÖ Toplam** | 1–25 | **0.857** |

### PÇBÖ (3 alt boyut)

| Kod | Alt Boyut | Maddeler | α (bu çalışma) |
|-----|-----------|----------|----------------|
| F1_PCG | Problem Çözmeye Güvenme | 1,2,3,4,11,19,20,23,24,27,33 | 0.840 |
| F2_YKS | Yaklaşma-Kaçınma Stili | 5,7,8,13,14,15,16,17,21,25,26,28,30,31,32,35 | 0.833 |
| F3_KK | Kişisel Kontrol | 6,10,18,29,34 | 0.634 |
| — | **PÇBÖ Toplam** | 1–35 | **0.912** |

---

## Analiz Akışı

Her iki ölçek için aynı akış uygulanır:

```
1. Veri yükleme ve Likert → sayısal dönüşümü
2. Ters madde düzeltmesi (sadece PÇBÖ)
3. Katılımcı eşleştirme (öğrenci numarası)
4. Alt boyut ve toplam puan hesaplama (madde ortalaması)
        ↓
5. Güvenirlik analizi      → Cronbach α (ön + son birleşik)
6. Tanımlayıcı istatistik  → N, x̄, SS, Min, Max
7. Normallik testi         → Shapiro-Wilk (n < 50 için uygun)
8. Fark testi              → Bağımlı örneklem t-testi (Paired t-test)
9. Etki büyüklüğü          → Cohen's d (farkların ort/SS oranı)
```

Cohen's d sınıflandırması: < 0.2 Çok küçük | 0.2–0.5 Küçük | 0.5–0.8 Orta | ≥ 0.8 Büyük

---

## Analiz Sonuçları (Özet)

### İBDÖ — Anlamlı fark yok

| Alt Boyut | Ön x̄ | Son x̄ | t(43) | p | d |
|-----------|-------|--------|--------|---|---|
| İletişim İlkeleri ve Temel Beceriler | 3.920 | 3.993 | 1.102 | .277 | 0.166 |
| Kendini İfade Etme | 3.653 | 3.790 | 1.416 | .164 | 0.213 |
| Etkin Dinleme ve Sözel Olmayan İletişim | 3.909 | 3.992 | 1.326 | .192 | 0.200 |
| İletişim Kurmaya İsteklilik | 3.705 | 3.741 | 0.649 | .520 | 0.098 |
| **İBDÖ Toplam** | **3.832** | **3.910** | **1.476** | **.147** | **0.223** |

### PÇBÖ — Toplam ve 2 alt boyutta anlamlı azalış (gelişim)

| Alt Boyut | Ön x̄ | Son x̄ | t(39) | p | d |
|-----------|-------|--------|--------|---|---|
| Problem Çözmeye Güvenme | 2.659 | 2.386 | 3.885 | **.000** | 0.614 (Orta) |
| Yaklaşma-Kaçınma Stili | 3.033 | 2.986 | 0.553 | .584 | 0.087 |
| Kişisel Kontrol | 2.815 | 2.525 | 2.609 | **.013** | 0.412 (Küçük) |
| **PÇBÖ Toplam** | **2.904** | **2.741** | **2.372** | **.023** | **0.375 (Küçük)** |

> PÇBÖ'de azalış = gelişim (düşük puan = daha iyi problem çözme becerisi).

---

## Geliştirme Ortamı

```bash
# Bağımlılıkları kur
uv sync --all-groups

# Analiz scriptlerini çalıştır
uv run python iletisim_analiz.py
uv run python problem_cozme_analiz.py

# Notebook'u çalıştır ve güncelle
uv run jupyter nbconvert --to notebook --execute --inplace iletisim_notebook.ipynb
uv run jupyter nbconvert --to notebook --execute --inplace problem_cozme_notebook.ipynb

# Jupyter Lab arayüzü
uv run jupyter lab
```

### Bağımlılıklar (pyproject.toml)

| Paket | Amaç |
|-------|------|
| pandas ≥ 2.2 | Veri manipülasyonu |
| numpy ≥ 1.26 | Sayısal hesaplama |
| scipy ≥ 1.13 | Shapiro-Wilk, paired t-test |
| matplotlib ≥ 3.8 | Görselleştirme |
| seaborn ≥ 0.13 | Violin plot |
| openpyxl ≥ 3.1 | Excel okuma |
| ipykernel ≥ 6.29 | Notebook kernel |

---

## Önemli Notlar

- Excel dosyalarında Türkçe karakter içeren klasör ve dosya adları var — path'lerde encoding sorununa dikkat.
- `Styler.applymap()` pandas ≥ 2.x'te kaldırıldı, `.map()` kullanılmalı.
- PÇBÖ son test dosyasında `İsim - Soyisim` ve `Öğrenci numarası` sütunları **ön testten farklı konumda** — `isim_ontest=False` parametresi bu farkı çözer.
- Tüm analizlerde birleşik (ön + son) veri üzerinden Cronbach α hesaplanır.
