---
name: s-oss
description: Unified Object Storage Security skill — bucket enumeration, ACL misconfiguration, AK/SK leakage, cross-tenant access.
---

# Unified Object Storage Security

## When To Use

Use for cloud object storage security assessment: S3/Aliyun OSS/Tencent COS/Huawei OBS bucket enumeration, anonymous read/write detection, AK/SK credential leakage, file listing traversal.

## Source Priority

| Task Type | Primary Source |
|---|---|
| Methodology | hack-skills |
| Execution | AboutSecurity |
| Ctf | AboutSecurity |
| Bug Bounty | hack-skills |
| Resources | AboutSecurity |

## Source Strategy

- Use hack-skills for methodology, scenario classification, domain coverage and deeper playbooks.
- Use AboutSecurity for execution constraints, mandatory rules, payload files, dictionaries, tool YAML configs, CTF and K8s fine-grained resources.
- Do not duplicate upstream content here. Load upstream files when needed.

## Recommended Loading Order

### High-Level Analysis

1. Read matched hack-skills files first unless Source Priority says otherwise.
2. Then read matched AboutSecurity files for constraints and execution details.

### Execution

1. Read matched AboutSecurity skill files first.
2. Check related Tools YAML.
3. Check related Payload/Dic/Doc files.
4. Fall back to hack-skills for scenario variants and methodology.

### Bug Bounty / Authorized Assessment

1. Prefer hack-skills methodology and scenario files.
2. Use AboutSecurity tools/resources for execution support.

## Matched hack-skills Skills

- `../../security-sources/hack-skills/skills/cloud-security/SKILL.md` — SKILL: Cloud Security — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/information-disclosure/SKILL.md` — SKILL: Information Disclosure — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/cloud/cloud-metadata/SKILL.md` — 云元数据利用方法论
- `../../security-sources/AboutSecurity/skills/cloud/s3-bucket-security/SKILL.md` — S3/OSS 存储桶安全测试方法论

## Related AboutSecurity Payloads

- `../../security-sources/AboutSecurity/Payload/cloud/_meta.yaml`
- `../../security-sources/AboutSecurity/Payload/cloud/oss-payload.txt`

## Vulnerability Testing Output Template

When you discover a potential OSS bucket vulnerability, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 1: 测试思路 (Testing Approach)
- Describe OSS discovery source: JS file, HTML src/href, API response, CSP header, error message
- Classify cloud platform: AWS S3, Alibaba Cloud OSS, Tencent COS, Huawei OBS, MinIO, Azure Blob
- Document bucket URL pattern: virtual-hosted-style vs path-style; region identification
- State decision tree: bucket URL identified → anonymous list test → anonymous read test → anonymous write test → AK/SK extraction from JS → credential validation
- Expected success indicator: XML file listing, accessible object, successful PUT, valid credential response

### Module 2: 关键技巧 (Key Techniques)
- JS source extraction: grep JS files for `oss-`, `aliyuncs`, `s3.`, `myqcloud`, `obs.`, `blob.core.windows`, `AccessKeyId`, `LTAI`, `AKID`
- Bucket name bruteforce: `<company>-static`, `<company>-assets`, `<company>-upload`, `<company>-backup`, `<company>-cdn`, `<company>-logs`
- Cross-region enumeration: same bucket name may exist in multiple regions with different ACLs
- Signed URL parameter stripping: remove `?Expires=...&Signature=...` from pre-signed URLs → test if unsigned access works

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by platform:
  1. **AWS S3**: `aws s3 ls s3://<bucket> --no-sign-request`; curl `https://<bucket>.s3.amazonaws.com/?list-type=2`; PUT test: `aws s3 cp test.txt s3://<bucket>/ --no-sign-request`
  2. **Aliyun OSS**: curl `https://<bucket>.oss-cn-<region>.aliyuncs.com/?prefix=&delimiter=/`; XML response → file listing; `?acl` → bucket ACL policy
  3. **Tencent COS**: curl `https://<bucket>.cos.<region>.myqcloud.com/?prefix=`; check `ListBucket` permission; anonymous PUT test
  4. **Credential validation (Aliyun)**: `aliyun sts GetCallerIdentity --access-key-id <AK> --access-key-secret <SK>` → verify AK/SK validity

### Module 4: 绕过方法 (Bypass Methods)
1. **Bucket name discovery**: search archived/old JS files via wayback machine; check CDN CNAME records; analyze CSP headers for `*.aliyuncs.com` / `*.amazonaws.com`
2. **ACL policy enumeration**: `?acl`, `?policy`, `?cors`, `?versioning`, `?logging` — policy endpoints may have different auth than object endpoints
3. **Cross-account/tenant access**: bucket policies may allow `Principal: *` or specific account IDs — test from different cloud accounts
4. **CDN → origin bucket bypass**: if CDN blocks listing but origin bucket URL is reachable → direct access bypasses CDN WAF

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- ⛔ AK/SK 类发现直接记录提交，不深入验证（国内SRC规则）
- ⛔ 不下载/保存/传播 OSS 桶内的业务数据
- Only operate in authorized environments.
