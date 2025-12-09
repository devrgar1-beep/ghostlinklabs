#!/bin/bash
# GhostLink Wiki - macOS Spotlight Integration
# Makes wiki content searchable via Spotlight (Cmd+Space)

set -e

WIKI_DIR="$HOME/ghostlink-wiki-organized"
PLIST_PATH="$HOME/Library/Preferences/com.apple.spotlight.plist"

echo "=================================================="
echo "  GHOSTLINK WIKI - SPOTLIGHT INTEGRATION"
echo "=================================================="

# Check if organized wiki exists
if [ ! -d "$WIKI_DIR" ]; then
    echo "❌ Organized wiki not found at: $WIKI_DIR"
    echo "Run organize_wiki.py first"
    exit 1
fi

echo "✅ Wiki found at: $WIKI_DIR"

# Add wiki to Spotlight index
echo "📍 Adding wiki to Spotlight index..."
mdimport -i "$WIKI_DIR"

# Wait a moment for indexing
sleep 2

# Check if indexed
echo "🔄 Verifying Spotlight indexing..."
mdfind -onlyin "$WIKI_DIR" "kMDItemDisplayName != ''" | head -5

# Add metadata to wiki files for better search
echo "🏷️  Adding metadata tags..."
tag -a "ghostlink,wiki,code" "$WIKI_DIR"

# Create .plist for custom metadata
echo "📝 Creating metadata importer config..."
mkdir -p "$HOME/Library/Spotlight"

cat > "$HOME/Library/Spotlight/GhostLink.mdimporter.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>LSItemContentTypes</key>
            <array>
                <string>public.python-script</string>
                <string>public.javascript-source</string>
                <string>public.typescript-source</string>
                <string>public.plain-text</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
EOF

echo "✅ Spotlight integration complete!"
echo ""
echo "You can now search wiki content with:"
echo "  Cmd+Space → type 'ghostlink' or code keywords"
echo "  Finder → search 'tag:ghostlink'"
echo ""
