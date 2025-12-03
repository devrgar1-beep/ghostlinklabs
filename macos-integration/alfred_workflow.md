# GhostLink Wiki - Alfred Workflow

**Requirement:** [Alfred 5](https://www.alfredapp.com/) with Powerpack

## Installation

1. **Create new workflow** in Alfred Preferences → Workflows
2. **Add Script Filter:**
   - Keyword: `glwiki`
   - Title: `GhostLink Wiki Search`
   - Script Language: `/bin/bash`

## Script Filter Code

```bash
#!/bin/bash

query="{query}"
wiki_dir="$HOME/ghostlink-wiki-organized"

# Search using ripgrep (fast) or grep (fallback)
if command -v rg &> /dev/null; then
    results=$(rg --no-heading --line-number --max-count 10 "$query" "$wiki_dir" 2>/dev/null || true)
else
    results=$(grep -rn --max-count=10 "$query" "$wiki_dir" 2>/dev/null || true)
fi

# Format for Alfred JSON
cat << EOF
{
  "items": [
EOF

first=true
while IFS= read -r line; do
    if [ -n "$line" ]; then
        file=$(echo "$line" | cut -d: -f1)
        linenum=$(echo "$line" | cut -d: -f2)
        content=$(echo "$line" | cut -d: -f3-)
        filename=$(basename "$file")
        
        [ "$first" = false ] && echo ","
        
        cat << ITEM
    {
      "uid": "$file:$linenum",
      "title": "$filename:$linenum",
      "subtitle": "$content",
      "arg": "$file",
      "autocomplete": "$filename",
      "icon": {
        "path": "$file"
      }
    }
ITEM
        first=false
    fi
done <<< "$results"

cat << EOF
  ]
}
EOF
```

## Actions

### 1. Open in VSCode
- **Type:** Run Script
- **Script:**
```bash
code --goto "{query}"
```

### 2. Open in Finder
- **Type:** Run Script  
- **Script:**
```bash
open -R "{query}"
```

### 3. Copy Path
- **Type:** Copy to Clipboard
- **Text:** `{query}`

## Usage

1. Press `Option+Space` (or your Alfred hotkey)
2. Type `glwiki` followed by search term
3. Select result and press:
   - `Enter` → Open in VSCode
   - `Cmd+Enter` → Show in Finder
   - `Cmd+C` → Copy file path

## Examples

```
glwiki ghostlink_main
glwiki consciousness daemon
glwiki lattice QCL
glwiki docker compose
```

## Advanced Features

### File Type Filter
```
glwiki .py authentication
glwiki .js WebSocket
glwiki .md setup guide
```

### Category Search
```
glwiki /core-runtime
glwiki /mcp-servers
glwiki /infrastructure
```

## Hotkeys (Optional)

Add workflow hotkeys:
- `Cmd+Shift+G` → Open wiki folder in Finder
- `Cmd+Option+G` → Search wiki from clipboard
- `Cmd+Ctrl+G` → Quick search current selection
