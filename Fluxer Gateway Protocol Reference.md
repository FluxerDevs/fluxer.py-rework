# Fluxer Gateway Protocol & Python Wrapper Reference

This document serves as the comprehensive technical reference for the Fluxer Gateway. It covers the underlying protocol, the server's architectural context, and a deep-dive implementation guide for building a robust, async Python wrapper.

---

## 1. Connection & Transport Layer

**Endpoint:** 
Connections are made via WebSocket to the root path (`/`) on the gateway's host and port.

**Query Parameters:**
*   `v=1`: The API version. Only version 1 is supported. Connecting with any other version will result in the socket closing with an `invalid_api_version` code.
*   `encoding=json`: The gateway expects JSON payloads. (Note: An `etf` parameter is defined in the protocol, but only JSON is fully wired and supported by the internal codecs).
*   `compress=zstd-stream&stream=true`: Enables Zstandard streaming compression. If omitted, or if `compress=none` is passed, the traffic remains uncompressed. 

**Transport Notes for Python:**
To handle `zstd-stream`, your Python wrapper must use a streaming decompressor (e.g., `zstandard.ZstdDecompressor().decompressobj()`) that continuously feeds chunked WebSocket bytes and extracts the decoded JSON string.

---

## 2. Opcodes & Payload Architecture

All messages follow a base JSON payload structure:
*   `op` (integer): The opcode indicating the message type.
*   `d` (mixed): The event data payload.
*   `s` (integer, optional): The sequence number (only present in Dispatch).
*   `t` (string, optional): The event name (only present in Dispatch).

### Opcode Dictionary

| Op | Name | Direction | Description |
|----|------|-----------|-------------|
| 0 | Dispatch | Server → Client | Core event dispatch containing `t` (event name) and `s` (sequence). |
| 1 | Heartbeat | Client → Server | Client keepalive ping. |
| 2 | Identify | Client → Server | Initial authentication and session establishment. |
| 3 | Presence Update | Client → Server | Updates the client's online status and activity. |
| 4 | Voice State Update | Client → Server | Connect/disconnect/move voice channels (Rate-limited to 2/sec). |
| 5 | Voice Server Ping | Client → Server | Voice RTC signaling ping. |
| 6 | Resume | Client → Server | Attempt to recover a dropped session using `{token, session_id, seq}`. |
| 7 | Reconnect | Server → Client | Server instructs the client to reconnect immediately. |
| 8 | Request Guild Members | Client → Server | Fetch offline or bulk member lists. |
| 9 | Invalid Session | Server → Client | Rejection of a session (e.g., failed resume). `d: false` means start over. |
| 10 | Hello | Server → Client | Sent immediately upon connection, containing `heartbeat_interval`. |
| 11 | Heartbeat Ack | Server → Client | Server acknowledges the client's heartbeat. |
| 12 | Gateway Error | Server → Client | Contains structured gateway error data. |
| 14 | Lazy Request | Client → Server | Fetch unified guild subscriptions and lazy loading states. |
| 15 | Request Guild Counts | Client → Server | Fetch member and guild statistics. |
| 16 | Request Channel Member Counts| Client → Server | Fetch targeted member metrics for a channel. |

*(Note: Opcode 13 is skipped to align identically with standard Discord gateway numbering).*

---

## 3. The Connection Lifecycle & State Machine

A robust Python wrapper must implement a state machine that handles the following flow non-blockingly (e.g., using `asyncio`).

### A. The Handshake
1.  **Connect** to the WebSocket.
2.  **Await `Hello` (Op 10)**: Extract `d["heartbeat_interval"]` (typically 41250 ms).
3.  **Start Heartbeater**: Launch a background async task that sends `Op 1` (Heartbeat) repeatedly at the defined interval.
4.  **Send `Identify` (Op 2)**: Payload must contain:
    ```json
    {
      "token": "YOUR_TOKEN",
      "properties": {
        "os": "linux",
        "browser": "my_python_library",
        "device": "my_python_library"
      },
      "presence": {...}, 
      "ignored_events": [...],
      "flags": 0,
      "shard": [0, 1]
    }
    ```
5.  **Await `READY` (Op 0)**: Extract the `session_id`.

### B. Session Tracking
*   Every time an `Op 0 (Dispatch)` is received, cache the sequence number `s`. 

### C. Disconnects & Resumes
*   If the socket closes (e.g., network drop, or server sends Op 7 Reconnect), establish a new WebSocket connection.
*   Wait for the new `Hello` (Op 10).
*   Send **`Resume` (Op 6)** using your cached data: `{ "token": "...", "session_id": "...", "seq": 1234 }`.
*   If accepted, the server replies with a `RESUMED` dispatch. If rejected (e.g., session expired), the server sends `Op 9 (Invalid Session)` and closes the socket. The wrapper must then clear its session cache and send a full `Identify`.

