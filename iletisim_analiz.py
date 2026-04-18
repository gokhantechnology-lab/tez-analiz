"""
İletişim Becerileri Ölçeği (İBDÖ) - Ön Test / Son Test Analizi
Kaynak: Korkut Owen & Bugay (2014)
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

COL_OLCEK  = "Ölçek / Alt Boyut"
COL_OLCUM  = "Ölçüm"

# ── Dosya yolları ─────────────────────────────────────────────────────────────
ONTEST_PATH  = "data/İletişim_Becerileri/öntest/İBDÖ - Ön test - Yanıtlar adlı dosyanın kopyası.xlsx"
SONTEST_PATH = "data/İletişim_Becerileri/sontest/İBDÖ - Son test - Cevaplar adlı dosyanın kopyası.xlsx"

# ── Likert → sayısal ──────────────────────────────────────────────────────────
LIKERT_MAP = {
    "Hiçbir zaman": 1,
    "Nadiren":       2,
    "Bazen":         3,
    "Sık sık":       4,
    "Her zaman":     5,
}

# ── Alt boyut madde haritası (Excel sütun sırası 1-25) ───────────────────────
# Kaynak: Korkut Owen & Bugay (2014), Tablo 2
FAKTÖRLER = {
    "F1_İİTB": [1, 3, 6, 13, 15, 16, 21, 23, 24, 25],   # İletişim İlkeleri ve Temel Beceriler
    "F2_KİE":  [2, 5, 17, 20],                            # Kendini İfade Etme
    "F3_EDSÖİ":[10, 11, 12, 18, 19, 22],                  # Etkin Dinleme ve Sözel Olmayan İletişim
    "F4_İKİ":  [4, 7, 8, 9, 14],                          # İletişim Kurmaya İsteklilik
}

FAKTÖR_ETIKET = {
    "F1_İİTB":  "İletişim İlkeleri ve Temel Beceriler",
    "F2_KİE":   "Kendini İfade Etme",
    "F3_EDSÖİ": "Etkin Dinleme ve Sözel Olmayan İletişim",
    "F4_İKİ":   "İletişim Kurmaya İsteklilik",
    "Toplam":   "İBDÖ Toplam",
}


# ── Yardımcı fonksiyonlar ─────────────────────────────────────────────────────

def yukle_ve_temizle(path: str, isim_ontest: bool) -> pd.DataFrame:
    """Excel'i yükle, madde sütunlarını çıkar, Likert kodla, isim/numara ekle."""
    df = pd.read_excel(path)

    if isim_ontest:
        # Ön testte: [0]=zaman, [1-25]=maddeler, [26]=isim, [27]=numara, [28]=email
        madde_cols = df.columns[1:26]
        df["isim"]   = df.iloc[:, 26]
        df["numara"] = df.iloc[:, 27]
    else:
        # Son testte: [0]=zaman, [1]=isim, [2]=numara, [3-27]=maddeler
        madde_cols = df.columns[3:28]
        df["isim"]   = df.iloc[:, 1]
        df["numara"] = df.iloc[:, 2]

    # Madde sütunlarını M1..M25 olarak yeniden adlandır
    madde_df = df[madde_cols].copy()
    madde_df.columns = [f"M{i}" for i in range(1, 26)]

    # Likert → sayısal
    madde_df = madde_df.replace(LIKERT_MAP)

    # Sayısal olmayanları NaN yap
    for col in madde_df.columns:
        madde_df[col] = pd.to_numeric(madde_df[col], errors="coerce")

    result = pd.DataFrame({
        "isim":   df["isim"].str.strip(),
        "numara": pd.to_numeric(df["numara"], errors="coerce"),
    })
    result = pd.concat([result, madde_df], axis=1)
    return result.dropna(subset=["numara"])


