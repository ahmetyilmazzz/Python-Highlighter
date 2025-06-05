# Python Sözdizimi Vurgulayıcı ve Kod Editörü - Teknik Dokümantasyon

## 1. Giriş

Bu doküman, Python programlama dilinin bir alt kümesi için geliştirilmiş gerçek zamanlı, gramer tabanlı bir sözdizimi vurgulayıcı ve kod editörünün teknik detaylarını açıklamaktadır. 

Proje aşağıdaki bileşenleri içerir:
- Sözcüksel analizci (lexer)
- Sözdizimsel analizci (parser)
- Kullanıcı etkileşimi için Grafiksel Kullanıcı Arayüzü (GUI)

### Temel Özellikler
- Yazım sırasında anlık kod renklendirmesi
- Hata tespiti
- Parantez eşleştirme
- Otomatik tamamlama
- Tema yönetimi

**Temel Amaç:** Biçimsel bir gramere dayalı sözdizimi analizi yaparak en az 15 farklı token türünü gerçek zamanlı olarak vurgulayabilen bir GUI geliştirmek.

## 2. Kullanılan Programlama Dili

Proje **Python 3.7+** kullanılarak geliştirilmiştir.

### Kullanılan Modüller
- **Tkinter:** GUI geliştirme
- **re:** Düzenli ifadeler

## 3. Sözdizimi Analiz Süreci

Sözdizimi analizi iki ana aşamadan oluşur:

### 3.1. Sözcüksel Analiz (Lexical Analysis)

#### 3.1.1. Seçilen Yöntem
Biçimsel tanımlama ve düzenli ifadeler tabanlı bir analizci uygulanmıştır. Token tanımları, düzenli ifadeler listesi (`token_specs`) olarak belirtilmiştir.

#### 3.1.2. Uygulama (`lexer.py`)

`lexer.py` dosyası, sözcüksel analizciyi içerir:

- Token tanımları, `re` modülü ile düzenli ifadeler olarak tanımlanmıştır (`token_specs`)
- Tüm token türleri için tek bir regex ifadesi `re.compile()` ile derlenir ve `finditer` ile kod taranır
- Her token için türü, değeri ve satır/sütun pozisyonu hesaplanır (`get_line_column`)

#### 3.1.3. Token Türleri

Sistem aşağıdaki **15 token türünü** tanır ve vurgular:

| Token Türü | Açıklama | Örnekler |
|------------|----------|----------|
| `KEYWORD` | Anahtar kelimeler | `if`, `else`, `def`, `class`, `try` |
| `BUILTIN` | Yerleşik fonksiyonlar | `print`, `len`, `range`, `True`, `False` |
| `IDENTIFIER` | Değişken ve fonksiyon adları | `x`, `my_function` |
| `OPERATOR` | İşleçler | `+`, `-`, `*`, `/`, `==`, `!=` |
| `ASSIGN` | Atama işleci | `=` |
| `NUMBER` | Sayılar | `123`, `3.14` |
| `STRING` | String değişmezleri | `"hello"`, `'world'` |
| `STRING_QUOTE` | String tırnakları | `"`, `'` |
| `STRING_CONTENT` | String içeriği | `hello` |
| `ESCAPE_CHAR` | Kaçış karakterleri | `\n`, `\t`, `\\"` |
| `COLON` | İki nokta | `:` |
| `LPAREN/RPAREN` | Parantezler | `(`, `)` |
| `COMMA` | Virgül | `,` |
| `LBRACKET/RBRACKET` | Köşeli parantezler | `[`, `]` |
| `COMMENT` | Yorumlar | `# yorum` |

> **Not:** `WHITESPACE` ve `NEWLINE` token'ları analizde kullanılır ancak vurgulanmaz.

#### 3.1.4. Hata Yönetimi

- **Geçersiz Karakterler:** Tanımlı token'lara uymayan karakterler için `ValueError` fırlatılır
  - Örnek: `"Invalid character '@' at line 1, column 5"`
- **Kapatılmamış String'ler:** String'in son tırnağı eksikse `ValueError` fırlatılır  
  - Örnek: `"Unclosed string literal at line 1, column 10"`

#### 3.1.5. Özel String Analizi

`tokenize_with_escape_highlighting` metodu, string değişmezlerini şu şekilde ayrıştırır:

1. **Tırnaklar** (`STRING_QUOTE`)
2. **İçerik** (`STRING_CONTENT`) 
3. **Kaçış karakterleri** (`ESCAPE_CHAR`)

Bu, string bileşenlerinin farklı renklerle vurgulanmasını sağlar.

### 3.2. Sözdizimsel Analiz (Parsing)

#### 3.2.1. Seçilen Yöntem
**Yukarıdan aşağıya özyinelemeli iniş ayrıştırıcısı** (Recursive Descent Parser) kullanılmıştır. Her gramer kuralı için ayrı bir fonksiyon tanımlanmıştır.

