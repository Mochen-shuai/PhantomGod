---
name: s-grpc
description: gRPC Security Testing skill. Covers gRPC endpoint discovery, reflection API enumeration, protobuf message tampering, gRPC-Web testing, authentication/authorization bypass in gRPC services, and request smuggling via gRPC stream multiplexing.
---

# gRPC Security Testing

## When To Use

Use for gRPC endpoint discovery and security assessment, protobuf reflection enumeration, gRPC service fuzzing, authentication bypass in streaming/multiplexed connections, and gRPC-Web proxy security testing.

## Source Priority

| Task Type | Primary Source |
|---|---|
| Methodology | (self-contained) |
| Execution | (self-contained) |
| Ctf | (self-contained) |
| Bug Bounty | (self-contained) |
| Resources | (self-contained) |

## Source Strategy

This is a standalone skill. gRPC security is a specialized area with limited upstream content.

## References

See `references/SOURCES.md`.

## gRPC Security Testing Workflow

### Step 1: gRPC 服务发现 (Endpoint Discovery)

gRPC uses HTTP/2 with `content-type: application/grpc`. Standard HTTP scanners often miss gRPC endpoints.

**Discovery techniques:**
- Look for `application/grpc` in HTTP response headers or JS bundle
- Common paths: `/package.Service/Method`, grpc-web proxy at `/grpcweb/`
- Check if gRPC Reflection API is enabled:
  ```bash
  grpcurl -plaintext target:50051 list
  grpcurl -plaintext target:50051 describe
  ```
- For gRPC-Web (browser-compatible): look for `grpc-web` content type, Envoy proxy paths

### Step 2: Reflection API 枚举 (If Enabled)

When gRPC reflection is enabled (common in dev/staging), the service self-describes:

```bash
# List all services
grpcurl -plaintext target:50051 list

# Describe a service (no proto file needed)
grpcurl -plaintext target:50051 describe myapp.UserService

# Call a method
grpcurl -plaintext -d '{"user_id": "1"}' target:50051 myapp.UserService/GetUser
```

### Step 3: 认证与授权测试 (Auth Testing)

gRPC auth is typically handled via:
- **TLS**: check if TLS is enforced or optional (`grpcurl -insecure`)
- **Token/Cert metadata**: JWT, OAuth, mTLS — test if metadata can be omitted or tampered
- **Per-method authorization**: each gRPC method requires independent auth check — common bug: gRPC service checks auth only on first call in a stream

**Test cases:**
1. Call without auth metadata: `grpcurl -plaintext target:50051 myapp.AdminService/DeleteUser`
2. Call with empty/tampered token: `grpcurl -H 'authorization: Bearer invalid' ...`
3. Reuse token from one service on another service
4. Call internal-only methods that are not exposed via gRPC-Web proxy
5. Check if streaming methods have per-message authorization (not just per-stream)

### Step 4: 参数注入 (Protobuf Tampering)

gRPC uses protobuf serialization — not HTTP forms. Key injection surfaces:

1. **Field-level injection**: gRPC services often pass protobuf fields directly to backend (SQL, command execution, file operations)
   ```bash
   grpcurl -d '{"query": "'\'' OR 1=1--"}' target:50051 myapp.SearchService/Search
   ```

2. **Integer overflow/underflow**: protobuf int32/int64 fields — test boundary values
   ```json
   {"amount": -1, "quantity": 9223372036854775807}
   ```

3. **Repeated field abuse**: send massive repeated fields → memory exhaustion
   ```json
   {"ids": [1,1,1,...10000 entries]}
   ```

4. **Unknown field injection**: add extra fields not in the proto definition — some implementations process them, some crash

5. **Default value bypass**: protobuf treats 0/false/"" as default and may omit them in serialization — test if default-vs-missing distinction leads to logic bugs

### Step 5: gRPC-Web 测试 (Browser-facing)

gRPC-Web is the browser-compatible proxy layer (usually Envoy). It translates HTTP/1.1 ↔ gRPC/HTTP/2.

**Common issues:**
- gRPC-Web proxy exposes internal gRPC methods to the browser
- Proxy bypass: call the gRPC backend directly on its HTTP/2 port, skipping gRPC-Web auth
- Content-type smuggling between gRPC-Web and gRPC layers
- CORS misconfiguration on the gRPC-Web proxy

### Step 6: DoS / Stream Abuse

gRPC supports four method types:
- Unary (1 request → 1 response)
- Server streaming (1 request → N responses)
- Client streaming (N requests → 1 response)
- Bidirectional streaming (N requests → N responses)

**Test for:**
- Client streaming: send infinite stream → server OOM
- Bidirectional: open many concurrent bidirectional streams → connection exhaustion
- Flow control bypass: ignore server flow control window
- gRPC deadlines: send request without deadline → server hangs indefinitely

## Key Tools

| Tool | Purpose |
|------|---------|
| `grpcurl` | Command-line gRPC client (like curl for gRPC) |
| `grpcui` | Interactive gRPC UI (like Postman for gRPC) |
| `evans` | Interactive gRPC REPL client |
| `mitmproxy` | gRPC traffic interception (requires HTTP/2 MITM) |
| Burp Suite | HTTP/2 + gRPC traffic (Burp 2020.11+) |
| `protoc` + custom scripts | Build ad-hoc clients for fuzzing |

## Important Agent Rules

- ⛔ gRPC testing requires understanding the proto schema — use reflection or extract from client binaries
- ⛔ Streaming methods can consume server resources — close streams immediately after verification
- Only operate in authorized environments
