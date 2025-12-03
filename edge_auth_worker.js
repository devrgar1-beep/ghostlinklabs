/**
 * GhostLink Edge Authentication Worker
 * Handles authentication and authorization at the edge
 */

addEventListener('fetch', event => {
    event.respondWith(handleAuthRequest(event.request))
})

async function handleAuthRequest(request) {
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
        // Authentication endpoints
        if (url.pathname === '/auth/login' && method === 'POST') {
            return await handleLogin(request, corsHeaders)
        }

        if (url.pathname === '/auth/verify' && method === 'GET') {
            return await handleVerify(request, corsHeaders)
        }

        if (url.pathname === '/auth/refresh' && method === 'POST') {
            return await handleRefresh(request, corsHeaders)
        }

        // Protected routes - check authorization
        if (url.pathname.startsWith('/api/')) {
            return await handleProtectedRoute(request, corsHeaders)
        }

        return new Response(JSON.stringify({
            error: 'Authentication endpoint not found'
        }), {
            status: 404,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

    } catch (error) {
        console.error('Auth Worker Error:', error)
        return new Response(JSON.stringify({
            error: 'Authentication Error',
            message: error.message
        }), {
            status: 500,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })
    }
}

async function handleLogin(request, corsHeaders) {
    try {
        const body = await request.json()
        const { username, password } = body

        // Simulate authentication (replace with real logic)
        if (username && password) {
            // Generate edge JWT token
            const token = await generateEdgeToken({ user: username, role: 'user' })

            return new Response(JSON.stringify({
                success: true,
                token: token,
                message: 'Authenticated at edge',
                edge_location: request.cf?.colo || 'unknown'
            }), {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            })
        }

        return new Response(JSON.stringify({
            error: 'Invalid credentials'
        }), {
            status: 401,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

    } catch (error) {
        return new Response(JSON.stringify({
            error: 'Login failed',
            message: error.message
        }), {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })
    }
}

async function handleVerify(request, corsHeaders) {
    const authHeader = request.headers.get('Authorization')

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return new Response(JSON.stringify({
            valid: false,
            error: 'No token provided'
        }), {
            status: 401,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })
    }

    const token = authHeader.substring(7) // Remove 'Bearer '

    try {
        // Verify token at edge
        const payload = await verifyEdgeToken(token)

        return new Response(JSON.stringify({
            valid: true,
            user: payload.user,
            role: payload.role,
            edge_verified: true,
            location: request.cf?.colo || 'unknown'
        }), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

    } catch (error) {
        return new Response(JSON.stringify({
            valid: false,
            error: 'Token verification failed'
        }), {
            status: 401,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })
    }
}

async function handleRefresh(request, corsHeaders) {
    // Token refresh logic
    return new Response(JSON.stringify({
        message: 'Token refresh not implemented yet'
    }), {
        status: 501,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
}

async function handleProtectedRoute(request, corsHeaders) {
    // Verify token for protected routes
    const authHeader = request.headers.get('Authorization')

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return new Response(JSON.stringify({
            error: 'Authentication required'
        }), {
            status: 401,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })
    }

    // If token is valid, forward to API worker
    // This is a simplified example - in production, you'd verify the token
    return new Response(JSON.stringify({
        message: 'Request authenticated at edge',
        forwarded: true,
        edge_location: request.cf?.colo || 'unknown'
    }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
}

// Simplified JWT-like token generation/verification for edge
// In production, use proper JWT library or Cloudflare's crypto APIs
async function generateEdgeToken(payload) {
    const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }))
    const payloadEncoded = btoa(JSON.stringify({
        ...payload,
        iat: Math.floor(Date.now() / 1000),
        exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60) // 24 hours
    }))

    // Simple signature (not secure - replace with proper crypto)
    const signature = btoa('edge-signature-' + Math.random())

    return `${header}.${payloadEncoded}.${signature}`
}

async function verifyEdgeToken(token) {
    try {
        const parts = token.split('.')
        if (parts.length !== 3) throw new Error('Invalid token format')

        const payload = JSON.parse(atob(parts[1]))

        // Check expiration
        if (payload.exp < Math.floor(Date.now() / 1000)) {
            throw new Error('Token expired')
        }

        return payload
    } catch (error) {
        throw new Error('Token verification failed')
    }
}