---

## 4. Close Codes & Error Handling

When the WebSocket closes, the Gateway provides specific codes:
*   `4000`: Unknown error
*   `4001`: Unknown opcode
*   `4002`: Decode error (Invalid payload shape or oversized)
*   `4003`: Not authenticated (Payload sent before Identify)
*   `4004`: Authentication failed (Invalid token)
*   `4005`: Already authenticated
*   `4007`: Invalid sequence
*   `4008`: Rate limited
*   `4009`: Session timeout
*   `4010`: Invalid shard
*   `4011`: Sharding required
*   `4012`: Invalid API version
*   `4013`: Ack backpressure

---

## 5. Dispatch Events (Op 0)

Fluxer Gateway overlaps heavily with standard chat gateway specs but introduces specific events. Your wrapper's event router (PubSub) must accommodate these.

**Standard Overlaps:**
*   `READY`, `RESUMED`
*   `GUILD_CREATE`, `GUILD_UPDATE`, `GUILD_DELETE`
*   `GUILD_MEMBER_ADD`, `GUILD_MEMBER_UPDATE`, `GUILD_MEMBER_REMOVE`
*   `CHANNEL_CREATE`, `CHANNEL_UPDATE`, `CHANNEL_DELETE`
*   `MESSAGE_CREATE`, `MESSAGE_UPDATE`, `MESSAGE_DELETE`, `MESSAGE_DELETE_BULK`
*   `MESSAGE_REACTION_ADD`, `MESSAGE_REACTION_REMOVE`
*   `TYPING_START`
*   `PRESENCE_UPDATE`, `VOICE_STATE_UPDATE`, `VOICE_SERVER_UPDATE`

**Fluxer-Specific Events:**
*   `GUILD_MEMBER_LIST_UPDATE`: Used for lazy member list synchronization (powered by the internal Oset NIF).
*   `RELATIONSHIP_ADD`, `RELATIONSHIP_REMOVE`, `RELATIONSHIP_UPDATE`
*   `FAVORITE_MEME_ADD`, `FAVORITE_MEME_REMOVE`
*   `SAVED_MESSAGE_ADD`, `SAVED_MESSAGE_REMOVE`
*   `RECENT_MENTION_DELETE`
*   `ENTRANCE_SOUND_PLAY`
*   `AUTH_SESSION_CHANGE`
*   `WEBAUTHN_CREDENTIALS_UPDATE`
*   `USER_GUILD_SETTINGS_UPDATE`
*   `USER_PINNED_DMS_UPDATE`
*   `USER_CONNECTIONS_UPDATE`
*   `CHANNEL_UPDATE_BULK`
*   `GUILD_ROLE_UPDATE_BULK`

---

## 6. Wrapper Implementation Constraints & Internal Architecture

Understanding the server's Erlang/Rust architecture ensures your Python wrapper respects system boundaries.

### Rate Limiting & Voice Queues
*   **Voice State Updates (`Op 4`):** Rate-limited to **2 per second**. If your Python client attempts to quickly join/move channels, the server will queue these or potentially drop/throttle the connection. Your wrapper *must* implement an `asyncio.Queue` for outbound `Op 4` payloads with a strict `0.5s` delay between emissions.

### Internal Concurrency & Backpressure
*   The Fluxer server utilizes a high-performance **Dispatch Relay** (`gateway_dispatch_relay.erl`) with a sharded worker pool. If the server experiences heavy load, it relies on backpressure. If your Python client does not read from the WebSocket fast enough (e.g., blocking the event loop), the server will terminate the connection with `4013: Ack backpressure`.
*   *Actionable Fix:* Ensure your WebSocket `recv()` loop does zero heavy lifting. It should parse JSON and immediately dispatch it to `asyncio.create_task()` or an `asyncio.Queue` worker pool.

### High-Performance Rust NIFs
*   The server uses Rust Native Implemented Functions (NIFs) to process large datasets quickly, such as Markdown plaintext extraction (`push_markdown_plaintext_nif`) and large guild member list sets (`guild_member_list_oset_nif`). 
*   Because the server processes these instantly, expect rapid, large payload bursts when requesting guild members (`Op 8`) or lazy requesting (`Op 14`). Your JSON parser (e.g., `orjson` or `ujson` in Python) must be highly optimized.

### Cluster Handoffs
*   The Gateway operates in a distributed cluster (`gateway_cluster_handoff.erl`). 
*   During maintenance or scaling, you may receive an `Op 7 Reconnect`. 
*   The server's `gateway_event_pause.erl` might temporarily freeze event dispatches during these node handoffs. Your client should not assume the connection is dead if events stop flowing for a few seconds, provided Heartbeat Acks (`Op 11`) are still being received.