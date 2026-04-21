# 🤝 YaparAI MCP — Katkı Rehberi

> Forkladığınız proje: `https://github.com/enis1998/yaparai-mcp`  
> Orijinal proje: `https://github.com/ilhankilic/yaparai-mcp`

Bu belge, projeye nasıl katkı sağlayabileceğinizi, eksik olan ne olduğunu ve hangi alanlarda geliştirme yapılabileceğini detaylı olarak açıklar.

---

## 📊 Mevcut Durum Özeti

| Alan | Durum |
|------|-------|
| Test Coverage | ❌ Sıfır test yok |
| CI/CD Pipeline | ❌ GitHub Actions yok |
| CONTRIBUTING.md | ❌ Katkı rehberi yok |
| CHANGELOG.md | ❌ Değişiklik geçmişi yok |
| Retry Mekanizması | ❌ Ağ hatalarında yeniden deneme yok |
| Loglama | ❌ Debug/info log yok |
| Tip Güvenliği | ⚠️ `Literal` tipler kullanılmamış |
| Eksik Araçlar | ⚠️ Client'ta var ama MCP aracı yok olanlar |
| `swap_face` İkinci Görsel | ⚠️ `face_url` parametresi eksik |
| Model Seçimi | ⚠️ Görüntü üretiminde model seçilemiyor |

---

## 🔴 KRİTİK EKSİKLER (Hemen Katkı Sağlanabilir)

### 1. 🧪 Test Yazılması — En Büyük Boşluk

Projede **tek bir test dosyası bile yok**. Bu, açık kaynak katkı için en değerli alandır.

**Neler test edilebilir:**

```
tests/
├── test_client.py          # YaparAIClient HTTP çağrıları (mock ile)
├── test_generate.py        # generate_image, generate_video, generate_music
├── test_edit.py            # transform_image, remove_background, swap_face
├── test_templates.py       # list_templates, execute_template
├── test_social.py          # Sosyal medya araçları
├── test_crm.py             # CRM araçları
├── test_config.py          # Ortam değişkeni okuma
└── test_org.py             # resolve_org_id hata senaryoları
```

**Örnek test yapısı:**
```python
# tests/test_client.py
import pytest
from unittest.mock import AsyncMock, patch
from yaparai.client import YaparAIClient

@pytest.mark.asyncio
async def test_generate_image_success():
    client = YaparAIClient(api_key="test_key")
    mock_response = {"job_id": "job_123", "status": "queued"}
    
    with patch.object(client, "_request", new=AsyncMock(return_value=mock_response)):
        result = await client.generate({"type": "image", "prompt": "test"})
        assert result["job_id"] == "job_123"

@pytest.mark.asyncio
async def test_missing_api_key_raises():
    with pytest.raises(ValueError, match="YAPARAI_API_KEY"):
        YaparAIClient(api_key="")

@pytest.mark.asyncio
async def test_wait_for_result_timeout():
    client = YaparAIClient(api_key="test_key")
    with patch.object(client, "get_job", new=AsyncMock(return_value={"status": "processing"})):
        with pytest.raises(TimeoutError):
            await client.wait_for_result("job_123", timeout=1, poll_interval=1)
```

**Gerekli bağımlılıklar eklenecek:**
```toml
# pyproject.toml'a eklenecek
[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-mock>=3.12",
    "respx>=0.21",      # httpx mock kütüphanesi
]
```

---

### 2. 🔍 Eksik MCP Araçları — Client'ta Var, Tool Yok

`client.py` incelendiğinde şu metodların karşılık gelen MCP aracı **olmadığı** görülmektedir:

#### a) `list_social_posts` — Sosyal Medya Gönderilerini Listele

```python
# tools/social.py'ye eklenecek
async def list_social_posts(
    platform: str | None = None,
    account_id: str | None = None,
    org_id: str | None = None,
) -> dict:
    """
    List published and scheduled social media posts.

    Args:
        platform: Filter by platform ("instagram", "facebook", "tiktok")
        account_id: Filter by specific social account
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        List of posts with content, platform, published_at, engagement stats.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    params = {}
    if platform:
        params["platform"] = platform
    if account_id:
        params["account_id"] = account_id
    return await client.social_list_posts(oid, params or None)
```

#### b) `get_social_quota` — Sosyal Medya Kota Bilgisi

```python
async def get_social_quota(org_id: str | None = None) -> dict:
    """
    Get social media quota and usage limits.
    
    Returns remaining post quota, message limits, and billing period.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    return await client.social_get_quota(oid)
```

**`server.py`'ye de kayıt eklenmeli:**
```python
mcp.tool(list_social_posts)
mcp.tool(get_social_quota)
```

---

### 3. 🔄 Retry (Yeniden Deneme) Mekanizması

