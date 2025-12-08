#!/bin/bash
# GhostLink Wireshark Build Script

echo "🔧 Building GhostLink Wireshark - Custom Protocol Analyzer..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

echo "🐍 Python 3 found: $(python3 --version)"

# Check tkinter (for GUI)
python3 -c "import tkinter" &> /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Tkinter available for GUI"
else
    echo "⚠️  Tkinter not available - GUI will not work"
fi

# Make scripts executable
chmod +x ghostlink_analyzer.py
chmod +x ghostlink_wireshark_gui.py

echo "📦 Installation complete!"
echo ""
echo "🚀 Usage:"
echo "  CLI Mode:    python3 ghostlink_analyzer.py"
echo "  GUI Mode:    python3 ghostlink_wireshark_gui.py"
echo "  Test Data:   python3 ghostlink_analyzer.py --generate-test"
echo ""
echo "📡 Default listening port: 9999"
echo "🔍 Features:"
echo "  - Real-time packet capture"
echo "  - GhostLink protocol dissection"
echo "  - Statistics and analysis"
echo "  - Test packet generation"
echo "  - GUI and CLI interfaces"
echo ""
echo "🎉 GhostLink Wireshark is ready!"
