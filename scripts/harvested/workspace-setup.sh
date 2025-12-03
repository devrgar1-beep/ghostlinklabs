#!/bin/bash
# GhostLink Workspace Configuration for React Dashboard
# This script sets up the optimal development environment for the Unified Dashboard

# Set up environment variables
GHOSTLINK_DIR="/Users/ghost/GhostLink"
DASHBOARD_DIR="/Users/ghost/Projects/unified-dashboard"
CONFIG_DIR="$DASHBOARD_DIR/configs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$CONFIG_DIR/setup_$TIMESTAMP.log"

# Create necessary directories
mkdir -p "$CONFIG_DIR/vscode"
mkdir -p "$CONFIG_DIR/git"
mkdir -p "$CONFIG_DIR/env"
mkdir -p "$CONFIG_DIR/logs"

# Initialize log file
echo "GhostLink Workspace Setup Started: $(date)" > $LOG_FILE
echo "=====================================" >> $LOG_FILE

# Function to log actions
log() {
  echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1" >> $LOG_FILE
  echo "$1"
}

# Check if project directory exists
if [ ! -d "$DASHBOARD_DIR" ]; then
  log "Creating project directory at $DASHBOARD_DIR"
  mkdir -p "$DASHBOARD_DIR"
fi

# Setup VSCode configuration
setup_vscode() {
  log "Setting up VSCode configuration"
  
  # Create settings.json
  cat > "$CONFIG_DIR/vscode/settings.json" << EOL
{
  "editor.formatOnSave": true,
  "editor.tabSize": 2,
  "editor.rulers": [100],
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "javascript.updateImportsOnFileMove.enabled": "always",
  "typescript.updateImportsOnFileMove.enabled": "always",
  "eslint.validate": [
    "javascript",
    "typescript",
    "javascriptreact",
    "typescriptreact"
  ],
  "files.exclude": {
    "**/.git": true,
    "**/node_modules": true,
    "**/dist": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true
  },
  "tailwindCSS.includeLanguages": {
    "typescript": "javascript",
    "typescriptreact": "javascript"
  },
  "workbench.colorCustomizations": {
    "titleBar.activeBackground": "#0078d7",
    "titleBar.activeForeground": "#ffffff"
  }
}
EOL

  # Create recommended extensions list
  cat > "$CONFIG_DIR/vscode/extensions.json" << EOL
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "formulahendry.auto-rename-tag",
    "streetsidesoftware.code-spell-checker",
    "ms-vscode.vscode-typescript-next",
    "mikestead.dotenv",
    "ms-azuretools.vscode-docker",
    "github.vscode-pull-request-github",
    "eamodio.gitlens"
  ]
}
EOL

  # Copy to project .vscode directory
  mkdir -p "$DASHBOARD_DIR/.vscode"
  cp "$CONFIG_DIR/vscode/settings.json" "$DASHBOARD_DIR/.vscode/"
  cp "$CONFIG_DIR/vscode/extensions.json" "$DASHBOARD_DIR/.vscode/"
  
  log "VSCode configuration completed"
}

# Setup Git configuration
setup_git() {
  log "Setting up Git configuration"
  
  # Create .gitignore
  cat > "$CONFIG_DIR/git/gitignore" << EOL
# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# production
/build
/dist

# misc
.DS_Store
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# editor
.idea/
.vscode/*
!.vscode/settings.json
!.vscode/extensions.json

# artifacts
artifacts/builds/*
artifacts/logs/*
!artifacts/builds/.gitkeep
!artifacts/logs/.gitkeep
EOL

  # Copy to project root
  cp "$CONFIG_DIR/git/gitignore" "$DASHBOARD_DIR/.gitignore"
  
  # Add Git hooks
  mkdir -p "$DASHBOARD_DIR/.git/hooks"
  
  # Create pre-commit hook
  cat > "$CONFIG_DIR/git/pre-commit" << EOL
#!/bin/bash
echo "Running pre-commit hooks..."

# Run ESLint
echo "Running ESLint..."
npx eslint --fix "src/**/*.{js,jsx,ts,tsx}"

# Run TypeScript type check
echo "Running TypeScript type check..."
npx tsc --noEmit

# Run tests
echo "Running tests..."
npm test -- --watchAll=false

# Check for console.log statements
echo "Checking for console.log statements..."
if grep -r "console.log" --include="*.{js,jsx,ts,tsx}" src/; then
  echo "WARNING: console.log statements found"
fi

echo "Pre-commit hooks completed successfully"
EOL

  chmod +x "$CONFIG_DIR/git/pre-commit"
  cp "$CONFIG_DIR/git/pre-commit" "$DASHBOARD_DIR/.git/hooks/"
  
  log "Git configuration completed"
}