`client.py`'de ağ hatası olduğunda direkt hata fırlatılıyor. **Exponential backoff** eklenebilir:

```python
# client.py — _request metoduna eklenecek
import random

async def _request(self, method: str, path: str, retries: int = 3, **kwargs) -> dict:
    for attempt in range(retries):
        try:
            client = await self._client()
            resp = await client.request(method, path, **kwargs)
            # ... mevcut hata işleme
            resp.raise_for_status()
            return resp.json()
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            if attempt == retries - 1:
                raise
            wait = (2 ** attempt) + random.uniform(0, 1)  # 1s, 2s, 4s + jitter
            await asyncio.sleep(wait)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:  # Rate limit — yeniden dene
                if attempt == retries - 1:
                    raise RuntimeError("Rate limit exceeded.")
                await asyncio.sleep(5 * (attempt + 1))
            else:
                raise
```

---

### 4. 🐛 `swap_face` — İkinci Görsel Parametresi Eksik

Şu anki `swap_face` fonksiyonu sadece bir `image_url` alıyor. Gerçek bir yüz değiştirme işlemi için **iki görsel** gerekir: hedef görüntü + kaynak yüz.

**Mevcut (eksik):**
```python
async def swap_face(prompt: str, image_url: str) -> dict:
```

**Önerilen düzeltme:**
```python
async def swap_face(
    image_url: str,           # Yüzün değiştirileceği hedef görüntü
    face_url: str,            # Kullanılacak kaynak yüz görseli
    prompt: str = "",         # Opsiyonel ek talimat
) -> dict:
    """
    Swap a face in an image using AI.
    
    Args:
        image_url: Target image URL (where the face will be replaced)
        face_url: Source face image URL (the face to use)
        prompt: Optional additional instructions
    """
    client = YaparAIClient()
    job = await client.generate({
        "type": "image",
        "mode": "editor_face_swap",
        "prompt": prompt,
        "image_url": image_url,
        "face_url": face_url,   # Yeni parametre
    })
    ...
```

---

## 🟡 ORTA ÖNCELİKLİ GELİŞTİRMELER

### 5. 🎯 `generate_image`'e Model Seçimi Eklenmesi

Şu an model seçimi API'nin "smart routing"'ine bırakılıyor. Kullanıcı belirli bir model isteyebilir:

```python
async def generate_image(
    prompt: str,
    model: Literal["auto", "flux", "sdxl", "imagen4"] = "auto",  # YENİ
    negative_prompt: str = "",
    width: int = 512,
    height: int = 512,
    style: str | None = None,
) -> dict:
    """
    ...
    Args:
        model: AI model to use — "auto" (smart routing), "flux" (best quality),
               "sdxl" (fast), "imagen4" (Google, photorealistic)
    """
```

---

### 6. 📅 `create_social_post`'a Zamanlama Desteği

Şu an gönderiler anında yayınlanıyor. `scheduled_at` parametresi eklenebilir:

```python
async def create_social_post(
    text: str,
    platform: str,
    account_id: str,
    media_urls: list[str] | None = None,
    scheduled_at: str | None = None,  # YENİ — ISO 8601: "2026-05-01T10:00:00Z"
    org_id: str | None = None,
) -> dict:
    """
    ...
    Args:
        scheduled_at: Optional ISO 8601 datetime to schedule the post
                      (e.g., "2026-05-01T10:00:00Z"). If None, posts immediately.
    """
    payload: dict = {"text": text, "platform": platform, "account_id": account_id}
    if media_urls:
        payload["media_urls"] = media_urls
    if scheduled_at:
        payload["scheduled_at"] = scheduled_at   # YENİ
```

---

### 7. 🏷️ Tip Güvenliği — `Literal` Kullanımı

Şu an platform, tone, style gibi parametreler serbest `str`. Yanlış değer girilince API'den hata gelir. `Literal` ile derleme zamanında yakalanabilir:

```python
# tools/social.py
from typing import Literal

async def create_social_post(
    text: str,
    platform: Literal["instagram", "facebook", "tiktok", "twitter"],  # str yerine
    account_id: str,
    ...
)

# tools/generate.py  
async def generate_image(
    prompt: str,
    style: Literal["realistic", "anime", "cinematic", "artistic"] | None = None,
    ...
)
```

---

### 8. 📝 `execute_template`'e Esnek Input Desteği

Şu an şablon çalıştırırken sadece `prompt`, `image_url`, `width`, `height` gönderilebiliyor. Ama 448+ şablonun bazıları çok farklı input bekleyebilir (renk, metin katmanı, vs.):

