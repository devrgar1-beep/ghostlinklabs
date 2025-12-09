#!/bin/bash
# GhostLink Shell Layer - Add to ~/.zshrc or ~/.bashrc

# Core routing function
ghostlink() {
  local cmd="$*"
  local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  
  echo "[$timestamp] SPAWN: $cmd" >> ~/.ghostlink_log
  
  # Execute
  eval "$cmd"
  local exit_code=$?
  
  # Collapse
  echo -n "Collapse? [s=SIGMA, x=SCAR, c=COMPOST, enter=skip]: "
  read -r response
  
  case "$response" in
    s|S)
      echo "[$timestamp] SIGMA: $cmd" >> ~/.ghostlink_sigma
      ;;
    x|X)
      echo "[$timestamp] SCAR: $cmd (exit: $exit_code)" >> ~/.ghostlink_scars
      ;;
    c|C)
      echo "[$timestamp] COMPOST: $cmd" >> ~/.ghostlink_compost
      ;;
  esac
}

# Quick SCAR marker (no execution)
scar() {
  echo "[$(date +"%Y-%m-%d %H:%M:%S")] MANUAL_SCAR: $*" >> ~/.ghostlink_scars
  echo "✗ Marked as SCAR"
}

# View SCAR map
scars() {
  if [ -f ~/.ghostlink_scars ]; then
    echo "=== SCAR MEMORY ==="
    tail -20 ~/.ghostlink_scars
  else
    echo "No SCARs marked yet"
  fi
}

# View successful routes
sigmas() {
  if [ -f ~/.ghostlink_sigma ]; then
    echo "=== SIGMA ROUTES ==="
    tail -20 ~/.ghostlink_sigma
  else
    echo "No successful routes logged"
  fi
}

# Check if command is in SCAR memory
check_scar() {
  if [ -f ~/.ghostlink_scars ]; then
    if grep -q "$*" ~/.ghostlink_scars; then
      echo "⚠️  WARNING: This command has SCAR history"
      grep "$*" ~/.ghostlink_scars | tail -3
      echo -n "Continue anyway? (y/n): "
      read -r confirm
      [ "$confirm" != "y" ] && return 1
    fi
  fi
  return 0
}

# Initialize logs
[ ! -f ~/.ghostlink_log ] && touch ~/.ghostlink_log
[ ! -f ~/.ghostlink_scars ] && touch ~/.ghostlink_scars
[ ! -f ~/.ghostlink_sigma ] && touch ~/.ghostlink_sigma
[ ! -f ~/.ghostlink_compost ] && touch ~/.ghostlink_compost

echo "GhostLink shell layer loaded"