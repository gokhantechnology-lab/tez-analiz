# İki sürümün karşılaştırması — 13 Kasım 2026

Dayanak: **df3e577** commit’indeki 119 sayfalık Word/PDF. Önceki dosyalar değiştirilmedi.

| Sürüm | Word | PDF |
|---|---|---|
| Özgün, 119 sayfa | [Word](TEZ-OZGUN-119-SAYFA.docx) | [PDF](TEZ-OZGUN-119-SAYFA.pdf) |
| Görselli, 121 sayfa | [Word](TEZ-GORSELLI-13-11-2026.docx) | [PDF](TEZ-GORSELLI-13-11-2026.pdf) |
| Karşılaştırma ve kontrol raporu | [Word](SES-TALEPLERI-VE-KARSILASTIRMALI-KONTROL-RAPORU.docx) | [PDF](SES-TALEPLERI-VE-KARSILASTIRMALI-KONTROL-RAPORU.pdf) |

## Yeni ses kayıtları

11 Kasım 09.32 kaydında danışman; verileri ve mevcut düzeni bozmayan, abartılmayan görsellerin eklenebileceğini, gereksiz tekrardan kaçınılmasını söylüyor. Son aşamada yerleşimi inceleyecek. İki belirli görselin danışman tarafından önceden onaylandığı iddia edilmiyor.

09.33 kaydında ayın yaklaşık **27’si** olası savunma günü olarak konuşuluyor; tarih daha sonra kesinleşecek. Kayıt, kesin randevu veya son tarih yerine geçmez. [Zaman aralıklı otomatik çözüm ve belirsizlik notları](SES-KAYITLARI-COZUMU-11-11-2026.txt).

## Değişiklikler

- Özgün Word/PDF kaynak commit’teki dosyalarla bayt düzeyinde aynı; SHA-256 kayıtları doğrulama dosyasında.
- Görselli sürümde literatür 2.4.2’ye beş aşamalı sade süreç özeti eklendi: **Şekil 2.1, tez s.24 / PDF s.36**. Haftalık uygulama takvimini tekrar etmiyor; mevcut kaynaklar çerçevesinde kavramsal sentez olarak etiketli.
- Bulgular 4.2 sonunda iki ölçeğin ortalama farkları ve %95 güven aralıklarını gösteren tek grafik eklendi: **Şekil 4.1, tez s.57 / PDF s.69**. PÇBÖ: −0,162 [−0,300; −0,024]; İBDÖ: 0,095 [−0,018; 0,208]. Ham puan farkları standartlaştırılmış etki büyüklüğü değildir. İletişim sonucunun anlamlı olmadığı korunuyor.
- İki yeni şekille dizin 24 şekle çıktı. **92 dizin hedefi** kontrol edildi ve sayfa numaraları güncellendi.
- Kısa tabloların satırları birlikte tutuldu. Birleştirilmiş hücreler fiziksel satır düzeninde kontrol edildi.
- **Tablo 3.3**, font küçültülmeden, tablo içi satır/paragraf boşlukları düzenlenerek **tez s.49 / PDF s.61’de tek sayfaya** alındı. 18 grup kaydı ve bütün hücreler aynı.
- Giriş, tartışma ve kaynakça birebir aynı. Özgün ana metnin **528 dolu paragrafı**, **23 tablonun hücre içerikleri** ve kaynak görseller korunuyor. Altı yeni paragraf ve iki görsel var; veri/puanlama değişikliği yok.

## Uzun tablolar: kılavuzun açık hükmü

Kaynak: kullanıcı tarafından paylaşılan **Tez Yazım Kılavuzu**, **3.7 “Tablo Oluşturma”**, **basılı/PDF sayfa 27**:

> Tablolar bölünmemelidir.

Aynı maddenin s.26 açıklaması, gerektiğinde tablo yazısının en fazla 8 puntoya kadar küçültülebileceğini söylüyor. Bu alt sınır bir küçültme hedefi olarak kullanılmadı. Kullanıcının okunabilirlik talebi esas alındı.

Görselli sürümde Tablo 3.3 ve kısa tablolar tek sayfada. **Ek 1’deki ölçek tablosu PDF s.93–94, Ek 2’deki ölçek tablosu s.95–97, Ek 4’teki 53 satırlık kod kitabı s.99–101** arasında sürüyor. Bu üç tabloda mevcut **10,5 punto** ve bütün içerik korunuyor; başlıklar tekrarlanıyor, satırlar bölünmeye karşı korunuyor. Çok sayfalı uzun tabloların **3.7 maddesine katı anlamda tam uyum sağladığı iddia edilmez**. Okunurluğu bozacak biçimde küçültme veya içerik silme yapılmadı. Nihai kabul, danışman/enstitü kontrolüne açık.

## Kontrollerin sınırı

Son PDF’de boş sayfa veya sayfa dışına çıkan sözcük bulunmadı. Yeni şekiller ve etkilenen tablo/ek sayfaları görüntü olarak incelendi. PDF LibreOffice ile üretildi; **gerçek Microsoft Word görünümü**, **etik/izin/onam ekleri**, **güncel benzerlik raporu** ve **kesin savunma takvimi** tamamlanmış sayılmıyor. Puanlama konusu yeniden açılmadı; önceki gerçek SPSS kontrolü korunuyor.
