"""İki ölçeğin ön/son testleri için aynı, eksiksiz katılımcı kümesi.

25 Ekim 2026 danışman geri bildirimi: sayı eşitlemek için kişi seçilmez;
dört veri kaynağının öğrenci numarası kesişimi kullanılır. Kimlikler yazdırılmaz.
"""
from pathlib import Path
import importlib

ROOT = Path(__file__).resolve().parent


def ortak_numaralari_bul():
    """Son yinelenen kayıt korunur; tüm madde yanıtları geçerli olmalıdır."""
    kumeler = []
    for name, madde_sayisi, en_yuksek in [
        ('iletisim_analiz', 25, 5), ('problem_cozme_analiz', 35, 6)
    ]:
        mod = importlib.import_module(name)
        for path, ontest in [(mod.ONTEST_PATH, True), (mod.SONTEST_PATH, False)]:
            df = mod.yukle_ve_temizle(str(ROOT / path), ontest)
            df = df.drop_duplicates('numara', keep='last')
            cols = [f'M{i}' for i in range(1, madde_sayisi + 1)]
            valid = df[cols].notna().all(axis=1) & df[cols].ge(1).all(axis=1) & df[cols].le(en_yuksek).all(axis=1)
            kumeler.append(set(df.loc[valid, 'numara']))
    return set.intersection(*kumeler)


def fark_tanilari(on, son, etiketler):
    """Eşleştirilmiş son−ön farklarının Shapiro ve çift yönlü Wilcoxon incelemesi."""
    import numpy as np
    import pandas as pd
    from scipy import stats
    rows = []
    for key, label in etiketler.items():
        delta = (son[key] - on[key]).to_numpy()
        w, p = stats.shapiro(delta)
        # 12 basamak yalnızca kayan nokta farklarının sahte sıralarını önler.
        wil = stats.wilcoxon(np.round(delta, 12), zero_method='wilcox', method='approx')
        rows.append({'Alt Boyut': label, 'N': len(delta), 'Ortalama fark': float(delta.mean()),
                     'Fark SS': float(delta.std(ddof=1)), 'Shapiro-Wilk W': float(w),
                     'Shapiro p': float(p), 'Wilcoxon W': float(wil.statistic),
                     'Wilcoxon p': float(wil.pvalue), 'Fark yönü': 'Son − Ön'})
    return pd.DataFrame(rows)