def esle(on: pd.DataFrame, son: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Öğrenci numarasına göre ortak katılımcıları eşleştir.
    Tekrar eden numara varsa son girişi al."""
    on  = on.drop_duplicates(subset="numara", keep="last")
    son = son.drop_duplicates(subset="numara", keep="last")

    ortak = set(on["numara"].dropna()) & set(son["numara"].dropna())

    on_es  = on[on["numara"].isin(ortak)].sort_values("numara").reset_index(drop=True)
    son_es = son[son["numara"].isin(ortak)].sort_values("numara").reset_index(drop=True)
    return on_es, son_es


def faktor_puanla(df: pd.DataFrame) -> pd.DataFrame:
    """Alt boyut ve toplam puanları hesapla."""
    madde_cols = [f"M{i}" for i in range(1, 26)]
    for fk, maddeler in FAKTÖRLER.items():
        cols = [f"M{m}" for m in maddeler]
        df[fk] = df[cols].mean(axis=1)  # madde ortalaması (1-5 arası)
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
        on[[f"M{i}" for i in range(1, 26)]],
        son[[f"M{i}" for i in range(1, 26)]]
    ], ignore_index=True)

    rows = []
    for fk, maddeler in FAKTÖRLER.items():
        cols = [f"M{m}" for m in maddeler]
        alpha = cronbach_alpha(birlesik, cols)
        rows.append({"Alt Boyut": FAKTÖR_ETIKET[fk], "Madde Sayısı": len(maddeler), "Cronbach α": round(alpha, 3)})

    all_cols = [f"M{i}" for i in range(1, 26)]
    alpha_top = cronbach_alpha(birlesik, all_cols)
    rows.append({"Alt Boyut": "İBDÖ Toplam", "Madde Sayısı": 25, "Cronbach α": round(alpha_top, 3)})
    return pd.DataFrame(rows)


def tanimlayici(on: pd.DataFrame, son: pd.DataFrame) -> pd.DataFrame:
    """Ön test ve son test için tanımlayıcı istatistikler."""
    boyutlar = list(FAKTÖRLER.keys()) + ["Toplam"]
    rows = []
    for b in boyutlar:
        rows.append({
            COL_OLCEK: FAKTÖR_ETIKET[b],
            COL_OLCUM: "Ön Test",
            "N": on[b].count(),
            "Ortalama": round(on[b].mean(), 3),
            "SS": round(on[b].std(ddof=1), 3),
            "Min": round(on[b].min(), 2),
            "Max": round(on[b].max(), 2),
        })
        rows.append({
            COL_OLCEK: FAKTÖR_ETIKET[b],
            COL_OLCUM: "Son Test",
            "N": son[b].count(),
            "Ortalama": round(son[b].mean(), 3),
            "SS": round(son[b].std(ddof=1), 3),
            "Min": round(son[b].min(), 2),
            "Max": round(son[b].max(), 2),
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
                COL_OLCEK: FAKTÖR_ETIKET[b],
                "Ölçüm": label,
                "N": len(data),
                "Shapiro-Wilk W": round(stat, 3),
                "p": round(p, 3),
                "Normal mi?": "Evet" if p > 0.05 else "Hayır",
            })
    return pd.DataFrame(rows)


def paired_ttest(on: pd.DataFrame, son: pd.DataFrame) -> pd.DataFrame:
    """Bağımlı örneklem t-testi (Paired Samples t-test)."""
    boyutlar = list(FAKTÖRLER.keys()) + ["Toplam"]
    rows = []
    for b in boyutlar:
        x_on  = on[b].values
        x_son = son[b].values
        t, p  = stats.ttest_rel(x_son, x_on)
        n     = len(x_on)
        sd    = n - 1
        # Cohen's d
        fark  = x_son - x_on
        d     = fark.mean() / fark.std(ddof=1)
        rows.append({
            COL_OLCEK:  FAKTÖR_ETIKET[b],
            "Ön x̄":   round(on[b].mean(), 3),
            "Ön SS":   round(on[b].std(ddof=1), 3),
            "Son x̄":  round(son[b].mean(), 3),
            "Son SS":  round(son[b].std(ddof=1), 3),
            "N": n,
            "sd": sd,
            "t": round(t, 3),
            "p": round(p, 3),
            "p < .05": "Evet*" if p < 0.05 else "Hayır",
            "Cohen's d": round(d, 3),
            "Etki Büyüklüğü": etki_buyuklugu(abs(d)),
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


# ── Ana fonksiyon ─────────────────────────────────────────────────────────────

def analiz_calistir() -> dict:
    """Tüm analizi çalıştır, sonuçları dict olarak döndür."""

    # 1. Veri yükleme
    on_raw  = yukle_ve_temizle(ONTEST_PATH,  isim_ontest=True)
    son_raw = yukle_ve_temizle(SONTEST_PATH, isim_ontest=False)

    # 2. Eşleştirme
    on_es, son_es = esle(on_raw, son_raw)

    # 3. Alt boyut puanları
    on_es  = faktor_puanla(on_es)
    son_es = faktor_puanla(son_es)

    # 4. Analizler
    sonuclar = {
        "n_ontest":   len(on_raw),
        "n_sontest":  len(son_raw),
        "n_eslesen":  len(on_es),
        "on_eslesen":  on_es,
        "son_eslesen": son_es,
        "guvenirlik":  guve_analizi(on_es, son_es),
        "tanimlayici": tanimlayici(on_es, son_es),
        "normallik":   normallik_testi(on_es, son_es),
        "ttest":       paired_ttest(on_es, son_es),
    }
    return sonuclar


if __name__ == "__main__":
    s = analiz_calistir()
    print(f"\nKatılımcı Sayıları:")
    print(f"  Ön test : {s['n_ontest']}")
    print(f"  Son test: {s['n_sontest']}")
    print(f"  Eşlenen : {s['n_eslesen']}")

    print("\n── Güvenirlik ──────────────────────────────────")
    print(s["guvenirlik"].to_string(index=False))

    print("\n── Normallik Testi (Shapiro-Wilk) ──────────────")
    print(s["normallik"].to_string(index=False))

    print("\n── Paired t-Test Sonuçları ─────────────────────")
    print(s["ttest"].to_string(index=False))
