# Webpack SPA Identification & JS File Audit Rules

Supplement to upstream `js-api-extract` and `api-fuzz` skills. Covers SPA build-tool identification, JS file triage grading, and async chunk authorization testing.

---

## 1. SPA Framework Identification

Before extracting endpoints, identify the build tool and SPA type. This determines which extraction strategies work and which are useless.

### 1.1 Webpack-Built SPA

| Indicator | Location | What It Means |
|-----------|----------|---------------|
| `webpackJsonp` | Global JS scope | Webpack runtime is present (v3+) |
| `__webpack_require__` | Any JS file | Webpack module system active |
| `chunk-vendors.*.js` | Filename | Vue CLI project (webpack-based) |
| `main.*.chunk.js` | Filename | Create React App (webpack-based) |
| `runtime~main.*.js` | Filename | Webpack 4/5 with chunk splitting |
| `polyfills.*.js` | Filename | Angular CLI (webpack-based) |
| `manifest.*.json` at `/` or `/static/js/` | File | Webpack asset manifest |
| Hash in filename (`app.a1b2c3d4.js`) | Filename | Content-hashed production build |
| No hash (`app.js`) | Filename | Dev build; easier to track changes |

### 1.2 Vite-Built SPA

| Indicator | What It Means |
|-----------|---------------|
| `<script type="module">` in HTML | Native ESM loading (not Webpack) |
| `index.*.js` with no Webpack artifacts | Vite/Rollup output |
| `/@vite/` in dev mode URLs | Vite dev server running |
| `import.meta.env.` references in JS | Vite environment variables |
| `__vite_*` globals | Vite HMR runtime |

### 1.3 Hash-Route SPA (Client-Side Routing)

**Identification**: URLs contain `#/` (e.g., `target.com/#/admin/users`)

**Key insight for testing**: The `#` fragment is NEVER sent to the server. All pages share the same HTML shell. Backend only serves the SPA fallback at `/`. API endpoints are the ONLY real HTTP paths.

**Strategy**: For hash-route SPAs:
- Directory brute-forcing is **useless** (everything returns 200 with SPA fallback)
- JS extraction is the **only reliable way** to discover backend endpoints
- Route names in JS often map 1:1 to API paths (`/admin/users` → `GET /api/admin/users`)

---

## 2. JS File Grading System (A / B / C)

⛔ **MUST grade JS files BEFORE extraction.** Do not blindly process all files. This system saves analysis time and focuses on high-yield sources.

### Grade A — ⛔ Must Extract (Highest Priority)

| File Pattern | Reason |
|-------------|--------|
| `app.*.js` / `main.*.js` | Main application bundle — ALL core business logic |
| `config.*.js` / `setting.*.js` | Global config — domains, keys, backend URLs, test env |
| `api.*.js` / `request.*.js` | Unified API request wrapper — ALL backend endpoints |
| `router.*.js` | Frontend route config — ALL page paths, admin entry points |
| `utils.*.js` / `common.*.js` | Utility functions — encryption keys, signature algorithms, credentials |
| `backup*.js` | Dev backup files — test endpoints, plaintext keys, debug code |
| Files containing `baseURL` / `API_URL` / `apiPrefix` | Direct backend base URL exposure |
| Files > 500KB | Large enough to contain full app logic |
| WayBack historical versions of any Grade A file | Old versions may expose deleted-but-still-active endpoints |

### Grade B — Likely Useful (Process if time permits)

| File Pattern | Reason |
|-------------|--------|
| Named route chunks: `page-admin.*.js`, `dashboard.*.js`, `panel.*.js` | Admin route logic, admin-specific API calls |
| Files 50KB–500KB | Large enough to have logic, small enough to process |
| Files containing `axios` / `fetch` / `this.$http` / `HttpClient` | HTTP client usage — has API calls |
| Files containing `Bearer` / `Authorization` / `x-api-key` / `token` | Auth token handling — might expose auth endpoints |
| Files containing `import(` | Dynamic imports — references other chunk files |
| Files containing `process.env.` | Environment variable usage — may reveal internal config |
| `.map` sourcemap files | Contains unminified original code with comments and variable names |

### Grade C — ⛔ Skip (Only if No Other Files Found)

| File Pattern | Reason |
|-------------|--------|
| `polyfills.*.js` | Browser polyfills only — zero application logic |
| `vendor.*.js` / `chunk-libs.*.js` WITHOUT API references | Framework/library internals (React, Vue, lodash) |
| `runtime.*.js` | Webpack runtime bootstrap — no business logic |
| `*.worker.js` | Web Workers — isolated context, limited API surface |
| Files < 2KB | Too small to contain meaningful logic |
| Filenames containing `polyfill` | Explicitly marked polyfill |
| Files from CDN (`cdn.jsdelivr.net`, `unpkg.com`, etc.) | Third-party libraries, skip unless scoped to target domain |

### 2.1 Quick Triage Script