# Setup Environment Variables
setup_env() {
  log "Setting up environment variables"
  
  # Create .env templates for different environments
  cat > "$CONFIG_DIR/env/.env.template" << EOL
# This is a template .env file
# Copy this file to .env and update the values

# API Keys
VITE_GOOGLE_CLIENT_ID=your_google_client_id
VITE_VERCEL_TOKEN=your_vercel_token
VITE_CLOUDFLARE_TOKEN=your_cloudflare_token

# Environment Settings
VITE_APP_ENV=development
VITE_API_BASE_URL=http://localhost:3000
EOL

  cat > "$CONFIG_DIR/env/.env.development" << EOL
# Development environment variables
VITE_APP_ENV=development
VITE_API_BASE_URL=http://localhost:3000
EOL

  cat > "$CONFIG_DIR/env/.env.production" << EOL
# Production environment variables
VITE_APP_ENV=production
VITE_API_BASE_URL=https://api.yourdomain.com
EOL

  cat > "$CONFIG_DIR/env/.env.test" << EOL
# Test environment variables
VITE_APP_ENV=test
VITE_API_BASE_URL=http://localhost:3000
EOL

  # Copy template to project root
  cp "$CONFIG_DIR/env/.env.template" "$DASHBOARD_DIR/.env.template"
  cp "$CONFIG_DIR/env/.env.development" "$DASHBOARD_DIR/.env.development"
  cp "$CONFIG_DIR/env/.env.production" "$DASHBOARD_DIR/.env.production"
  cp "$CONFIG_DIR/env/.env.test" "$DASHBOARD_DIR/.env.test"
  
  log "Environment configuration completed"
}

# Create package.json if it doesn't exist
setup_project() {
  if [ ! -f "$DASHBOARD_DIR/package.json" ]; then
    log "Creating package.json and project structure"
    
    # Initialize package.json
    cat > "$DASHBOARD_DIR/package.json" << EOL
{
  "name": "unified-dashboard",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint src --ext .js,.jsx,.ts,.tsx --fix",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "prepare": "husky install"
  },
  "dependencies": {
    "@tanstack/react-query": "^5.0.0",
    "axios": "^1.5.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.15.0",
    "zustand": "^4.4.1"
  },
  "devDependencies": {
    "@types/node": "^20.5.9",
    "@types/react": "^18.2.21",
    "@types/react-dom": "^18.2.7",
    "@typescript-eslint/eslint-plugin": "^6.6.0",
    "@typescript-eslint/parser": "^6.6.0",
    "@vitejs/plugin-react": "^4.0.4",
    "autoprefixer": "^10.4.15",
    "eslint": "^8.49.0",
    "eslint-config-prettier": "^9.0.0",
    "eslint-plugin-import": "^2.28.1",
    "eslint-plugin-jsx-a11y": "^6.7.1",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "husky": "^8.0.0",
    "postcss": "^8.4.29",
    "prettier": "^3.0.3",
    "tailwindcss": "^3.3.3",
    "typescript": "^5.2.2",
    "vite": "^4.4.9",
    "vite-tsconfig-paths": "^4.2.0",
    "vitest": "^0.34.4"
  }
}
EOL

    # Create tsconfig.json
    cat > "$DASHBOARD_DIR/tsconfig.json" << EOL
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
EOL

    # Create vite.config.ts
    cat > "$DASHBOARD_DIR/vite.config.ts" << EOL
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          ui: ['@/components/ui'],
          query: ['@tanstack/react-query'],
        },
      },
    },
  },
});
EOL

    # Create basic project structure
    mkdir -p "$DASHBOARD_DIR/src/features/google-drive/components"
    mkdir -p "$DASHBOARD_DIR/src/features/google-drive/hooks"
    mkdir -p "$DASHBOARD_DIR/src/features/google-drive/services"
    mkdir -p "$DASHBOARD_DIR/src/features/gmail"
    mkdir -p "$DASHBOARD_DIR/src/features/calendar"
    mkdir -p "$DASHBOARD_DIR/src/features/vercel"
    mkdir -p "$DASHBOARD_DIR/src/features/cloudflare"
    mkdir -p "$DASHBOARD_DIR/src/features/dashboard"
    mkdir -p "$DASHBOARD_DIR/src/shared/components/ui"
    mkdir -p "$DASHBOARD_DIR/src/shared/components/layout"
    mkdir -p "$DASHBOARD_DIR/src/shared/hooks"
    mkdir -p "$DASHBOARD_DIR/src/shared/lib"
    mkdir -p "$DASHBOARD_DIR/src/shared/stores"
    mkdir -p "$DASHBOARD_DIR/src/services"
    mkdir -p "$DASHBOARD_DIR/public"
    
    log "Basic project structure created"
  else
    log "Project already initialized, skipping setup_project step"
  fi
}

