#!/usr/bin/osascript
# GhostLink Quick Actions for macOS
# Right-click file → Services → "Search in GhostLink Wiki"

on run {input, parameters}
    set searchTerm to text returned of (display dialog "Search GhostLink Wiki for:" default answer "")
    set wikiPath to (POSIX path of (path to home folder)) & "ghostlink-wiki-organized"
    
    -- Use ripgrep if available, otherwise grep
    try
        set results to do shell script "rg --no-heading --line-number '" & searchTerm & "' " & quoted form of wikiPath
    on error
        set results to do shell script "grep -rn '" & searchTerm & "' " & quoted form of wikiPath
    end try
    
    -- Display results
    display dialog results buttons {"OK"} default button 1 with title "GhostLink Wiki Search Results"
    
    return input
end run
