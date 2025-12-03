# Breaking Changes - GhostLink Repository Upgrades

## Overview
This document details breaking changes introduced in the comprehensive repository upgrade. Most changes are backward compatible, but some require action from users.

## Breaking Changes

### 1. Python 3.8 Support Dropped (BREAKING)

**Affected File:** `pyproject.toml`  
**Change:** `requires-python` updated from `>=3.8` to `>=3.9`

#### Impact
Users running Python 3.8 will no longer be able to install or use GhostLink.

#### Rationale
- Python 3.8 reached **End of Life on October 7, 2024**
- No longer receives security updates
- Python 3.9 has been stable since October 2020 (4+ years)
- Allows use of modern Python features and security fixes

#### Migration Path
1. **Check your Python version:**
   ```bash
   python --version
   ```

2. **If Python 3.8, upgrade to Python 3.9 or later:**
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install python3.9 python3.9-venv
   ```
   
   **macOS (Homebrew):**
   ```bash
   brew install python@3.9
   ```
   
   **Windows:**
   - Download from https://www.python.org/downloads/
   - Install Python 3.9 or later
   
3. **Recreate virtual environment:**
   ```bash
   rm -rf venv  # or your venv directory
   python3.9 -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

#### Timeline
- **Now:** Python 3.9 minimum enforced
- **October 2025:** Python 3.9 reaches EOL (plan for Python 3.10 minimum)
- **October 2026:** Python 3.10 reaches EOL (plan for Python 3.11 minimum)

### 2. VSCode 1.85.0 Minimum Required (POTENTIALLY BREAKING)

**Affected File:** `vscode-extensions/ghostlink-vscode/package.json`  
**Change:** `engines.vscode` updated from `^1.74.0` to `^1.85.0`

#### Impact
Users with VSCode older than version 1.85.0 cannot use the GhostLink extension.

#### Rationale
- VSCode 1.74.0 released December 2022 (2+ years old)
- VSCode 1.85.0 released November 2023 (1+ year old)
- Enables use of modern VSCode APIs
- Improves TypeScript and ESLint integration

#### Migration Path
1. **Check your VSCode version:**
   - Open VSCode
   - Go to Help → About
   - Look for version number

2. **If older than 1.85.0, update VSCode:**
   - VSCode typically auto-updates
   - Manual update: Help → Check for Updates
   - Or download from https://code.visualstudio.com/

3. **Verify extension compatibility:**
   ```bash
   cd vscode-extensions/ghostlink-vscode
   npm install
   npm run compile
   ```

#### Notes
- VSCode updates are typically painless and automatic
- Version 1.85.0 is now over 1 year old (widely adopted)
- No known API breaking changes affecting GhostLink

### 3. ESLint 9 Configuration Format (DEVELOPMENT ONLY)

**Affected Files:** 
- `vscode-extensions/ghostlink-vscode/package.json`
- `vscode-extensions/ghostlink-vscode/eslint.config.mjs` (NEW)

**Change:** ESLint updated from 8.28.0 to 9.17.0

#### Impact
**Development only** - Does not affect end users.

Developers must:
1. Use new flat config format (`eslint.config.mjs`)
2. Update ESLint VS Code extension
3. Adjust any custom ESLint rules

#### Rationale
- ESLint 8 is deprecated
- ESLint 9 is faster and more maintainable
- Flat config is simpler and more explicit

#### Migration Path
For developers contributing to GhostLink:

1. **Install updated dependencies:**
   ```bash
   cd vscode-extensions/ghostlink-vscode
   npm install
   ```

2. **ESLint config already migrated** - `eslint.config.mjs` provided

3. **Update ESLint VS Code extension:**
   - In VSCode, go to Extensions
   - Search for "ESLint"
   - Update to latest version

4. **Test linting:**
   ```bash
   npm run lint
   ```

#### Notes
- End users unaffected (compiled code unchanged)
- Only affects developers modifying extension code
- Migration guide: https://eslint.org/docs/latest/use/configure/migration-guide

## Non-Breaking Changes

