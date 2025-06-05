# Python Sözdizimi Vurgulayıcı ve Kod Editörü

Python dili alt kümesi için gerçek zamanlı gramer tabanlı sözdizimi vurgulayıcı. Gelişmiş GUI yetenekleri, sözcüksel analiz, ayrıştırma, parantez eşleştirme, otomatik tamamlama ve tema özelleştirme sunar.

## 🚀 Özellikler

### Temel Fonksiyonlar
* **Gerçek Zamanlı Sözdizimi Vurgulaması**: Yazarken anlık kod renklendirme
  * **Anahtar Kelimeler**: `if`, `else`, `elif`, `while`, `for`, `in`, `def`, `class`, `return`, `break`, `continue`, `and`, `or`, `not`, `try`, `except`, `finally`, `raise`, `import`, `from`, `as`, `with`, `lambda`, `global`, `nonlocal`, `pass`, `del`, `yield`, `assert`, `async`, `await`, `match`, `case`
  * **Yerleşik Fonksiyonlar**: `print`, `input`, `len`, `str`, `int`, `float`, `list`, `dict`, `tuple`, `set`, `range`, `True`, `False`, `None`
  * **Operatörler**: Aritmetik (`+`, `-`, `*`, `/`), karşılaştırma (`==`, `!=`, `<`, `>`), atama (`=`)
  * **Veri Türleri**: Sayılar (`123`, `3.14`), kaçış dizili stringler, tanımlayıcılar
  * **Ayırıcılar**: Parantezler `()`, köşeli parantezler `[]`, süslü parantezler `{}`, iki nokta `:`, virgül `,`
  * **Yorumlar**: Tek satırlık yorumlar (`# yorum`)

### Gelişmiş Özellikler
* **Sözcüksel Analiz**: Kapsamlı hata tespiti ile regex tabanlı tokenizer
* **Sözdizimi Ayrıştırma**: Python gramer alt kümesi için yukarıdan aşağı özyinelemeli iniş ayrıştırıcı
* **Akıllı Parantez Eşleştirme**: Gerçek zamanlı eşleştirme ve uyumsuzluk vurgulaması
* **Otomatik Kod Tamamlama**: Anahtar kelimeler ve yerleşik fonksiyonlar için bağlam duyarlı öneriler
* **Satır Numaraları**: Kod içeriği ile senkronize edilmiş satır numaralandırma
* **Kod Çalıştırma**: Çıktı görüntüleme ile yerleşik Python yorumlayıcı
* **Tema Sistemi**: Tam UI tutarlılığı ile açık/koyu tema değiştirme
* **Hata Tespiti**: Kesin konum ile gerçek zamanlı sözcüksel ve sözdizimi hata raporlaması

### Desteklenen Python Yapıları
- Değişken atamaları ve ifadeler
- Kontrol yapıları (`if/elif/else`, `while`, `for...in`)
- Fonksiyon tanımları (`def`) ve sınıf tanımları (`class`)
- İstisna yönetimi (`try/except/finally`, `raise`)
- Desen eşleştirme (`match/case`)
- Liste değişmezleri ve karmaşık ifadeler
- Yorumlar ve kaçış dizili string değişmezleri

## 📁 Proje Klasör Yapısı
```
python-highlighter/
├── src/
│   ├── main.py              # Ana uygulama ve GUI kontrolcüsü
│   ├── highlighter.py       # Sözdizimi vurgulama motoru ve tema yöneticisi
│   ├── lexer.py            # Sözcüksel analizci (tokenizer)
│   └── parser.py           # Sözdizimi ayrıştırıcı (özyinelemeli iniş)
├── documentation.md         # Teknik uygulama detayları
├── grammar.bnf             # Biçimsel gramer tanımı (BNF formatı)
├── tokens.txt              # Token türü tanımları ve desenleri
└── README.md               # Bu dosya
```

## 🔧 Teknik Uygulama

### Sözcüksel Analiz
- **Yöntem**: Biçimsel Tanımlama ve Tablo Tabanlı Analizci
- **Yaklaşım**: Verimli tokenizasyon için regex tabanlı desen eşleştirme
- **Özellikler**: Geçersiz karakter tespiti, kapatılmamış string işleme, detaylı hata raporlaması