#### 3.2.2. Uygulama (`parser.py`)

`parser.py` dosyası, özyinelemeli iniş ayrıştırıcısını içerir:

- Token listesini alır ve `parse_program` ile başlar
- Her kural için bir `parse_*` metodu bulunur
- Sözdizimi ağacı, liste içinde demetler olarak saklanır (`self.tree`)
- Ağaç, GUI'de Treeview ile görselleştirilir (`populate_treeview`)

#### 3.2.3. Gramer

Desteklenen Python yapılarının bağlamdan bağımsız gramer kuralları `parser.py` içindeki metodlarla tanımlanmıştır.

**Başlıca yapılar:**
- Program yapısı
- Atama ifadeleri (`x = 5`)
- Kontrol yapıları (`if/elif/else`, `while`, `for`)
- Fonksiyon (`def`) ve sınıf (`class`) tanımları
- `return`, `try/except/finally`, `raise`, `match/case` ifadeleri
- Aritmetik, mantıksal ve karşılaştırma ifadeleri
- Liste değişmezleri (`[1, 2, 3]`), fonksiyon çağrıları
- Sabitler (`True`, `False`, `None`)

#### 3.2.4. Desteklenen Python Yapıları

Ayrıştırıcı aşağıdaki yapıları destekler:

```python
# Değişken atamaları
x = 5

# İfadeler
result = x + y
condition = x > 5 and y < 10

# Kontrol yapıları
if condition:
    print("True")
elif x == 0:
    print("Zero")
else:
    print("False")

# Döngüler
for i in range(10):
    print(i)

# Fonksiyonlar
def my_function():
    return 42

# Sınıflar
class MyClass:
    pass

# İstisna yönetimi
try:
    risky_operation()
except ValueError:
    handle_error()
finally:
    cleanup()
```

#### 3.2.5. Hata Yönetimi

- Sözdizimi hatalarında `SyntaxError` fırlatılır
- Hata mesajları beklenen token, bulunan token ve konum bilgisini içerir
- Örnek: `"':' expected at line 1, column 10"`

#### 3.2.6. İstisna Yönetimi Yapıları

**Lexer Güncellemeleri:** `try`, `except`, `finally`, `raise` anahtar kelimeleri eklendi.

**Gramer kuralları:**
```bnf
<try_statement> ::= "try" ":" <statement> <except_clause> ["finally" ":" <statement>]
<except_clause> ::= "except" [IDENTIFIER] ":" <statement> [<except_clause>]
<raise_statement> ::= "raise" [<expression>]
```

**Parser metodları:**
- `parse_try_statement`: try, except ve finally bloklarını işler
- `parse_except_clause`: İsteğe bağlı hata türüyle except bloklarını özyinelemeli işler
- `parse_raise_statement`: raise ifadeleri ve isteğe bağlı hata nesnelerini işler

#### 3.2.7. Ayrıştırma Ağacı

Ayrıştırıcı, kodun yapısını temsil eden bir ağaç oluşturur ve bunu GUI'de "Ağaç Yapısı" sekmesinde görselleştirir. Her düğüm türü, detayı ve açıklamasını içerir (`GRAMMAR_INFO`).

## 4. Vurgulama Şeması (`highlighter.py`)

`highlighter.py`, sözdizimi vurgulama, tema yönetimi, parantez eşleştirme ve otomatik tamamlama özelliklerini içerir.

### 4.1. Gerçek Zamanlı Mekanizma

Kullanıcı yazarken veya metni değiştirdiğinde (`<KeyRelease>`, `<Button-1>`, `<Control-v>` vb.), `schedule_highlight` 100 ms gecikmeyle vurgulamayı tetikler.

**`highlight` metodu:**
1. Kodu alır, değişip değişmediğini kontrol eder (`last_code`)
2. Önceki etiketleri temizler (`clear_syntax_tags`)
3. Lexer ile token'ları üretir (`tokenize_code_with_positions`)
4. Parser ile token'ları analiz eder
5. Başarılıysa "✓ Syntax OK" gösterir; hata varsa hata mesajını gösterir
6. Token'lara tema renkleri ile etiketler ekler (`apply_syntax_highlighting`)

### 4.2. Renk Kodlaması ve Temalar

İki tema tanımlanmıştır:

#### Açık Tema (`light_theme`)
- Beyaz arka plan
- Koyu metinler
- Örnek: `KEYWORD: '#3a45cb'`

#### Koyu Tema (`dark_theme`)
- Koyu arka plan  
- Açık metinler
- Örnek: `KEYWORD: '#FF8C00'`

Her token türü için renkler `highlighter_colors` altında tanımlıdır. `apply_theme_globally` ve `toggle_theme` fonksiyonları temayı tüm bileşenlere uygular.

### 4.3. Hata Vurgulaması

