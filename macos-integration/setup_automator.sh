#!/bin/bash
# Setup Automator Quick Actions for GhostLink Wiki

set -e

WORKFLOW_DIR="$HOME/Library/Services"
mkdir -p "$WORKFLOW_DIR"

echo "=================================================="
echo "  GHOSTLINK WIKI - AUTOMATOR SETUP"
echo "=================================================="

# Create "Search GhostLink Wiki" service
cat > "$WORKFLOW_DIR/Search GhostLink Wiki.workflow/Contents/document.wflow" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>AMApplicationBuild</key>
    <string>523</string>
    <key>AMApplicationVersion</key>
    <string>2.10</string>
    <key>actions</key>
    <array>
        <dict>
            <key>action</key>
            <dict>
                <key>AMAccepts</key>
                <dict>
                    <key>Container</key>
                    <string>List</string>
                    <key>Optional</key>
                    <true/>
                    <key>Types</key>
                    <array>
                        <string>com.apple.cocoa.string</string>
                    </array>
                </dict>
                <key>AMActionVersion</key>
                <string>2.0.3</string>
                <key>AMApplication</key>
                <array>
                    <string>Automator</string>
                </array>
                <key>AMParameterProperties</key>
                <dict>
                    <key>COMMAND_STRING</key>
                    <dict/>
                </dict>
                <key>AMProvides</key>
                <dict>
                    <key>Container</key>
                    <string>List</string>
                    <key>Types</key>
                    <array>
                        <string>com.apple.cocoa.string</string>
                    </array>
                </dict>
                <key>ActionBundlePath</key>
                <string>/System/Library/Automator/Run Shell Script.action</string>
                <key>ActionName</key>
                <string>Run Shell Script</string>
                <key>ActionParameters</key>
                <dict>
                    <key>COMMAND_STRING</key>
                    <string>#!/bin/bash
wiki_dir="$HOME/ghostlink-wiki-organized"
search_term="$1"

if command -v rg &> /dev/null; then
    rg --no-heading --line-number "$search_term" "$wiki_dir" | head -20
else
    grep -rn "$search_term" "$wiki_dir" | head -20
fi
</string>
                    <key>CheckedForUserDefaultShell</key>
                    <true/>
                    <key>inputMethod</key>
                    <integer>1</integer>
                    <key>shell</key>
                    <string>/bin/bash</string>
                </dict>
            </dict>
        </dict>
    </array>
</dict>
</plist>
EOF

# Create "Open in GhostLink Wiki" service
cat > "$WORKFLOW_DIR/Open in GhostLink Wiki.workflow/Contents/document.wflow" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>actions</key>
    <array>
        <dict>
            <key>action</key>
            <dict>
                <key>ActionParameters</key>
                <dict>
                    <key>COMMAND_STRING</key>
                    <string>#!/bin/bash
open "$HOME/ghostlink-wiki-organized"
</string>
                </dict>
            </dict>
        </dict>
    </array>
</dict>
</plist>
EOF

echo "✅ Automator services created!"
echo ""
echo "Available services:"
echo "  1. Right-click text → Services → 'Search GhostLink Wiki'"
echo "  2. Right-click anywhere → Services → 'Open in GhostLink Wiki'"
echo ""
echo "Restart apps for services to appear"