```python
async def execute_template(
    slug: str,
    prompt: str,
    image_url: str | None = None,
    width: int = 512,
    height: int = 512,
    extra_inputs: dict | None = None,   # YENİ — şablona özel ek parametreler
) -> dict:
    """
    ...
    Args:
        extra_inputs: Additional template-specific inputs (check get_template_detail)
                      e.g., {"brand_color": "#FF0000", "logo_text": "ACME"}
    """
    payload = {"prompt": prompt, "width": width, "height": height}
    if image_url:
        payload["image_url"] = image_url
    if extra_inputs:
        payload.update(extra_inputs)   # YENİ
```

---

### 9. 📋 `bulk_message`'a Tag Filtresi

Şu an tüm müşteri ID'leri tek tek verilmeli. Etiket bazlı toplu mesaj çok daha pratik olur:

```python
async def bulk_message(
    message: str,
    customer_ids: list[str] | None = None,  # Artık opsiyonel
    tag: str | None = None,                 # YENİ — "vip", "lead" gibi
    platform: str | None = None,            # YENİ — sadece belirli platform
    media_urls: list[str] | None = None,
    org_id: str | None = None,
) -> dict:
    """
    ...
    Args:
        customer_ids: Specific customer IDs (or use tag/platform to filter)
        tag: Send to all customers with this tag (e.g., "vip", "returning")
        platform: Send only to customers from this platform
    """
```

---

## 🟢 KÜÇÜK AMA DEĞERLİ KATKILAR

### 10. 🛠️ GitHub Actions CI/CD Pipeline

`.github/workflows/ci.yml` oluşturulabilir:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: pytest tests/ -v --tb=short
  
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff
      - run: ruff check src/
```

---

### 11. 📖 `CONTRIBUTING.md` Dosyası

Orijinal projede katkı rehberi yok. Şu adımları içeren bir dosya eklenebilir:
- Fork & clone nasıl yapılır
- Geliştirme ortamı kurulumu
- Test nasıl çalıştırılır
- PR açma süreci
- Kod stil kuralları

---

### 12. 📜 `CHANGELOG.md` Dosyası

Versiyon geçmişi belgesi oluşturulabilir. [Keep a Changelog](https://keepachangelog.com) formatında.

---

### 13. ⚡ `remove_background`'daki Gereksiz `prompt` Parametresi

Arka plan kaldırma için açıklama metni anlamsız. Parametre ya kaldırılmalı ya da opsiyonel yapılmalı:

```python
# Mevcut (garip kullanım):
async def remove_background(prompt: str, image_url: str) -> dict:

# Önerilen:
async def remove_background(
    image_url: str,
    output_format: Literal["transparent", "white"] = "transparent",  # YENİ
) -> dict:
```

---

### 14. 📊 Loglama (Logging) Eklemesi

Debug için yapılandırılabilir log sistemi:

```python
# client.py'ye eklenecek
import logging

logger = logging.getLogger("yaparai")

class YaparAIClient:
    async def _request(self, method, path, **kwargs):
        logger.debug(f"→ {method} {path}")
        # ...
        logger.debug(f"← {resp.status_code} ({elapsed:.2f}s)")
```

---

### 15. 🌐 Türkçe Hata Mesajları / i18n Desteği

Tüm hata mesajları İngilizce. Locale bazlı mesaj desteği veya en azından Türkçe seçeneği eklenebilir.

---

## 🗺️ Katkı Öncelik Sırası (Önerilen)

```
1. ✅ Test yazımı (test_client.py ile başla)
2. ✅ list_social_posts + get_social_quota araçları ekleme  
3. ✅ swap_face'e face_url parametresi ekleme
4. ✅ GitHub Actions CI pipeline oluşturma
5. ✅ Retry mekanizması (client.py)
6. ✅ Literal tip güvenliği (tüm tool dosyaları)
7. ✅ execute_template'e extra_inputs ekleme
8. ✅ generate_image'e model seçimi ekleme
9. ✅ create_social_post'a scheduled_at ekleme
10. ✅ CONTRIBUTING.md ve CHANGELOG.md dosyaları
```

---

## 🚀 Geliştirme Ortamı Kurulumu

```bash
# Repo'yu clone'la
git clone https://github.com/enis1998/yaparai-mcp.git
cd yaparai-mcp

# Geliştirme bağımlılıklarıyla kur
pip install -e ".[dev]"

# Test çalıştır
pytest tests/ -v

# Lint kontrolü
ruff check src/
```

---

## 📬 Pull Request Açma Süreci

1. `git checkout -b feature/test-coverage` (veya `fix/swap-face-face-url`)
2. Değişikliklerinizi yapın
3. `pytest tests/` ile testlerin geçtiğini doğrulayın
4. `git push origin feature/test-coverage`
5. GitHub'da **orijinal repoya** (ilhankilic/yaparai-mcp) PR açın
6. PR başlığını açıklayıcı yazın, ne yaptığınızı, neden gerekli olduğunu belirtin

---

*Bu rehber `enis1998/yaparai-mcp` forku için hazırlanmıştır. — Nisan 2026*

