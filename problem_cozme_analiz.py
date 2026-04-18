"""
Problem Çözme Becerileri Ölçeği (PÇBÖ) - Ön Test / Son Test Analizi
Kaynak: Şahin, Şahin & Heppner (1993) — PSI Türkçe uyarlaması

Puanlama notu:
  Ham kodlama  : 1=Hep böyle davranırım … 6=Hiç böyle davranmam
  Ters maddeler: düzeltme = 7 − ham_puan (17 madde)
  Yön          : düşük düzeltilmiş ortalama → daha iyi problem çözme becerisi
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

COL_OLCEK = "Ölçek / Alt Boyut"
COL_OLCUM = "Ölçüm"

# ── Dosya yolları ─────────────────────────────────────────────────────────────
ONTEST_PATH  = "data/Problem_Çözme_Becerileri/öntest/PÇBÖ - Ön test - Yanıtlar adlı dosyanın kopyası.xlsx"
SONTEST_PATH = "data/Problem_Çözme_Becerileri/sontest/PÇBÖ - Son test - Yanıtlar adlı dosyanın kopyası.xlsx"

# ── Likert → sayısal ──────────────────────────────────────────────────────────
# Orijinal PSI kodlaması: 1=Hep (yüksek benimseme) … 6=Hiç (düşük benimseme)
LIKERT_MAP = {
    "Hep böyle davranırım":           1,
    "Çoğunlukla böyle davranırım":    2,
    "Sıklıkla böyle davranırım":      3,
    "Arada sırada böyle davranırım":  4,
    "Ender olarak böyle davranırım":  5,
    "Hiç böyle davranmam":            6,
}

# ── Ters puanlı maddeler (7 − ham_puan) ──────────────────────────────────────
# Kaynak: Şahin et al. (1993), data/olcek_yapilari.md
TERS_MADDELER = [1, 2, 3, 4, 9, 13, 14, 15, 17, 21, 22, 25, 26, 29, 30, 32, 34]

# ── Alt boyut madde haritası ──────────────────────────────────────────────────
# PSI 3 faktörü (Heppner & Krauskopf, 1987; Şahin et al., 1993)
# Maddeler 9, 12, 22 dolgu (filler) — toplama dahil, alt boyutlara dahil değil
FAKTÖRLER = {
    "F1_PCG":  [1, 2, 3, 4, 11, 19, 20, 23, 24, 27, 33],         # Problem Çözmeye Güvenme (11 madde)
    "F2_YKS":  [5, 7, 8, 13, 14, 15, 16, 17, 21, 25, 26, 28, 30, 31, 32, 35],  # Yaklaşma-Kaçınma Stili (16 madde)
    "F3_KK":   [6, 10, 18, 29, 34],                                # Kişisel Kontrol (5 madde)
}

FAKTÖR_ETIKET = {
    "F1_PCG":  "Problem Çözmeye Güvenme",
    "F2_YKS":  "Yaklaşma-Kaçınma Stili",
    "F3_KK":   "Kişisel Kontrol",
    "Toplam":  "PÇBÖ Toplam",
}


# ── Yardımcı fonksiyonlar ─────────────────────────────────────────────────────

def yukle_ve_temizle(path: str, isim_ontest: bool) -> pd.DataFrame:
    """Excel'i yükle, madde sütunlarını çıkar, Likert kodla, ters maddeleri düzelt."""
    df = pd.read_excel(path)

    if isim_ontest:
        # Ön test: [0]=zaman, [1-35]=maddeler, [36]=isim, [37]=numara
        madde_cols = df.columns[1:36]
        df["isim"]   = df.iloc[:, 36]
        df["numara"] = df.iloc[:, 37]
    else:
        # Son test: [0]=zaman, [1]=isim, [2]=numara, [3-37]=maddeler
        madde_cols = df.columns[3:38]
        df["isim"]   = df.iloc[:, 1]
        df["numara"] = df.iloc[:, 2]

    # Madde sütunlarını M1..M35 olarak yeniden adlandır
    madde_df = df[madde_cols].copy()
    madde_df.columns = [f"M{i}" for i in range(1, 36)]

    # Likert → sayısal
    madde_df = madde_df.replace(LIKERT_MAP)

    # Sayısal olmayanları NaN yap
    for col in madde_df.columns:
        madde_df[col] = pd.to_numeric(madde_df[col], errors="coerce")

    # Ters maddeleri düzelt
    for m in TERS_MADDELER:
        col = f"M{m}"
        madde_df[col] = 7 - madde_df[col]

    result = pd.DataFrame({
        "isim":   df["isim"].str.strip(),
        "numara": pd.to_numeric(df["numara"], errors="coerce"),
    })
    result = pd.concat([result, madde_df], axis=1)
    return result.dropna(subset=["numara"])