### Ayrıştırma Stratejisi
- **Yöntem**: Yukarıdan Aşağı Özyinelemeli İniş Ayrıştırıcı
- **Gramer**: Python'un bağlamdan bağımsız gramer alt kümesi
- **Avantajlar**: Sezgisel uygulama, kesin hata kontrolü, kolay genişletilebilirlik

### Gerçek Zamanlı İşleme
- **Performans**: Optimize edilmiş regex derleme ve artımlı işleme
- **Yanıt Verme**: `after_idle` zamanlaması kullanarak engellenmeyen GUI güncellemeleri
- **Bellek**: Verimli token önbelleğe alma ve seçici yeniden ayrıştırma

## 🎨 Kullanıcı Arayüzü

### Editör Özellikleri
- **Kod Alanı**: Gerçek zamanlı geri bildirim ile sözdizimi vurgulı metin editörü
- **Satır Numaraları**: İçerik ile senkronize otomatik güncelenen satır sayacı
- **Hata Paneli**: Satır/sütun bilgisi ile detaylı hata mesajları
- **Çıktı Konsolu**: Sonuç görüntüleme ile entegre Python çalıştırma

### Kontroller
- **Kodu Çalıştır**: Çıktı yakalama ile Python kodu çalıştırma
- **Tema Değiştir**: Açık ve koyu temalar arasında geçiş
- **Otomatik Tamamlama**: Tab/Enter ile tamamlama, Escape ile kapatma
- **Parantez Eşleştirme**: İmlecin yanındaki parantezlerin otomatik eşleştirilmesi

### Görsel Tasarım
- **Açık Tema**: Gündüz kodlama için temiz, profesyonel görünüm
- **Koyu Tema**: Uzun süreli oturumlar için göz dostu karanlık arayüz
- **Renk Kodlaması**: Tüm temalarda tutarlı token renklendirmesi

## 🚀 Kurulum ve Kullanım

### Gereksinimler
- Python 3.7+ (Tkinter dahil)

### Hızlı Başlangıç
1. **Proje dosyalarını** yerel dizininize klonlayın veya indirin
2. **Uygulamayı çalıştırın**:
   ```bash
   python src/main.py
   ```
3. **Kodlamaya başlayın** - sözdizimi vurgulaması otomatik olarak etkinleşir
4. **Özellikleri kullanın**:
   - Anlık vurgulama için Python kodu yazın
   - Otomatik tamamlama önerileri için Tab'a basın
   - Çalıştırma ve çıktı görmek için "Kodu Çalıştır"a tıklayın
   - "Tema Değiştir" butonu ile temaları değiştirin

### Örnek Kod
```python
# Editörde bu örneği deneyin
def fibonacci(n):
    try:
        if n <= 1:
            return n
        else:
            return fibonacci(n-1) + fibonacci(n-2)
    except RecursionError:
        print("Çok derin özyineleme")
        return None
    finally:
        print(f"fibonacci({n}) hesaplandı")

# Fonksiyonu test et
sonuc = fibonacci(10)
print(f"Sonuç: {sonuc}")
```

## 📄 Proje Makalesi

### Gerçek Zamanlı Python Sözdizimi Vurgulayıcı: Gramer Tabanlı Yaklaşım

#### Özet
Bu proje, biçimsel gramer analizi ve sözcüksel tokenizasyon kullanarak Python için kapsamlı bir sözdizimi vurgulayıcı uygular. Sistem, sezgisel GUI arayüzü aracılığıyla gerçek zamanlı kod analizi, hata tespiti ve görsel geri bildirim sağlar.

#### Teknik Mimari
Vurgulayıcı iki aşamalı analiz süreci kullanır:

1. **Sözcüksel Analiz Aşaması**
   - Biçimsel tanımlama metodolojisini takip eden regex tabanlı tokenizasyon
   - Kapsamlı token sınıflandırması (15+ token türü)
   - Geçersiz karakterler ve hatalı stringler için hata tespiti
   - Derlenmiş regex optimizasyonu ile verimli desen eşleştirme

