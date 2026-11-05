# SPSS kullanım paketi — 5 Kasım 2026

**[Veri dahil şifreli tam paket](SPSS-TAM-PAKET-SIFRELI.zip)** — AES-256 ZIP; parola sohbet üzerinden ayrıca paylaşılır. WinRAR veya 7-Zip ile çıkarın. Şifreli pakette isim ve öğrenci numarası bulunmayan 40 kişilik veri vardır; açık CSV yayımlanmaz.


[Adım adım Word](SPSS-ADIM-ADIM-KULLANIM.docx) · [PDF](SPSS-ADIM-ADIM-KULLANIM.pdf) · [Kılavuz ve komutlar ZIP](SPSS-KILAVUZ-VE-KOMUTLAR.zip)

1. Windows’ta `C:/TEZ_SPSS` oluşturun; komut dosyalarını ve yerel verilen `SPSS-DOGRULAMA-VERISI.csv` dosyasını içine koyun.
2. SPSS’te **File → Open → Syntax** ile [00_VERIYI_AC.sps](00_VERIYI_AC.sps) açın, **Run → All** seçin. `TEZ40.sav` oluşur.
3. Aynı menüyle [01_ILETISIM_ANALIZLERI.sps](01_ILETISIM_ANALIZLERI.sps) çalıştırın.
4. Output’u `.spv` olarak kaydedin.

[02_PC_MEVCUT_PUANLAMA_KONTROLU_BEKLET.sps](02_PC_MEVCUT_PUANLAMA_KONTROLU_BEKLET.sps) mevcut puanlama tekrarıdır; **PÇBÖ yetkili anahtarı teyit beklediği için şimdilik çalıştırmayın.**

Kimliksiz CSV yalnız şifreli tam paketin içindedir. Kılavuz ve komutlar ZIP’i ise veri içermez. 40 satır/148 değişken beklenir. Komutlar gerçek SPSS’te henüz çalıştırılmamıştır. [Karşılaştırma değerleri](KARSILASTIRMA-DEGERLERI.json) SPSS çıktısı değildir.

Resmî ürün: [IBM SPSS Statistics](https://www.ibm.com/products/spss-statistics). Lisans, IBM hesabı ve kurulum araştırmacıya aittir; şifre paylaşılması gerekmez.
