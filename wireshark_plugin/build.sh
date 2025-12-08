#!/bin/bash
# GhostLink Wireshark Plugin Build Script

echo "🔧 Building GhostLink Wireshark Plugin..."

# Check if Wireshark is installed
if ! command -v wireshark &> /dev/null && ! command -v /Applications/Wireshark.app/Contents/MacOS/Wireshark &> /dev/null; then
    echo "⚠️  Wireshark not found. Please install Wireshark first."
    echo "   macOS: brew install --cask wireshark"
    echo "   Ubuntu: sudo apt install wireshark"
    exit 1
fi

# Determine Wireshark plugins directory
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    WIRESHARK_DIR="/Applications/Wireshark.app/Contents/PlugIns/wireshark/"
    PERSONAL_DIR="$HOME/.wireshark/plugins/"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    WIRESHARK_DIR="/usr/lib/wireshark/plugins/"
    PERSONAL_DIR="$HOME/.local/lib/wireshark/plugins/"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

echo "📍 Detected OS: $OSTYPE"
echo "📂 System plugins dir: $WIRESHARK_DIR"
echo "📂 Personal plugins dir: $PERSONAL_DIR"

# Create personal plugins directory if it doesn't exist
mkdir -p "$PERSONAL_DIR"

# Copy the dissector
cp ghostlink_dissector.lua "$PERSONAL_DIR/"

if [ $? -eq 0 ]; then
    echo "✅ Plugin installed to: $PERSONAL_DIR"
    echo "🔄 Please restart Wireshark to load the plugin"
    echo ""
    echo "📋 To test the plugin:"
    echo "1. Start Wireshark"
    echo "2. Capture on port 9999 (or modify dissector for your port)"
    echo "3. Send GhostLink packets"
    echo "4. Look for 'GHOSTLINK' protocol in packet list"
else
    echo "❌ Failed to install plugin"
    exit 1
fi

echo ""
echo "🎉 GhostLink Wireshark Plugin build complete!"
echo "📖 See README.md for usage instructions"