def esle(on: pd.DataFrame, son: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Öğrenci numarasına göre ortak katılımcıları eşleştir."""
    on  = on.drop_duplicates(subset="numara", keep="last")
    son = son.drop_duplicates(subset="numara", keep="last")

    ortak = set(on["numara"].dropna()) & set(son["numara"].dropna())

    on_es  = on[on["numara"].isin(ortak)].sort_values("numara").reset_index(drop=True)
    son_es = son[son["numara"].isin(ortak)].sort_values("numara").reset_index(drop=True)
    return on_es, son_es


def faktor_puanla(df: pd.DataFrame) -> pd.DataFrame:
    """Alt boyut ve toplam madde ortalamasını hesapla (1-6 arası)."""
    madde_cols = [f"M{i}" for i in range(1, 36)]
    for fk, maddeler in FAKTÖRLER.items():
        cols = [f"M{m}" for m in maddeler]
        df[fk] = df[cols].mean(axis=1)
    df["Toplam"] = df[madde_cols].mean(axis=1)
    return df


def cronbach_alpha(df: pd.DataFrame, cols: list) -> float:
    """Cronbach Alpha hesapla."""
    data = df[cols].dropna()
    k = len(cols)
    if k < 2:
        return float("nan")
    item_vars = data.var(axis=0, ddof=1).sum()
    total_var = data.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_vars / total_var)


def guve_analizi(on: pd.DataFrame, son: pd.DataFrame) -> pd.DataFrame:
    """Her alt boyut ve toplam için Cronbach Alpha (ön + son test birleşik)."""
    birlesik = pd.concat([
        on[[f"M{i}" for i in range(1, 36)]],
        son[[f"M{i}" for i in range(1, 36)]]
    ], ignore_index=True)

    rows = []
    for fk, maddeler in FAKTÖRLER.items():
        cols = [f"M{m}" for m in maddeler]
        alpha = cronbach_alpha(birlesik, cols)
        rows.append({
            "Alt Boyut":    FAKTÖR_ETIKET[fk],
            "Madde Sayısı": len(maddeler),
            "Cronbach α":   round(alpha, 3),
        })

    all_cols  = [f"M{i}" for i in range(1, 36)]
    alpha_top = cronbach_alpha(birlesik, all_cols)
    rows.append({"Alt Boyut": "PÇBÖ Toplam", "Madde Sayısı": 35, "Cronbach α": round(alpha_top, 3)})
    return pd.DataFrame(rows)


def tanimlayici(on: pd.DataFrame, son: pd.DataFrame) -> pd.DataFrame:
    """Ön test ve son test için tanımlayıcı istatistikler."""
    boyutlar = list(FAKTÖRLER.keys()) + ["Toplam"]
    rows = []
    for b in boyutlar:
        for label, df in [("Ön Test", on), ("Son Test", son)]:
            rows.append({
                COL_OLCEK:  FAKTÖR_ETIKET[b],
                COL_OLCUM:  label,
                "N":        df[b].count(),
                "Ortalama": round(df[b].mean(), 3),
                "SS":       round(df[b].std(ddof=1), 3),
                "Min":      round(df[b].min(), 2),
                "Max":      round(df[b].max(), 2),
            })
    return pd.DataFrame(rows)


def normallik_testi(on: pd.DataFrame, son: pd.DataFrame) -> pd.DataFrame:
    """Shapiro-Wilk normallik testi (n < 50 için uygun)."""
    boyutlar = list(FAKTÖRLER.keys()) + ["Toplam"]
    rows = []
    for b in boyutlar:
        for label, df in [("Ön Test", on), ("Son Test", son)]:
            data = df[b].dropna()
            stat, p = stats.shapiro(data)
            rows.append({
                COL_OLCEK:        FAKTÖR_ETIKET[b],
                "Ölçüm":          label,
                "N":              len(data),
                "Shapiro-Wilk W": round(stat, 3),
                "p":              round(p, 3),
                "Normal mi?":     "Evet" if p > 0.05 else "Hayır",
            })
    return pd.DataFrame(rows)


def etki_buyuklugu(d: float) -> str:
    if d < 0.2:
        return "Çok küçük"
    elif d < 0.5:
        return "Küçük"
    elif d < 0.8:
        return "Orta"
    else:
        return "Büyük"


def paired_ttest(on: pd.DataFrame, son: pd.DataFrame) -> pd.DataFrame:
    """Bağımlı örneklem t-testi.

    PÇBÖ yönü: düşük ortalama → daha iyi problem çözme.
    t > 0 ve p < .05 → on > son → son testte azalış → gelişim var.
    """
    boyutlar = list(FAKTÖRLER.keys()) + ["Toplam"]
    rows = []
    for b in boyutlar:
        x_on  = on[b].values
        x_son = son[b].values
        # ttest_rel(on, son): t > 0 → on > son → azalış → gelişim
        t, p  = stats.ttest_rel(x_on, x_son)
        n     = len(x_on)
        sd    = n - 1
        fark  = x_on - x_son   # pozitif = azalış = gelişim
        d     = fark.mean() / fark.std(ddof=1)
        rows.append({
            COL_OLCEK:         FAKTÖR_ETIKET[b],
            "Ön x̄":           round(on[b].mean(), 3),
            "Ön SS":           round(on[b].std(ddof=1), 3),
            "Son x̄":          round(son[b].mean(), 3),
            "Son SS":          round(son[b].std(ddof=1), 3),
            "N":               n,
            "sd":              sd,
            "t":               round(t, 3),
            "p":               round(p, 3),
            "p < .05":         "Evet*" if p < 0.05 else "Hayır",
            "Cohen's d":       round(d, 3),
            "Etki Büyüklüğü":  etki_buyuklugu(abs(d)),
        })
    return pd.DataFrame(rows)


# ── Ana fonksiyon ─────────────────────────────────────────────────────────────

def analiz_calistir() -> dict:
    """Tüm analizi çalıştır, sonuçları dict olarak döndür."""
    on_raw  = yukle_ve_temizle(ONTEST_PATH,  isim_ontest=True)
    son_raw = yukle_ve_temizle(SONTEST_PATH, isim_ontest=False)

    on_es, son_es = esle(on_raw, son_raw)

    on_es  = faktor_puanla(on_es)
    son_es = faktor_puanla(son_es)

    return {
        "n_ontest":    len(on_raw),
        "n_sontest":   len(son_raw),
        "n_eslesen":   len(on_es),
        "on_eslesen":  on_es,
        "son_eslesen": son_es,
        "guvenirlik":  guve_analizi(on_es, son_es),
        "tanimlayici": tanimlayici(on_es, son_es),
        "normallik":   normallik_testi(on_es, son_es),
        "ttest":       paired_ttest(on_es, son_es),
    }


if __name__ == "__main__":
    s = analiz_calistir()
    print(f"\nKatılımcı Sayıları:")
    print(f"  Ön test : {s['n_ontest']}")
    print(f"  Son test: {s['n_sontest']}")
    print(f"  Eşlenen : {s['n_eslesen']}")

    print("\n── Güvenirlik ──────────────────────────────────────────")
    print(s["guvenirlik"].to_string(index=False))

    print("\n── Normallik Testi (Shapiro-Wilk) ──────────────────────")
    print(s["normallik"].to_string(index=False))

    print("\n── Paired t-Test Sonuçları ─────────────────────────────")
    print(s["ttest"].to_string(index=False))
    print("\nNot: PÇBÖ'de azalış = gelişim (düşük puan = daha iyi beceri).")
