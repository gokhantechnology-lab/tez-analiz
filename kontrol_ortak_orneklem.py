"""Mevcut veri dosyalarıyla ortak örneklem regresyon kontrolü (kimlik yazdırmaz)."""
import os
from pathlib import Path
import numpy as np
from scipy import stats
import iletisim_analiz as ib
import problem_cozme_analiz as pc


def main():
    os.chdir(Path(__file__).resolve().parent)
    eski_ib = ib.analiz_calistir(ortak_orneklem=False)
    eski_pc = pc.analiz_calistir(ortak_orneklem=False)
    yeni_ib = ib.analiz_calistir()
    yeni_pc = pc.analiz_calistir()
    assert eski_ib['n_eslesen'] == 44 and eski_pc['n_eslesen'] == 40
    referans = set(eski_ib['on_eslesen']['numara']) & set(eski_pc['on_eslesen']['numara'])
    assert len(referans) == 40
    for sonuc in [yeni_ib, yeni_pc]:
        assert sonuc['n_ontest'] == sonuc['n_sontest'] == sonuc['n_eslesen'] == 40
        assert set(sonuc['on_eslesen']['numara']) == referans
        assert sonuc['on_eslesen']['numara'].tolist() == sonuc['son_eslesen']['numara'].tolist()
    assert yeni_ib['on_eslesen']['numara'].tolist() == yeni_pc['on_eslesen']['numara'].tolist()
    assert yeni_pc['ttest'].equals(eski_pc['ttest'])
    # Independent restriction of the prior 44-person frame must reproduce the new communication data.
    for zaman in ['on_eslesen', 'son_eslesen']:
        beklenen = eski_ib[zaman].loc[eski_ib[zaman]['numara'].isin(referans), 'Toplam'].to_numpy()
        np.testing.assert_allclose(beklenen, yeni_ib[zaman]['Toplam'].to_numpy(), rtol=0, atol=0)
    a, b = yeni_ib['on_eslesen']['Toplam'], yeni_ib['son_eslesen']['Toplam']
    t, p = stats.ttest_rel(b, a)
    np.testing.assert_allclose([a.mean(), b.mean(), t, p], [3.828, 3.923, 1.6948287841735274, .09807972550719778], rtol=1e-12)
    assert p > .05
    print('Başarılı: dört ölçümde aynı 40 kişi; PÇBÖ ana sonuçları korundu; İBDÖ ortak grup hesabı doğrulandı.')


if __name__ == '__main__':
    main()