2. **Sözdizimi Analiz Aşaması**
   - Yukarıdan aşağı özyinelemeli iniş ayrıştırma
   - Python alt kümesi için bağlamdan bağımsız gramer uygulaması
   - Kesin konum takibi ile gerçek zamanlı hata raporlaması
   - Karmaşık iç içe yapılar ve kontrol akışı desteği

#### Uygulama Öne Çıkanları
- **Performans Optimizasyonu**: Artımlı ayrıştırma ve seçici yeniden vurgulama
- **Kullanıcı Deneyimi**: Yanıt veren GUI ile engellenmeyen gerçek zamanlı güncellemeler
- **Genişletilebilirlik**: Kolay özellik ekleme sağlayan modüler tasarım
- **Sağlamlık**: Kapsamlı hata işleme ve zarif bozulma

#### Sonuçlar ve Etki
Vurgulayıcı, Python kodunu saniyenin altında yanıt süreleri ile başarıyla işler, geliştiricilere anında görsel geri bildirim ve hata tespiti sağlar. Kullanıcı testleri, kod okunabilirliği ve geliştirme verimliliğinde önemli iyileşme gösterir.
---

## 📋 Gereksinim Uygunluğu

✅ **Programlama Dili**: Python seçildi ve uygulandı  
✅ **Sözcüksel Analiz**: Biçimsel Tanımlama ve Tablo Tabanlı Analizci yöntemi  
✅ **Ayrıştırıcı Uygulaması**: Yukarıdan Aşağı Özyinelemeli İniş yaklaşımı  
✅ **Token Vurgulaması**: Gerçek zamanlı renklendirme ile 15+ farklı token türü  
✅ **GUI Arayüzü**: Yanıt veren tasarım ile tam özellikli Tkinter uygulaması  
✅ **Gerçek Zamanlı Güncellemeler**: Anında geri bildirim ve sürekli analiz  
✅ **Dokümantasyon**: Kapsamlı teknik ve kullanıcı dokümantasyonu  


## 🎮 Gelişmiş Özellikler

### Parantez Eşleştirme Sistemi
- **Akıllı Tespiti**: İmleç parantez yakınındayken otomatik eşleştirme
- **Görsel Geri Bildirim**: Eşleşen parantezleri renklendirme
- **Hata Gösterimi**: Uyumsuz parantezleri farklı renkte vurgulama
- **Desteklenen Türler**: `()`, `[]`, `{}` parantez türleri

### Otomatik Kod Tamamlama
- **Akıllı Öneriler**: Minimum 2 karakter sonrası aktivasyon
- **Kapsam**: Python anahtar kelimeleri ve yerleşik fonksiyonlar
- **Kullanım**: Tab/Enter ile kabul, Escape ile iptal
- **Performans**: Hızlı filtreleme ve görüntüleme

### Tema Yönetimi
- **Çift Tema**: Açık ve koyu mod desteği
- **Tutarlılık**: Tüm UI bileşenlerinde uyumlu renklendirme
- **Geçiş**: Tek tıkla tema değiştirme
- **Özelleştirme**: Her token türü için özel renk tanımları

### Kod Çalıştırma Motoru
- **Yerleşik Yorumlayıcı**: Python kodu doğrudan editörde çalıştırma
- **Çıktı Yakalama**: Standart çıktı ve hata mesajlarını görüntüleme
- **Güvenlik**: Kontrollü çalıştırma ortamı
- **Geri Bildirim**: Çalıştırma durumu ve sonuç gösterimi

---

**Geliştirici**: Programlama Dilleri dersi projesi kapsamında geliştirildi  
**Lisans**: Açık kaynak eğitim projesi

## 📚 makale ve video

**📰 Makale:** [Python Sözdizimi Vurgulayıcı Yapmak - Sıfırdan Kod Editörü]([medium-link](https://medium.com/@ahyil.fb/python-i%C3%A7in-ger%C3%A7ek-zamanl%C4%B1-s%C3%B6zdizimi-vurgulay%C4%B1c%C4%B1-yapmak-derleyici-teorisinden-prati%C4%9Fe-51d11502f4d8))

**🎥 Video:** [Kendi Kod Editörümü Yaptım! VS Code Nasıl Çalışır?]([youtube-link](https://youtu.be/E4HlKmfrdbM))
