/**
 * GhostLink Edge API Worker
 * Handles API requests at Cloudflare's edge network
 */

addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
    const url = new URL(request.url)
    const method = request.method

    // CORS headers
    const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    }

    // Handle preflight requests
    if (method === 'OPTIONS') {
        return new Response(null, { headers: corsHeaders })
    }

    try {
        // Route requests
        if (url.pathname.startsWith('/api/ghostlink/')) {
            return await handleGhostLinkAPI(request, corsHeaders)
        }

        if (url.pathname === '/health') {
            return new Response(JSON.stringify({
                status: 'healthy',
                service: 'ghostlink-edge-api',
                timestamp: new Date().toISOString(),
                region: request.cf?.colo || 'unknown'
            }), {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            })
        }

        // Default response
        return new Response(JSON.stringify({
            message: 'GhostLink Edge API',
            version: '1.0.0',
            endpoints: ['/health', '/api/ghostlink/*']
        }), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

    } catch (error) {
        console.error('Edge API Error:', error)
        return new Response(JSON.stringify({
            error: 'Internal Server Error',
            message: error.message
        }), {
            status: 500,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })
    }
}

async function handleGhostLinkAPI(request, corsHeaders) {
    const url = new URL(request.url)
    const method = request.method

    // Extract API path
    const apiPath = url.pathname.replace('/api/ghostlink/', '')

    // Simulate different API endpoints
    switch (apiPath) {
        case 'status':
            return new Response(JSON.stringify({
                status: 'operational',
                edge_location: request.cf?.colo || 'unknown',
                timestamp: new Date().toISOString()
            }), {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            })

        case 'ai/models':
            return new Response(JSON.stringify({
                models: ['gpt-4', 'claude-3', 'ghostlink-v2'],
                edge_processed: true
            }), {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            })

        default:
            return new Response(JSON.stringify({
                error: 'Endpoint not found',
                available_endpoints: ['status', 'ai/models']
            }), {
                status: 404,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            })
    }
}