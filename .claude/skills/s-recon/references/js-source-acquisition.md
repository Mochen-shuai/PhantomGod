# JavaScript Source Acquisition Enhancement

Supplement to upstream `js-api-extract` skill. Covers JS source collection techniques not present in the upstream methodology.

---

## 1. Mini-Program (.wxapkg) Reverse Engineering

WeChat/Alipay mini-programs package multiple JS pages into `.wxapkg` archives. These often contain full API endpoint definitions not exposed in the web-facing SPA.

### 1.1 Detection

Look for these indicators during recon:

- `/__APP__/` paths in discovered URLs
- `/wxapkg/` directory listings
- `.wxapkg` file downloads from app pages
- Mobile API endpoints returning `wxapkg` Content-Type
- WeChat mini-program AppID in HTML meta tags or JS (`wx.config` / `wx.ready`)

### 1.2 Unpacking

```bash
# Common unpacking tools
# unwxapkg: https://github.com/xxx (check latest fork)
python3 unwxapkg.py app.wxapkg -o unpacked/

# Alternative: wxappUnpacker
node wuWxapkg.js app.wxapkg

# After unpacking, process all .js files with standard js-api-extract Phase 2 patterns
find unpacked/ -name "*.js" -exec grep -oP '["\x27](/(?:api|v[0-9]|rest|service|gateway)[^\s"\x27]*?)["\x27]' {} \;
```

### 1.3 Key Insight

Mini-program JS bundles often contain:

- **Internal/admin API endpoints** not exposed in the web SPA
- **Backup/legacy API paths** that still respond on the main domain
- **Hard-coded API keys** specific to the mini-program context (different from web keys)
- **WeChat-specific auth endpoints** (code2session, access_token, etc.) that may be misconfigured

### 1.4 Alipay Mini-Program

- Look for `.apkg` files
- Alipay mini-programs use `my.request()` instead of standard fetch/axios
- Extract with: `grep -oP "my\.request\(\{.*?url\s*:\s*['\"]([^'\"]+)['\"]" *.js`

---

## 2. Async Chunk Discovery

Single-Page Applications (Vue/React/Angular) with Webpack/Vite use async chunk loading (`import()` / lazy routes). Many endpoints are hidden in lazy-loaded chunks not found in the main bundle.

### 2.1 Webpack Runtime Chunk Analysis

```bash
# Find runtime chunk (Webpack 4+)
curl -s "$TARGET" | grep -oP 'src="([^"]*runtime[^"]*\.js)"' | head -1

# Extract chunk URLs from runtime
curl -s "$TARGET/static/js/runtime~main.*.js" | grep -oP '"([a-zA-Z0-9_-]+)\+?[a-zA-Z0-9]*\.chunk\.(?:js|css)"' | sort -u

# Alternative: extract from manifest.json
curl -s "$TARGET/asset-manifest.json" | jq -r '.[] | select(endswith(".js"))' | sort -u
curl -s "$TARGET/manifest.json" | jq -r 'to_entries[].value' | grep '\.js$' | sort -u
```

### 2.2 Vite/Rollup Dynamic Import Discovery

```bash
# Vite uses native ESM dynamic imports
curl -s "$TARGET/assets/index.*.js" | grep -oP 'import\s*\(\s*["\x60]([^"\x60]+)["\x60]\s*\)' 

# Vite manifest (build output)
curl -s "$TARGET/.vite/manifest.json" 2>/dev/null
```

### 2.3 Automated Chunk Enumeration

```bash
# Discover all chunks from the runtime bundle
TARGET="https://example.com"
JS_DIR=$(curl -s "$TARGET" | grep -oP 'src="([^"]*\.js)"' | head -1 | grep -oP '/[^"]*\.js' | xargs dirname)

# Common Webpack chunk naming patterns to probe
for pattern in "admin" "dashboard" "manage" "panel" "settings" "config" "setup" "profile" "user" "account"; do
    for hash in "" ".*"; do
        curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" "$TARGET${JS_DIR}/${pattern}${hash}.chunk.js"
    done
done
```

---

## 3. Wayback Machine Enhanced CDX Queries

Extends the upstream `js-api-extract` Phase 1.4 with additional CDX API patterns for deeper historical JS discovery.

### 3.1 Full JavaScript History (All MIME Types)

