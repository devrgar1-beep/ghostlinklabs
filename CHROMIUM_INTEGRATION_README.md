# GhostLink Chromium Integration

This module provides headless browser automation capabilities for the GhostLink AI system using Chromium/Puppeteer.

## Features

- **Headless Browser Control**: Start, stop, and control Chromium browser instances
- **Web Navigation**: Navigate to URLs and capture page content
- **Screenshot Capture**: Take screenshots of web pages
- **JavaScript Execution**: Execute custom JavaScript code in browser context
- **Real-time Monitoring**: Monitor browser state and console output
- **Automation Scripts**: Pre-built automation scripts for common tasks

## Architecture

### Backend Service (`chromium_service.py`)
- FastAPI-based REST API
- Puppeteer integration for browser control
- Async/await pattern for non-blocking operations
- CORS enabled for frontend communication

### Frontend Component (`ChromiumBrowser.tsx`)
- React component with modern UI
- Real-time browser state management
- Automation script execution
- Screenshot display and console logging

## API Endpoints

### Browser Control
- `POST /api/chromium/start` - Start headless browser
- `POST /api/chromium/stop` - Stop browser and cleanup
- `GET /api/chromium/status` - Get browser status

### Navigation & Content
- `POST /api/chromium/navigate` - Navigate to URL
- `POST /api/chromium/screenshot` - Take page screenshot
- `POST /api/chromium/execute` - Execute JavaScript

## Usage

### Starting the Services

1. **Backend Service**:
```bash
cd /Users/ghost-link-labs/ghostlinklabs
python3 chromium_service.py
```

2. **Frontend**:
```bash
cd /Users/ghost-link-labs/ghostlinklabs/frontend
npm run dev
```

### Using the Browser Interface

1. Click "Start Browser" to initialize Chromium
2. Enter a URL and click the navigation button
3. Use "Screenshot" to capture the current page
4. Select from pre-built automation scripts or write custom JavaScript
5. Monitor activity in the console panel

## Automation Scripts

### Form Filler
Automatically fills out web forms with predefined data.

### Data Scraper
Extracts structured data from web pages using DOM selectors.

### Screenshot Taker
Captures full-page screenshots for documentation.

## Dependencies

### Backend
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- pydantic==2.5.0
- pyppeteer==1.0.2

### Frontend
- react ^18.2.0
- puppeteer ^22.6.3
- axios ^1.6.7
- lucide-react ^0.344.0
- recharts ^2.12.0

## Security Considerations

- CORS is currently configured to allow all origins (`*`)
- In production, restrict CORS to specific frontend domains
- Browser automation can be resource-intensive
- Implement rate limiting for API endpoints
- Validate JavaScript execution to prevent malicious code

## Troubleshooting

### Browser Won't Start
- Ensure Chromium/Chrome is installed
- Check system resources (RAM, CPU)
- Verify Puppeteer dependencies are installed

### Navigation Fails
- Check URL format and network connectivity
- Verify target website allows automation
- Review browser console for JavaScript errors

### Screenshot Issues
- Ensure page has finished loading
- Check viewport size and page dimensions
- Verify file permissions for screenshot storage

## Development

### Adding New Automation Scripts
1. Define the script in the `automationScripts` state
2. Include proper error handling
3. Test with various websites
4. Document the script's purpose and limitations

### Extending the API
1. Add new endpoints in `chromium_service.py`
2. Update TypeScript interfaces in the frontend
3. Implement UI controls for new features
4. Add proper error handling and logging

## Integration with GhostLink AI

The Chromium integration enables GhostLink to:
- Interact with web applications programmatically
- Extract data from websites for analysis
- Automate repetitive web-based tasks
- Test web applications automatically
- Generate visual documentation

This creates a powerful combination of AI reasoning and web automation capabilities.