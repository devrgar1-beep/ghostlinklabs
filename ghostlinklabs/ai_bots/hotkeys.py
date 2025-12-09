#!/usr/bin/env python3
"""
Hotkey handler for GhostLink AI bots
System-level keyboard event capture for macOS
"""
import asyncio
from typing import Callable, Dict, Optional

try:
    from pynput import keyboard
except ImportError:
    keyboard = None


class HotkeyHandler:
    """
    Captures system-level keyboard events for bot hotkeys
    Uses pynput for cross-platform support
    """
    
    def __init__(self):
        self.hotkeys: Dict[str, Callable] = {}
        self.listener: Optional[keyboard.Listener] = None
        self.current_keys = set()
        self.running = False
        
    def register(self, hotkey: str, callback: Callable):
        """
        Register hotkey callback
        Format: "ctrl+shift+s", "alt+m", etc.
        """
        normalized = self._normalize_hotkey(hotkey)
        self.hotkeys[normalized] = callback
        
    def unregister(self, hotkey: str):
        """Unregister hotkey"""
        normalized = self._normalize_hotkey(hotkey)
        if normalized in self.hotkeys:
            del self.hotkeys[normalized]
            
    def _normalize_hotkey(self, hotkey: str) -> str:
        """Normalize hotkey string"""
        parts = [p.strip().lower() for p in hotkey.split("+")]
        
        # Map common variants
        mapping = {
            "control": "ctrl",
            "command": "cmd",
            "option": "alt",
            "return": "enter",
        }
        
        normalized = []
        for part in parts:
            normalized.append(mapping.get(part, part))
            
        # Sort modifiers, keep key last
        modifiers = []
        key = None
        
        for item in normalized:
            if item in ["ctrl", "shift", "alt", "cmd"]:
                modifiers.append(item)
            else:
                key = item
                
        modifiers.sort()
        if key:
            modifiers.append(key)
            
        return "+".join(modifiers)
        
    def _get_key_name(self, key) -> str:
        """Get normalized key name"""
        try:
            if hasattr(key, "char") and key.char:
                return key.char.lower()
            elif hasattr(key, "name"):
                name = key.name.lower()
                # Map special keys
                mapping = {
                    "ctrl_l": "ctrl",
                    "ctrl_r": "ctrl",
                    "shift_l": "shift",
                    "shift_r": "shift",
                    "alt_l": "alt",
                    "alt_r": "alt",
                    "cmd_l": "cmd",
                    "cmd_r": "cmd",
                }
                return mapping.get(name, name)
        except AttributeError:
            pass
        return str(key).lower()
        
    def _on_press(self, key):
        """Handle key press"""
        key_name = self._get_key_name(key)
        self.current_keys.add(key_name)
        self._check_hotkeys()
        
    def _on_release(self, key):
        """Handle key release"""
        key_name = self._get_key_name(key)
        if key_name in self.current_keys:
            self.current_keys.remove(key_name)
            
    def _check_hotkeys(self):
        """Check if current key combination matches any hotkey"""
        # Build current combination
        sorted_keys = sorted(self.current_keys)
        combo = "+".join(sorted_keys)
        
        # Check for match
        if combo in self.hotkeys:
            callback = self.hotkeys[combo]
            # Run callback in thread-safe way
            asyncio.create_task(callback())
            
    def start(self):
        """Start listening for hotkeys"""
        if keyboard is None:
            raise RuntimeError(
                "pynput not installed. "
                "Install with: pip install pynput"
            )
            
        if self.running:
            return
            
        self.running = True
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()
        
    def stop(self):
        """Stop listening"""
        if self.listener:
            self.listener.stop()
            self.listener = None
        self.running = False
        self.current_keys.clear()


async def demo():
    """Demo hotkey handler"""
    handler = HotkeyHandler()
    
    async def on_status():
        print("Status hotkey pressed!")
        
    async def on_restart():
        print("Restart hotkey pressed!")
        
    handler.register("ctrl+shift+s", on_status)
    handler.register("ctrl+shift+r", on_restart)
    
    print("Hotkey handler demo")
    print("Press ctrl+shift+s or ctrl+shift+r")
    print("Press ctrl+c to exit")
    
    handler.start()
    
    try:
        while True:
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        handler.stop()


if __name__ == "__main__":
    asyncio.run(demo())