# Integrate with GhostLink
ghostlink_integration() {
  log "Integrating with GhostLink"
  
  # Create GhostLink integration script
  cat > "$CONFIG_DIR/ghostlink-integration.sh" << EOL
#!/bin/bash
# GhostLink Integration for Unified Dashboard

# Set up environment variables
GHOSTLINK_DIR="/Users/ghost/GhostLink"
DASHBOARD_DIR="/Users/ghost/Projects/unified-dashboard"

# Execute GhostLink commands based on parameters
case "\$1" in
  "sync")
    # Sync services
    bash "\$GHOSTLINK_DIR/ghostlink_services.sh" google drive open
    bash "\$GHOSTLINK_DIR/ghostlink_services.sh" google gmail open
    bash "\$GHOSTLINK_DIR/ghostlink_services.sh" google calendar open
    echo "Google services synced"
    ;;
  "backup")
    # Create backup
    bash "\$GHOSTLINK_DIR/ghostlink_platform.sh" backup "\$DASHBOARD_DIR" 
    echo "Project backed up using GhostLink"
    ;;
  "ai")
    # Use AI assistance
    bash "\$GHOSTLINK_DIR/ghostlink_control.sh" claude
    echo "Claude AI assistant launched"
    ;;
  "monitor")
    # System monitoring
    bash "\$GHOSTLINK_DIR/ghostlink_control.sh" monitor
    echo "System monitoring initiated"
    ;;
  "help")
    echo "GhostLink Integration Commands:"
    echo "  sync    - Sync Google services"
    echo "  backup  - Create project backup"
    echo "  ai      - Launch Claude AI assistant"
    echo "  monitor - Start system monitoring"
    ;;
  *)
    echo "Unknown command: \$1"
    echo "Run 'ghostlink-integration.sh help' for available commands"
    ;;
esac
EOL

  chmod +x "$CONFIG_DIR/ghostlink-integration.sh"
  
  # Create symbolic link to GhostLink master script
  ln -sf "$GHOSTLINK_DIR/ghostlink_master.sh" "$DASHBOARD_DIR/ghostlink"
  
  log "GhostLink integration completed"
}

# Setup automation script
setup_automation() {
  log "Setting up automation script"
  
  # Create automation script
  cat > "$DASHBOARD_DIR/ghostlink-automate.sh" << EOL
#!/bin/bash

# Call GhostLink automation script
bash $DASHBOARD_DIR/artifacts/ghostlink-automation.sh "\$@"
EOL

  chmod +x "$DASHBOARD_DIR/ghostlink-automate.sh"
  
  log "Automation script setup completed"
}

# Main execution
case "$1" in
  "vscode")
    setup_vscode
    ;;
  "git")
    setup_git
    ;;
  "env")
    setup_env
    ;;
  "project")
    setup_project
    ;;
  "ghostlink")
    ghostlink_integration
    ;;
  "automation")
    setup_automation
    ;;
  "all")
    setup_vscode
    setup_git
    setup_env
    setup_project
    ghostlink_integration
    setup_automation
    ;;
  *)
    echo "Usage: $0 [vscode|git|env|project|ghostlink|automation|all]"
    echo "Examples:"
    echo "  $0 vscode    - Set up VSCode configuration"
    echo "  $0 git       - Set up Git configuration"
    echo "  $0 env       - Set up environment variables"
    echo "  $0 project   - Initialize project structure"
    echo "  $0 ghostlink - Integrate with GhostLink"
    echo "  $0 automation - Set up automation script"
    echo "  $0 all       - Set up everything"
    ;;
esac

log "GhostLink Workspace Setup Completed: $(date)"
echo "=====================================" >> $LOG_FILE