```bash
DOMAIN="example.com"

# All JS MIME types
curl -s "https://web.archive.org/cdx/search/cdx?url=$DOMAIN/*&output=text&fl=original,timestamp&filter=mimetype:application/javascript&limit=500" | sort -u -t' ' -k1,1
curl -s "https://web.archive.org/cdx/search/cdx?url=$DOMAIN/*&output=text&fl=original,timestamp&filter=mimetype:text/javascript&limit=500" | sort -u -t' ' -k1,1

# All chunks (Webpack/Vite)
curl -s "https://web.archive.org/cdx/search/cdx?url=$DOMAIN/*chunk*&output=text&fl=original,timestamp&limit=500" | sort -u

# All bundles
curl -s "https://web.archive.org/cdx/search/cdx?url=$DOMAIN/*bundle*&output=text&fl=original,timestamp&limit=500" | sort -u

# Configuration files (often exposed historically)
curl -s "https://web.archive.org/cdx/search/cdx?url=$DOMAIN/*config*&output=text&fl=original,timestamp&limit=200" | sort -u
curl -s "https://web.archive.org/cdx/search/cdx?url=$DOMAIN/*env*&output=text&fl=original,timestamp&limit=200" | sort -u
```

### 3.2 Differential Endpoint Analysis

```bash
# Collect API endpoints from current JS
curl -s "https://example.com/static/js/app.*.js" | grep -oP '["\x27]/(?:api|v[0-9]|rest|service)[^\s"\x27]*' | sort -u > current_endpoints.txt

# Collect from oldest archived JS snapshot
OLDEST_URL=$(curl -s "https://web.archive.org/cdx/search/cdx?url=$DOMAIN/static/js/app*&output=text&fl=original&limit=1&sort=timestamp" | tail -1)
curl -s "https://web.archive.org/web/0/$OLDEST_URL" | grep -oP '["\x27]/(?:api|v[0-9]|rest|service)[^\s"\x27]*' | sort -u > historical_endpoints.txt

# Find removed-but-still-active endpoints
comm -23 historical_endpoints.txt current_endpoints.txt > removed_endpoints.txt
# Test each: some removed from frontend still work on backend!
```

### 3.3 Time-Range Priority Strategy

- **Oldest snapshots first** (higher chance of forgotten endpoints)
- **Snapshots from major version changes** (look for changelog/release dates)
- **Snapshots before framework migration** (e.g., jQuery → React migration dates)

---

## 4. Backup and Legacy JS File Discovery

### 4.1 Common Backup Patterns

```bash
TARGET="https://example.com"
JS_BASE="/static/js"

# File-based probes
for ext in "bak" "old" "backup" "legacy" "dev" "test" "debug" "v1" "v2" "orig" "save" "tmp"; do
    curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" "$TARGET${JS_BASE}/app.${ext}.js"
    curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" "$TARGET${JS_BASE}/main.${ext}.js"
done

# Source maps (may contain unminified source with comments, internal paths, dev notes)
curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" "$TARGET${JS_BASE}/app.*.js.map"
curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" "$TARGET${JS_BASE}/app.*.js.map.gz"

# Gzip-compressed JS served as raw file
curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" "$TARGET${JS_BASE}/app.*.js.gz"
```

### 4.2 Build Tool Leftovers

```bash
# Webpack dev server artifacts
curl -s "$TARGET/webpack-dev-server"
curl -s "$TARGET/__webpack_hmr"
curl -s "$TARGET/sockjs-node/info"

# Vite dev artifacts
curl -s "$TARGET/@vite/client"
curl -s "$TARGET/@fs/"

# Source maps in production (misconfiguration)
curl -s "$TARGET" | grep -oP 'sourceMappingURL=([^\s]+)' 
```

### 4.3 Version Control Leaks in Static Directories

```bash
# Check if build output includes .git artifacts
paths=(
    "/static/.git/HEAD"
    "/js/.git/config"
    "/assets/.git/refs/heads/main"
    "/static/.svn/entries"
    "/js/.DS_Store"
)
for p in "${paths[@]}"; do
    code=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET$p")
    [ "$code" != "404" ] && echo "[!] $code $TARGET$p"
done
```

---

## Integration Note

This file supplements the upstream `js-api-extract/SKILL.md` Phase 1 (JS File Collection). Load this AFTER the upstream Phase 1 methodology, and use these techniques to expand the JS file corpus before running Phase 2 (API Endpoint Extraction).
