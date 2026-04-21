# 📋 YaparAI MCP Server — Proje Analizi

## 🧩 Proje Nedir?

**YaparAI MCP Server**, [YaparAI](https://www.yaparai.com) platformunun tüm yapay zeka araçlarını **Claude Desktop**, **Cursor**, **Windsurf** ve diğer **MCP (Model Context Protocol)** uyumlu yapay zeka asistanlarına doğrudan entegre eden bir Python paketidir.

Kullanıcılar, bu sunucu sayesinde sohbet arayüzü üzerinden görüntü üretmekten sosyal medya yönetimine, CRM işlemlerinden müzik oluşturmaya kadar 30 farklı yapay zeka aracını doğal dil ile kullanabilir.

---

## 🏗️ Teknik Altyapı

| Özellik | Detay |
|---|---|
| **Dil** | Python 3.10+ |
| **Paket Adı** | `yaparai` |
| **Versiyon** | 0.3.1 |
| **Lisans** | Apache 2.0 |
| **MCP Çerçevesi** | [FastMCP](https://github.com/jlowin/fastmcp) (≥2.0.0) |
| **HTTP İstemcisi** | [httpx](https://www.python-httpx.org/) (≥0.27.0, async) |
| **Build Sistemi** | Hatchling |
| **Yazar** | Ilhan Kilic — ilhan.kilic@yaparai.com |

---

## 📁 Proje Yapısı

```
yaparai-mcp-master/
├── pyproject.toml              # Paket tanımı, bağımlılıklar, CLI giriş noktası
├── README.md                   # İngilizce kullanım kılavuzu
└── src/yaparai/
    ├── __init__.py
    ├── config.py               # Ortam değişkenlerini okur (API Key, Base URL, Org ID)
    ├── client.py               # YaparAI API ile async HTTP iletişim katmanı
    ├── server.py               # FastMCP sunucusu — 30 aracı kaydeder
    └── tools/
        ├── generate.py         # Görüntü, video, müzik üretimi
        ├── edit.py             # Görüntü düzenleme
        ├── ecommerce.py        # E-ticaret araçları
        ├── avatar.py           # Avatar / lip sync
        ├── templates.py        # ComfyUI şablon yönetimi
        ├── ai.py               # Gemini metin & görsel analiz
        ├── chatbot.py          # Chatbot etkileşimi
        ├── social.py           # Sosyal medya yönetimi (Kurumsal)
        ├── crm.py              # CRM müşteri yönetimi (Kurumsal)
        ├── organizations.py    # Organizasyon listesi
        ├── balance.py          # Kredi bakiyesi
        ├── models.py           # Model listesi
        └── jobs.py             # İş durumu sorgulama
```

---

## ⚙️ Mimari Nasıl Çalışır?

```
Claude Desktop / Cursor / Windsurf
         │  (MCP Protokolü)
         ▼
    server.py  ──►  FastMCP (30 araç kayıtlı)
         │
         ▼
    tools/*.py  (her araç bağımsız async fonksiyon)
         │
         ▼
    client.py  (YaparAIClient — async httpx)
         │
         ▼
    https://api.yaparai.com
```

### Akış Detayı

1. **Yapılandırma (`config.py`):** `YAPARAI_API_KEY`, `YAPARAI_BASE_URL`, `YAPARAI_ORG_ID` ortam değişkenlerinden okunur.
2. **İstemci (`client.py`):** `YaparAIClient` sınıfı bağlantı havuzu kullanan tek bir `httpx.AsyncClient` ile tüm API çağrılarını yönetir. 401, 402, 403, 429 hata kodlarını anlamlı mesajlarla fırlatır.
3. **Araçlar (`tools/`):** Her araç bağımsız bir `async def` fonksiyonu. FastMCP bu fonksiyonları otomatik olarak MCP aracına dönüştürür.
4. **Sunucu (`server.py`):** Tüm araçları `mcp.tool()` ile kaydeder. `yaparai` CLI komutu çalıştırıldığında `mcp.run()` ile sunucu başlar.
5. **İş Kuyruğu:** Üretim işlemleri asenkron çalışır. `wait_for_result()` metodu sonuç hazır olana kadar belirli aralıklarla iş durumunu sorgular (polling).

---

## 🛠️ 30 Araç — Tam Liste

### 🎨 İçerik Üretimi (4 araç)

| Araç | Açıklama | Model | Maliyet |
|------|----------|-------|---------|
| `generate_image` | Metin → Görüntü | Flux, SDXL, Imagen 4 | ~6 kredi |
| `generate_video` | Metin/Görüntü → Video | Veo 3.1, Kling | ~350 kredi |
| `generate_music` | Metin → Müzik/Şarkı | Suno v4 | ~14 kredi |
| `generate_music_video` | Müzik + Video birlikte | Suno v4 + Kling/Veo | ~364 kredi |

### ✂️ Görüntü Düzenleme (3 araç)

| Araç | Açıklama | Maliyet |
|------|----------|---------|
| `transform_image` | Görüntüden görüntüye stil transferi | ~6 kredi |
| `remove_background` | Arka plan kaldırma | ~2 kredi |
| `swap_face` | Yüz değiştirme | ~6 kredi |

### 🛒 E-Ticaret (2 araç)

| Araç | Açıklama | Maliyet |
|------|----------|---------|
| `virtual_try_on` | Sanal kıyafet deneme | ~6 kredi |
| `generate_mannequin` | Ürün fotoğrafı için AI manken | ~6 kredi |

### 🤖 Avatar (1 araç)

| Araç | Açıklama | Maliyet |
|------|----------|---------|
| `lip_sync` | Fotoğraftan konuşan avatar | ~14 kredi |

### 📐 Şablonlar — 448+ ComfyUI İş Akışı (3 araç)

| Araç | Açıklama | Maliyet |
|------|----------|---------|
| `list_templates` | Şablonları listele (logo, reklam, ürün…) | Ücretsiz |
| `get_template_detail` | Şablon giriş/çıkış detayları | Ücretsiz |
| `execute_template` | Şablonu çalıştır | Değişken |

### 🧠 AI Araçları — Gemini (2 araç)

| Araç | Açıklama | Maliyet |
|------|----------|---------|
| `generate_text` | Metin üretimi (senaryo, sözler, storyboard) | ~2 kredi |
| `analyze_image` | Görüntü analizi ve açıklama | ~2 kredi |

### 💬 Chatbot (2 araç)

| Araç | Açıklama | Maliyet |
|------|----------|---------|
| `list_chatbots` | Mevcut chatbot'ları listele | Ücretsiz |
| `chat_with_bot` | Chatbot ile sohbet et | Değişken |

### 📱 Kurumsal: Sosyal Medya (8 araç)

| Araç | Açıklama |
|------|----------|
| `list_social_accounts` | Bağlı sosyal medya hesaplarını listele |
| `create_social_post` | Instagram/Facebook/TikTok/X'e gönderi paylaş |
| `generate_caption` | AI ile gönderi açıklaması oluştur |
| `generate_hashtags` | AI ile hashtag oluştur |
| `list_inbox` | Gelen mesajları/DM'leri listele |
| `read_conversation` | Konuşma mesajlarını oku |
| `reply_to_message` | Mesaja yanıt ver |
| `ai_reply_suggestion` | AI ile yanıt önerisi al |

### 👥 Kurumsal: CRM (6 araç)

| Araç | Açıklama |
|------|----------|
| `list_customers` | CRM müşterilerini listele |
| `get_customer` | Müşteri detaylarını getir |
| `extract_customer_info` | Konuşmalardan AI ile müşteri bilgisi çıkar |
| `send_shipping_info` | Kargo takip bildirimi gönder |
| `bulk_message` | Toplu müşteri mesajı gönder |
| `sync_customers_from_inbox` | Inbox'tan müşteri aktar |

### 🔧 Yardımcı Araçlar (4 araç)

| Araç | Açıklama |
|------|----------|
| `list_organizations` | Organizasyonları listele |
| `check_balance` | Kredi bakiyesini kontrol et |
| `list_models` | Modelleri ve maliyetleri listele |
| `get_job_status` | İş durumunu sorgula |

---

## 🔑 Ortam Değişkenleri

| Değişken | Zorunlu | Açıklama | Varsayılan |
|---|---|---|---|
| `YAPARAI_API_KEY` | ✅ Evet | API anahtarı | — |
| `YAPARAI_ORG_ID` | ⚠️ Kurumsal | Sosyal medya ve CRM için org ID | — |
| `YAPARAI_BASE_URL` | ❌ Hayır | API temel URL'i | `https://api.yaparai.com` |

---

## 🚀 Kurulum ve Kullanım

### Kurulum
```bash
pip install yaparai
```

### Claude Desktop Yapılandırması
```json
{
  "mcpServers": {
    "yaparai": {
      "command": "yaparai",
      "env": {
        "YAPARAI_API_KEY": "yap_live_xxxxxxxxxxxxx",
        "YAPARAI_ORG_ID": "opsiyonel-kurumsal-org-id"
      }
    }
  }
}
```

### Python SDK Kullanımı
```python
import asyncio
from yaparai.client import YaparAIClient

async def main():
    client = YaparAIClient(api_key="yap_live_xxxxx")
    job = await client.generate({"type": "image", "prompt": "İstanbul silueti"})
    result = await client.wait_for_result(job["job_id"])
    print(result["result_url"])

asyncio.run(main())
```

---

## 💡 Öne Çıkan Teknik Özellikler

- **Asenkron mimari:** Tüm API çağrıları `async/await` ile non-blocking çalışır.
- **Bağlantı havuzu:** Tek bir `httpx.AsyncClient` örneği tüm araçlar arasında paylaşılır.
- **Akıllı polling:** Uzun süren üretim işleri (video ~180s, müzik ~120s, görüntü ~60s) otomatik olarak tamamlanana kadar beklenir.
- **Anlamlı hata mesajları:** 401/402/403/429 HTTP hatalarına özel, kullanıcı dostu hata mesajları.
- **İki API katmanı:** Public API (`/v1/public/`) ve Kurumsal API (`/api/enterprise/`) ayrı metodlarla yönetilir.
- **MCP uyumluluğu:** FastMCP sayesinde herhangi bir MCP uyumlu istemciyle çalışır.

---

## 💰 Fiyatlandırma Özeti

- Kayıt olunca **100 ücretsiz kredi** (kredi kartı gerekmez)
- Görüntü: ~6 kredi (~$0,50)
- Video: ~350 kredi (~$3-5)
- Müzik: ~14 kredi (~$1)
- Kurumsal özellikler: abonelik ile dahil
- Kredilerin son kullanma tarihi yoktur

---

## 🔗 Bağlantılar

| | |
|---|---|
| **Web Sitesi** | [yaparai.com](https://www.yaparai.com) |
| **Kurumsal** | [kurumsal.yaparai.com](https://kurumsal.yaparai.com) |
| **PyPI** | [pypi.org/project/yaparai](https://pypi.org/project/yaparai/) |
| **GitHub** | [github.com/ilhankilic/yaparai-mcp](https://github.com/ilhankilic/yaparai-mcp) |
| **API Anahtarı** | [yaparai.com/settings](https://www.yaparai.com/settings) |
| **Destek** | destek@yaparai.com |