```bash
#!/bin/bash
# Grade JS files by scanning the first 2048 bytes for high-value indicators

TARGET_DIR="$1"
OUTPUT_A="grade_a_files.txt"
OUTPUT_B="grade_b_files.txt"
OUTPUT_C="grade_c_files.txt"

> "$OUTPUT_A"; > "$OUTPUT_B"; > "$OUTPUT_C"

for js_file in $(find "$TARGET_DIR" -name "*.js" -type f); do
    fname=$(basename "$js_file")
    fsize=$(stat -c%s "$js_file" 2>/dev/null || stat -f%z "$js_file" 2>/dev/null)
    
    # Grade A checks
    if echo "$fname" | grep -qiE '^(app|main|config|setting|api|request|router|utils|common|backup)\.'; then
        echo "$js_file ($fsize bytes)" >> "$OUTPUT_A"
        continue
    fi
    
    # Check first 2KB for API indicators
    head_bytes=$(head -c 2048 "$js_file" 2>/dev/null)
    if echo "$head_bytes" | grep -qE '(baseURL|API_URL|apiPrefix|BASE_URL|REACT_APP_|VITE_|NEXT_PUBLIC_)'; then
        echo "$js_file ($fsize bytes) [config indicators]" >> "$OUTPUT_A"
        continue
    fi
    
    # Grade C checks
    if [ "$fsize" -lt 2048 ]; then
        echo "$js_file ($fsize bytes) [tiny]" >> "$OUTPUT_C"
        continue
    fi
    
    if echo "$fname" | grep -qiE '(polyfill|runtime\b|\.worker\.)'; then
        echo "$js_file [skip pattern]" >> "$OUTPUT_C"
        continue
    fi
    
    if echo "$fname" | grep -qiE '^vendor\.|^chunk-libs\.'; then
        # Vendor file — check if it has API references before skipping
        if echo "$head_bytes" | grep -qiE '(api|axios|fetch|graphql|rest|service)'; then
            echo "$js_file ($fsize bytes) [vendor with API refs]" >> "$OUTPUT_B"
        else
            echo "$js_file ($fsize bytes) [vendor no API]" >> "$OUTPUT_C"
        fi
        continue
    fi
    
    # Default: Grade B if > 50KB, otherwise C
    if [ "$fsize" -gt 51200 ]; then
        echo "$js_file ($fsize bytes)" >> "$OUTPUT_B"
    else
        echo "$js_file ($fsize bytes) [small]" >> "$OUTPUT_C"
    fi
done

echo "Grade A: $(wc -l < "$OUTPUT_A") files"
echo "Grade B: $(wc -l < "$OUTPUT_B") files"
echo "Grade C: $(wc -l < "$OUTPUT_C") files (skipped)"
```

---

## 3. Async Chunk Unauthorized Access

Webpack/Vite async chunks are typically **publicly accessible files**. Even if the API they call requires authentication, the chunk file itself is downloadable by anyone who knows its URL. This enables **endpoint discovery of protected/admin functionality** without authentication.

### 3.1 The Attack Surface

1. Admin dashboard chunk (`admin.*.chunk.js`) — lists all admin API endpoints
2. Setup/onboarding chunk (`setup.*.chunk.js`) — might contain default credentials
3. Config chunk (`config.*.chunk.js`) — might expose internal service URLs
4. User management chunk — lists user CRUD API paths

### 3.2 Enumeration Technique

```bash
TARGET="https://example.com"

# Step 1: Get all chunk URLs from manifest
curl -s "$TARGET/asset-manifest.json" | jq -r '.[] | select(endswith(".js"))' | while read chunk; do
    echo "=== $chunk ==="
    curl -s "$TARGET$chunk" | grep -oP '["\x27]/(?:api|v[0-9]|rest|service|graphql|admin|internal)[^\s"\x27]*' | sort -u
done

# Step 2: Download admin-suggestive chunks WITHOUT authentication
for chunk_pattern in "admin" "dashboard" "manage" "panel" "settings" "config" "user" "account" "billing" "report"; do
    # Try webpack chunk naming
    curl -s -o "${chunk_pattern}.js" "$TARGET/static/js/${chunk_pattern}.*.chunk.js" 2>/dev/null
    # Try vite chunk naming
    curl -s -o "${chunk_pattern}.js" "$TARGET/assets/${chunk_pattern}.*.js" 2>/dev/null
    
    if [ -s "${chunk_pattern}.js" ]; then
        echo "[!] Downloaded ${chunk_pattern} chunk"
        grep -oP '["\x27]/(?:api|v[0-9]|rest|service|graphql)[^\s"\x27]*' "${chunk_pattern}.js" | sort -u
    fi
done
```

### 3.3 Real-World Scenarios

| Scenario | Leaked Content | Impact |
|----------|---------------|--------|
| Admin dashboard chunk accessible without login | All admin API paths (`/api/admin/users`, `/api/admin/settings`) | Full admin API surface exposed |
| Setup wizard chunk accessible on production | Step-by-step setup API calls, default config | May reveal initialization endpoints |
| Developer tools chunk in production | Debug endpoints, profiling APIs, internal tool URLs | Internal tool access |
| A/B test chunk with "pro" features | Premium/pro API paths | Premium feature bypass via direct API call |
| Old chunk from previous version (Wayback) | Deprecated API paths that still respond | Legacy API with weaker auth |

---

## 4. Integration with Upstream Skills

### When to Use This File

1. **After** identifying the target as a JavaScript-heavy application during recon
2. **Before** running upstream `js-api-extract` Phase 2 (endpoint extraction) — grade files first
3. **During** `api-fuzz` Phase 1 (API discovery) — use chunk enumeration for hidden endpoints
4. **When** you encounter a Webpack/Vite SPA — use Section 1 for framework identification

### Priority Order

1. Identify framework (Section 1) → determines extraction strategy
2. Grade JS files (Section 2) → prioritizes analysis effort
3. Extract endpoints from Grade A files first
4. Enumerate and download async chunks (Section 3) → second round of extraction
5. Process Grade B files if time permits