### Dependency Version Increases
All other dependency updates are **backward compatible**:
- Python packages (psutil, requests) - no API changes
- TypeScript - backward compatible compilation
- Pre-commit hooks - compatible with existing configs
- Docker images - same Python API
- NATS - protocol compatible

### Automated Updates
Dependabot configuration is **completely non-breaking**:
- Creates PRs for review (you control merging)
- No automatic updates without approval
- Can be disabled in `.github/dependabot.yml`

## Compatibility Matrix

| Component | Old Version | New Version | Breaking? | Action Required |
|-----------|-------------|-------------|-----------|-----------------|
| Python | >=3.8 | >=3.9 | ✅ YES | Upgrade to Python 3.9+ |
| VSCode | >=1.74.0 | >=1.85.0 | ⚠️ MAYBE | Update VSCode (likely auto-updated) |
| psutil | >=5.9.0 | >=6.1.1 | ❌ NO | None (pip handles it) |
| requests | >=2.31.0 | >=2.32.5 | ❌ NO | None (pip handles it) |
| Docker Base | 3.11-slim | 3.12-slim | ❌ NO | None (rebuild image) |
| NATS | 2.10 | 2.11 | ❌ NO | None (compatible) |
| ESLint | 8.28.0 | 9.17.0 | ⚠️ DEV ONLY | Update if developing extension |

## Rollback Instructions

If you need to rollback to previous versions:

### Full Rollback
```bash
git checkout HEAD~4  # Go back 4 commits before upgrades
pip install -r requirements.txt
```

### Selective Rollback
```bash
# Keep on current branch but use old requirements
echo "psutil>=5.9.0" > requirements.txt.old
echo "requests>=2.31.0" >> requirements.txt.old
pip install -r requirements.txt.old
```

### Restore Python 3.8 Support
Edit `pyproject.toml`:
```toml
requires-python = ">=3.8"
```

**Note:** Not recommended due to Python 3.8 EOL and security concerns.

## Testing Recommendations

After upgrading:

### For End Users
1. **Test Python installation:**
   ```bash
   python --version  # Should be 3.9+
   pip install -r requirements.txt
   python -c "import psutil, requests; print('OK')"
   ```

2. **Test main application:**
   ```bash
   python main.py  # or your entry point
   ```

3. **Run test suite:**
   ```bash
   pytest  # or your test command
   ```

### For Developers
1. **Test VSCode extension:**
   ```bash
   cd vscode-extensions/ghostlink-vscode
   npm install
   npm run compile
   npm run lint
   ```

2. **Test Docker build:**
   ```bash
   docker build -f docker/Dockerfile -t ghostlink:test .
   docker run --rm ghostlink:test python --version  # Should show 3.12.x
   ```

3. **Test CI/CD:**
   - Push to branch
   - Verify GitHub Actions pass
   - Check Dependabot setup

## Support

### Getting Help
If you encounter issues:

1. **Check this document** for migration guidance
2. **Review UPGRADE_SUMMARY.md** for technical details
3. **Open a GitHub issue** with:
   - Your Python version (`python --version`)
   - Your VSCode version (if using extension)
   - Error messages
   - Steps to reproduce

### Reporting Bugs
If you find bugs related to upgrades:

1. Verify it's not a pre-existing issue
2. Test with rollback to confirm it's upgrade-related
3. Include version information
4. Provide minimal reproduction case

## Deprecation Timeline

### Current (December 2025)
- ❌ Python 3.8 support removed (EOL October 2024)
- ✅ Python 3.9+ required

### Future (October 2025)
- ⚠️ Python 3.9 reaches EOL
- 📋 Plan migration to Python 3.10 minimum

### Future (October 2026)
- ⚠️ Python 3.10 reaches EOL
- 📋 Plan migration to Python 3.11 minimum

## Conclusion

Most users will experience a **seamless upgrade** with significant security and performance benefits. The main breaking change (Python 3.8 support dropped) affects users on an EOL Python version who should upgrade for security reasons anyway.

For the small number of affected users, clear migration paths are provided above.

---

**Document Version:** 1.0  
**Last Updated:** December 3, 2025  
**Related Documents:** UPGRADE_SUMMARY.md, README.md
