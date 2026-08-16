---
name: s-patch-diffing
description: Patch Diffing and 0day Discovery Methodology skill. Covers binary/source patch diffing, security patch analysis, vulnerability root cause identification from patches, N-day to 0day variant discovery, and diffing tools (BinDiff/Diaphora/ghidra-version-tracking).
---

# Patch Diffing & 0day Discovery

## When To Use

Use for analyzing security patches to identify fixed vulnerabilities, discovering variant vulnerabilities (N-day → 0day), reverse engineering patch logic, and competitive vulnerability research.

## Source Priority

| Task Type | Primary Source |
|---|---|
| Methodology | (self-contained) |
| Execution | (self-contained) |
| Ctf | (self-contained) |
| Bug Bounty | (self-contained) |
| Resources | (self-contained) |

## Source Strategy

This is a standalone skill with no upstream bridge. Content is self-contained methodology derived from industry best practices. Extend with CVE reproduction patterns from `s-cve-reproduction`.

## References

See `references/SOURCES.md`.

## Patch Diffing Methodology

### Phase 1: 补丁获取 (Patch Acquisition)
1. **Identify the target**: CVE advisory → affected version → patched version
2. **Obtain both versions**:
   - Open source: GitHub release tags, commit diff (`git diff v1.0 v1.0.1`)
   - Closed source: vendor downloads, MS patch Tuesday KB articles, update packages
   - Android: AOSP security bulletin → commit references
   - iOS/macOS: Apple security notes → dyld_shared_cache diffing
3. **Isolate the security-relevant changes**: vendors often bundle security fixes with feature changes — use the advisory description to narrow the scope

### Phase 2: 二进制 Diffing (Binary Diffing)
**Tools**: BinDiff (IDA/Ghidra plugin), Diaphora (IDA), Ghidra Version Tracking, Radare2 (`radiff2`)

1. Generate function signatures for both versions
2. Match functions between versions (primary matching: name/hash; secondary: call graph/CFG similarity)
3. Filter to changed functions — these are the fix candidates
4. For each changed function:
   - Identify what changed: added bounds check? Changed format string? New authentication gate? Removed dangerous function?
   - Determine if the change is security-relevant or a benign refactor
   - If security-relevant: map the change back to the vulnerability (what was the exploitable path before the fix?)

### Phase 3: 源码 Diffing (Source Diffing)
**Tools**: `git diff`, GitHub compare view, `diff -ruN`

1. **Read the security advisory first** — understand what was fixed at a high level
2. **Review the diff** — look for:
   - Added input validation (length checks, type checks, sanitization)
   - Modified memory operations (buffer size, allocation → free patterns)
   - Changed access control logic (new permission checks, session validation)
   - Removed code paths (debug endpoints, test interfaces, backdoors)
   - Updated dependency versions (transitive CVE fixes)
3. **Ask "why is this the fix?"** — the answer reveals the vulnerability:
   - If they added a length check → the vulnerability was a buffer overflow
   - If they moved `free()` after `use` → it was a use-after-free
   - If they added `require_admin()` → it was a privilege escalation

### Phase 4: 漏洞挖掘 (N-Day → 0day Discovery)
**Goal**: Find the same vulnerability pattern in other software, or variants in the same software

1. **Pattern extraction**: abstract the vulnerability pattern from the fix (e.g. "user-controlled size passed to `memcpy` without upper bound check")
2. **Code search**: grep/grep.app/Sourcegraph for similar patterns in other codebases
3. **Variant analysis in same codebase**: the vendor may have fixed only one instance — search the same codebase for identical patterns (same developer, same mistake pattern)
4. **Adjacent function analysis**: functions called by or calling the fixed function may share the same trust assumptions

### Phase 5: Patch Gap Exploitation
**Definition**: A vendor releases a patch → attackers reverse it → find the vulnerability → exploit unpatched systems

**Timeline considerations**:
- Patch Tuesday → Wednesday: patch diffing race
- Android Security Bulletin: patches released to AOSP immediately, OEMs take weeks/months
- Open source: fix committed to `main` before CVE assigned and advisory published — monitor commit logs

## Key Techniques

### 1. Function signature matching in stripped binaries
- FLIRT signatures (IDA) for standard library functions
- Cross-reference strings to function boundaries
- Import table + call graph reconstruction

### 2. Security patch identification
Not all changes in a security update are security fixes. Use these heuristics:
- Functions with added `if (size > MAX) return ERROR` patterns
- Functions with removed `memcpy`/`strcpy`/`sprintf`
- New `memset(0)` before `free()` (information leak fix)
- Changed comparison operators (`>` to `>=`)

### 3. Root cause extraction template
```
CVE: CVE-YYYY-NNNNN
Fixed function: <function_name> @ <address/file:line>
Before fix:
  <code snippet showing the vulnerable path>
Vulnerability type: <buffer overflow/UAF/type confusion/injection>
Root cause: <one-line explanation>
Trigger condition: <what input/state triggers the bug>
Patch analysis: <what the patch changed, and why it works>
Variant patterns: <similar code patterns to search for elsewhere>
```

## Tools Quick Reference

| Tool | Purpose | Platform |
|------|---------|----------|
| BinDiff | Binary diffing (function matching + call graph) | IDA/Ghidra plugin |
| Diaphora | Binary diffing with Python scripting | IDA plugin |
| Ghidra Version Tracking | Built-in diffing in Ghidra | Standalone |
| `radiff2` | Command-line binary diff | CLI |
| `git diff` / GitHub compare | Source diffing | Web/CLI |
| grep.app / Sourcegraph | Code search across OSS | Web |

## Important Agent Rules

- ⛔ Patch diffing is for authorized vulnerability research only.
- ⛔ Do NOT disclose vulnerability details before coordinated disclosure timeline.
- ⛔ Patch gap exploitation against unpatched third-party systems requires explicit authorization.
- Information derived from patches should be handled as confidential until the CVE embargo lifts.