- Hatalar `error_label` üzerinde gösterilir (kırmızı renkte)
- Hata durumunda metin alanına `ERROR` etiketi uygulanır
- Temaya göre kırmızımsı arka plan

### 4.4. Performans Optimizasyonları

- **Zamanlama:** `after(100, ...)` ile GUI donmaları önlenir
- **Değişiklik Kontrolü:** `last_code` ile gereksiz işlemler engellenir  
- **Regex Optimizasyonu:** `re.compile()` ile hızlı tokenizasyon

## 5. Grafiksel Kullanıcı Arayüzü (`main.py`)

### 5.1. Kullanılan Araç Kiti
**Tkinter**

### 5.2. Ana Bileşenler

```
├── Üst Çerçeve (top_frame)
│   ├── "Run Code" butonu
│   ├── "Toggle Theme" butonu  
│   └── "Python Code Editor" başlığı
│
├── Ana Çerçeve (main_frame)
│   ├── İçerik Çerçevesi (content_frame)
│   │   ├── Editör Çerçevesi (editor_frame)
│   │   │   ├── Satır Numaraları (line_numbers)
│   │   │   ├── Kod Alanı (text_area)
│   │   │   └── Kaydırma çubukları
│   │   │
│   │   ├── Hata Etiketi (error_label)
│   │   │
│   │   └── Analiz Çerçevesi (analysis_frame)
│   │       ├── Token'lar Sekmesi (token_tree)
│   │       └── Ağaç Yapısı Sekmesi (tree_tree)
│   │
│   └── Çıktı Çerçevesi (output_frame)
│       └── Çıktı Alanı (output_area)
```

### 5.3. Gerçek Zamanlı Güncellemeler

- **Sözdizimi Vurgulama:** Yazım sırasında anında güncellenir
- **Satır Numaraları:** Kaydırma veya içerik değişikliğinde senkronize edilir
- **Hata Bildirimi:** Hatalar anında `error_label`'da gösterilir
- **Parantez Eşleştirme:** İmleç hareketiyle çalışır
- **Otomatik Tamamlama:** Yazarken öneriler sunar
- **Analiz Panelleri:** Kod değiştiğinde `update_analysis` ile güncellenir

## 6. Gelişmiş Özellikler

### 6.1. Parantez Eşleştirme (`BracketMatcher`)

- `(`, `)`, `[`, `]`, `{`, `}` parantezlerini eşleştirir
- **Eşleşme varsa:** `BRACKET_MATCH` (yeşil) etiketi
- **Eşleşme yoksa:** `BRACKET_MISMATCH` (kırmızı) etiketi
- 100 ms gecikmeyle çalışır (`schedule_bracket_check`)

### 6.2. Otomatik Tamamlama (`AutoCompleter`)

**Özellikler:**
- Anahtar kelimeler, yerleşik fonksiyonlar ve kod içindeki tanımlayıcılar için öneriler
- Öneriler imlecin altında Listbox ile gösterilir
- **Klavye kısayolları:**
  - `Tab`, `Enter`: Seçim yapma
  - `Escape`: Kapatma
  - `Ctrl+Space`: Manuel tetikleme
- Minimum 1 karakterle öneriler başlar

### 6.3. Tema Yönetimi

- Açık ve koyu tema arasında geçiş ("Toggle Theme" butonu)
- Renkler tüm GUI bileşenlerine ve token'lara uygulanır
- Anlık tema değişimi

### 6.4. Kod Çalıştırma

- "Run Code" butonu kodu `exec()` ile çalıştırır
- Çıktılar ve hatalar `output_area`'da gösterilir
- Durum bilgisi `error_label`'da görüntülenir

### 6.5. Analiz Panelleri

#### Token'lar Sekmesi
- Token bilgileri (tür, değer, satır, sütun)
- Çift tıkla kodda vurgulama

#### Ağaç Yapısı Sekmesi  
- Sözdizimi ağacı görselleştirmesi
- Tıklamayla kodda vurgulama

## 7. Kurulum ve Kullanım

### Gereksinimler
- **Python 3.7+** (Tkinter dahil)

### Hızlı Başlangıç

1. Proje dosyalarını indirin
2. Terminal/komut satırında çalıştırın:
   ```bash
   python main.py
   ```
3. Kodu yazın ve özellikleri keşfedin!

## 8. Teknik Detaylar ve Optimizasyonlar

### Performans İyileştirmeleri

| Bileşen | Optimizasyon | Açıklama |
|---------|--------------|----------|
| **Sözcüksel Analiz** | `re.compile()` | Hızlı regex işleme |
| **Ayrıştırma** | Özyinelemeli iniş | Kesin hata raporlaması |
| **GUI** | Tkinter | Hafif ve platformlar arası uyumlu |
| **Vurgulama** | Gecikme mekanizması | GUI donmalarını önler |
| **Bellek** | Değişiklik kontrolü | Gereksiz işlemleri engeller |
