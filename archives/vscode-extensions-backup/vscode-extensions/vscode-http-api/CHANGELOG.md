# Changelog for VSCode HTTP API Extension

All notable changes to this project are documented in this file.


## [Unreleased]

- feat: Add audit logging (JSONL) for most state-changing endpoints (open/edit/create/delete/commit/exec/settings/experimental/yolo)
- feat: Add GET /audit to fetch last N entries or a single entry by id
- feat: Add POST /rollback to revert changes recorded in an audit entry (requires `vscodeHttpApi.masterAutoApprove=true`)
- feat: Add preview/apply flags to settings and extension toggle endpoints (`apply: true`) and record `prev` values for rollbacks
- chore: Add CLI examples & `examples/audit_tool.js` to list/get/rollback audit entries
- docs: Update README with audit and rollback usage examples and `apply` behavior

