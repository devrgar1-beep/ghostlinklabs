# DriftGuard

DriftGuard is a monitoring and enforcement node responsible for detecting and preventing symbolic and functional drift across GhostLink systems.

## Responsibilities

- Receive heartbeat pings and maintain a last-seen timestamp
- Analyze payloads for drift indicators (duplicate metadata, temporal anomalies)
- Emit events (`drift_detected`, `drift_resolved`) for upstream listeners
- Provide a safe, auditable interface for quarantining components

## Implementation Notes

- Minimal implementation exists in `src/ghostlinklabs/ghostlink/modules/driftguard.py`
- Heartbeat helper available in `src/ghostlinklabs/ghostlink/modules/heartbeat.py`

## Operational Parameters

- Default heartbeat interval: 7s (configurable)
- Acceptable interval range: 1-60s

## Audit & Logging

- All findings must be logged to `logs/driftguard.log`
- Findings must include causal metadata and a unique event id
