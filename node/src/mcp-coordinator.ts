/**
 * GhostLink v8 MCP Server Coordinator
 * 
 * Manages multiple Model Context Protocol server instances across different
 * connector types (filesystem, HTTP, database, GitHub, etc.) and coordinates
 * with the Python orchestrator for distributed AI coordination.
 * 
 * Architecture:
 * - Multiple MCP server instances for different tool categories
 * - Connection pooling for database and HTTP connectors
 * - Health check aggregation across all connectors
 * - Stigmergic coordination with orchestrator via Redis
 * 
 * @author Robert Christopher George (Ghost)
 * @version 8.0.0
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool
} from '@modelcontextprotocol/sdk/types.js';
import express, { Express, Request, Response } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import { createClient } from 'redis';
import { Pool } from 'pg';
import pino from 'pino';
import { z } from 'zod';
import { v4 as uuidv4 } from 'uuid';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

// ══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ══════════════════════════════════════════════════════════════════════════════

const CONFIG = {
  NODE_ENV: process.env.NODE_ENV || 'development',
  MCP_PORT: parseInt(process.env.MCP_PORT || '3000'),
  ORCHESTRATOR_URL: process.env.ORCHESTRATOR_URL || 'http://localhost:8000',
  DATABASE_URL: process.env.DATABASE_URL || 'postgresql://ghostlink:ghostlink@localhost:5432/ghostlink',
  REDIS_URL: process.env.REDIS_URL || 'redis://localhost:6379/0',
  LOG_LEVEL: process.env.LOG_LEVEL || 'info',
  ENABLE_METRICS: process.env.ENABLE_METRICS === 'true',
  HEALTH_CHECK_INTERVAL: 10000, // 10 seconds
};
  // optional admin key to protect mutating API endpoints
  CONFIG['ADMIN_API_KEY'] = process.env.ADMIN_API_KEY || process.env.GHOSTLINK_ADMIN_API_KEY || '';

// ══════════════════════════════════════════════════════════════════════════════
// LOGGING SETUP
// ══════════════════════════════════════════════════════════════════════════════

const logger = pino({
  level: CONFIG.LOG_LEVEL,
  transport: {
    target: 'pino-pretty',
    options: {
      colorize: true,
      translateTime: 'SYS:standard',
      ignore: 'pid,hostname'
    }
  }
});

// ══════════════════════════════════════════════════════════════════════════════
// MCP TOOL DEFINITIONS
// ══════════════════════════════════════════════════════════════════════════════

interface GhostLinkTool extends Tool {
  category: 'filesystem' | 'http' | 'database' | 'github' | 'coordination';
  handler: (args: any) => Promise<any>;
}

const GHOSTLINK_TOOLS: GhostLinkTool[] = [
  // ──── Filesystem Tools ──────────────────────────────────────────────────
  {
    name: 'read_file',
    description: 'Read contents of a file from the filesystem',
    category: 'filesystem',
    inputSchema: {
      type: 'object',
      properties: {
        path: {
          type: 'string',
          description: 'File path to read'
        }
      },
      required: ['path']
    },
    handler: async (args) => {
      const fs = await import('fs/promises');
      const content = await fs.readFile(args.path, 'utf-8');
      return { success: true, content };
    }
  },
  
  {
    name: 'write_file',
    description: 'Write content to a file',
    category: 'filesystem',
    inputSchema: {
      type: 'object',
      properties: {
        path: {
          type: 'string',
          description: 'File path to write'
        },
        content: {
          type: 'string',
          description: 'Content to write'
        }
      },
      required: ['path', 'content']
    },
    handler: async (args) => {
      const fs = await import('fs/promises');
      await fs.writeFile(args.path, args.content, 'utf-8');
      return { success: true, path: args.path };
    }
  },
  
  {
    name: 'list_directory',
    description: 'List contents of a directory',
    category: 'filesystem',
    inputSchema: {
      type: 'object',
      properties: {
        path: {
          type: 'string',
          description: 'Directory path to list'
        }
      },
      required: ['path']
    },
    handler: async (args) => {
      const fs = await import('fs/promises');
      const files = await fs.readdir(args.path, { withFileTypes: true });
      return {
        success: true,
        entries: files.map(f => ({
          name: f.name,
          type: f.isDirectory() ? 'directory' : 'file'
        }))
      };
    }
  },
  
  // ──── HTTP Tools ────────────────────────────────────────────────────────
  {
    name: 'http_request',
    description: 'Make an HTTP request',
    category: 'http',
    inputSchema: {
      type: 'object',
      properties: {
        url: {
          type: 'string',
          description: 'URL to request'
        },
        method: {
          type: 'string',
          enum: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
          description: 'HTTP method'
        },
        headers: {
          type: 'object',
          description: 'Request headers'
        },
        body: {
          type: 'string',
          description: 'Request body'
        }
      },
      required: ['url', 'method']
    },
    handler: async (args) => {
      const axios = (await import('axios')).default;
      const response = await axios({
        url: args.url,
        method: args.method,
        headers: args.headers,
        data: args.body
      });
      return {
        success: true,
        status: response.status,
        headers: response.headers,
        data: response.data
      };
    }
  },
  
  // ──── Database Tools ────────────────────────────────────────────────────
  {
    name: 'query_database',
    description: 'Execute a SQL query against the GhostLink database',
    category: 'database',
    inputSchema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'SQL query to execute'
        },
        params: {
          type: 'array',
          description: 'Query parameters',
          items: { type: 'string' }
        }
      },
      required: ['query']
    },
    handler: async (args) => {
      // Database handler implementation in coordinator
      return { success: true, placeholder: true };
    }
  },
  
  // ──── Coordination Tools ────────────────────────────────────────────────
  {
    name: 'deposit_pheromone',
    description: 'Deposit a stigmergic pheromone trail for agent coordination',
    category: 'coordination',
    inputSchema: {
      type: 'object',
      properties: {
        agent_id: {
          type: 'string',
          description: 'Agent ID depositing the pheromone'
        },
        trail_type: {
          type: 'string',
          description: 'Type of pheromone trail'
        },
        concentration: {
          type: 'number',
          description: 'Pheromone concentration (0-1)'
        },
        position: {
          type: 'array',
          description: 'Lattice position [x, y, z, w]',
          items: { type: 'integer' }
        }
      },
      required: ['agent_id', 'trail_type', 'concentration', 'position']
    },
    handler: async (args) => {
      // Redis pheromone handler implementation in coordinator
      return { success: true, placeholder: true };
    }
  },
  
  {
    name: 'sense_pheromones',
    description: 'Sense stigmergic pheromone trails at a lattice position',
    category: 'coordination',
    inputSchema: {
      type: 'object',
      properties: {
        position: {
          type: 'array',
          description: 'Lattice position [x, y, z, w]',
          items: { type: 'integer' }
        }
      },
      required: ['position']
    },
    handler: async (args) => {
      // Redis pheromone sensing implementation in coordinator
      return { success: true, placeholder: true };
    }
  }
];

// ══════════════════════════════════════════════════════════════════════════════
// MCP SERVER COORDINATOR
// ══════════════════════════════════════════════════════════════════════════════

class MCPServerCoordinator {
  private servers: Map<string, Server> = new Map();
  private pgPool: Pool;
  private redisClient: any;
  private app: Express;
  private startTime: Date;
  
  constructor() {
    this.app = express();
    this.startTime = new Date();
    
    // Initialize database pool
    this.pgPool = new Pool({ connectionString: CONFIG.DATABASE_URL });
    
    // Setup middleware
    this.setupMiddleware();
    this.setupRoutes();
  }
  
  private setupMiddleware(): void {
    this.app.use(helmet());
    this.app.use(cors());
    this.app.use(compression());
    this.app.use(express.json());
    
    // Request logging
    this.app.use((req, res, next) => {
      logger.info({
        method: req.method,
        path: req.path,
        ip: req.ip
      }, 'Incoming request');
      next();
    });
  }
  
  private setupRoutes(): void {
    // Health check endpoint
    this.app.get('/health', async (req: Request, res: Response) => {
      const health = await this.getHealthStatus();
      res.json(health);
    });
    
    // Server status endpoint
    this.app.get('/status', (req: Request, res: Response) => {
      const uptime = Math.floor((Date.now() - this.startTime.getTime()) / 1000);
      res.json({
        status: 'operational',
        version: '8.0.0',
        servers: Array.from(this.servers.keys()),
        uptime_seconds: uptime
      });
    });
    
    // Tools listing endpoint
    this.app.get('/tools', (req: Request, res: Response) => {
      const toolsByCategory: Record<string, any[]> = {};
      
      GHOSTLINK_TOOLS.forEach(tool => {
        if (!toolsByCategory[tool.category]) {
          toolsByCategory[tool.category] = [];
        }
        toolsByCategory[tool.category].push({
          name: tool.name,
          description: tool.description,
          inputSchema: tool.inputSchema
        });
      });
      
      res.json({
        total_tools: GHOSTLINK_TOOLS.length,
        by_category: toolsByCategory
      });
    });
    
    // Tool execution endpoint
    this.app.post('/execute/:toolName', async (req: Request, res: Response) => {
      const { toolName } = req.params;
      const args = req.body;
      
      const tool = GHOSTLINK_TOOLS.find(t => t.name === toolName);
      
      if (!tool) {
        return res.status(404).json({ error: 'Tool not found' });
      }
      
      try {
        const result = await this.executeToolWithContext(tool, args);
        res.json({ success: true, result });
      } catch (error: any) {
        logger.error({ error: error.message, tool: toolName }, 'Tool execution failed');
        res.status(500).json({ error: error.message });
      }
    });
    
    // Orchestrator coordination endpoint
    this.app.get('/coordination/status', async (req: Request, res: Response) => {
      try {
        const status = await this.getCoordinationStatus();
        res.json(status);
      } catch (error: any) {
        logger.error({ error: error.message }, 'Failed to get coordination status');
        res.status(500).json({ error: error.message });
      }
    });

    // UI settings - allow runtime toggling of front-end UI transparency
    this.app.get('/api/ui/settings', async (req: Request, res: Response) => {
      try {
        // Prefer Redis-stored value so it's dynamic across processes
        let uiTransparent = false;
        let uiAlpha = parseFloat(process.env.GHOSTLINK_UI_ALPHA || '0.2');

        if (this.redisClient) {
          const v = await this.redisClient.get('ui:transparent');
          if (v !== null) {
            uiTransparent = v === '1' || v === 'true';
          }
          const a = await this.redisClient.get('ui:alpha');
          if (a !== null) {
            uiAlpha = parseFloat(a);
          }
        } else {
          // fallback to env var
          uiTransparent = (process.env.GHOSTLINK_UI_TRANSPARENT === '1' || process.env.GHOSTLINK_UI_TRANSPARENT === 'true');
        }

        res.json({ uiTransparent, uiAlpha });
      } catch (error: any) {
        logger.error({ error: error.message }, 'Failed to read UI settings');
        res.status(500).json({ error: 'failed to read ui settings' });
      }
    });

    this.app.post('/api/ui/settings', async (req: Request, res: Response) => {
      try {
        // optional admin protection
        const provided = req.headers['x-admin-key'] || req.headers['authorization'];
        if (CONFIG.ADMIN_API_KEY && provided !== CONFIG.ADMIN_API_KEY) {
          return res.status(403).json({ error: 'forbidden' });
        }

        const { uiTransparent, uiAlpha } = req.body;

        if (typeof uiTransparent !== 'undefined') {
          if (this.redisClient) await this.redisClient.set('ui:transparent', uiTransparent ? '1' : '0');
          else process.env.GHOSTLINK_UI_TRANSPARENT = uiTransparent ? '1' : '0';
        }

        if (typeof uiAlpha !== 'undefined') {
          const val = String(parseFloat(uiAlpha));
          if (this.redisClient) await this.redisClient.set('ui:alpha', val);
          else process.env.GHOSTLINK_UI_ALPHA = val;
        }

        res.json({ success: true });
      } catch (error: any) {
        logger.error({ error: error.message }, 'Failed to write UI settings');
        res.status(500).json({ error: 'failed to write ui settings' });
      }
    });
  }
  
  async initialize(): Promise<void> {
    logger.info('Initializing MCP Server Coordinator...');
    
    // Connect to Redis
    this.redisClient = createClient({ url: CONFIG.REDIS_URL });
    await this.redisClient.connect();
    logger.info('Redis connection established');
    
    // Test database connection
    await this.pgPool.query('SELECT 1');
    logger.info('Database connection established');
    
    // Initialize MCP servers by category
    for (const category of ['filesystem', 'http', 'database', 'github', 'coordination']) {
      await this.initializeMCPServer(category);
    }
    
    logger.info({
      servers: Array.from(this.servers.keys()),
      tools: GHOSTLINK_TOOLS.length
    }, 'MCP Server Coordinator initialized');
  }
  
  private async initializeMCPServer(category: string): Promise<void> {
    const server = new Server(
      {
        name: `ghostlink-mcp-${category}`,
        version: '8.0.0'
      },
      {
        capabilities: {
          tools: {}
        }
      }
    );
    
    // Register tools for this category
    const categoryTools = GHOSTLINK_TOOLS.filter(t => t.category === category);
    
    server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: categoryTools.map(t => ({
        name: t.name,
        description: t.description,
        inputSchema: t.inputSchema
      }))
    }));
    
    server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const tool = categoryTools.find(t => t.name === request.params.name);
      
      if (!tool) {
        throw new Error(`Tool not found: ${request.params.name}`);
      }
      
      const result = await this.executeToolWithContext(tool, request.params.arguments);
      
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(result, null, 2)
        }]
      };
    });
    
    this.servers.set(category, server);
    logger.info({ category, tools: categoryTools.length }, 'MCP server initialized');
  }
  
  private async executeToolWithContext(tool: GhostLinkTool, args: any): Promise<any> {
    const executionId = uuidv4();
    const startTime = Date.now();
    
    logger.info({
      executionId,
      tool: tool.name,
      category: tool.category
    }, 'Executing tool');
    
    try {
      // Special handling for database tools
      if (tool.category === 'database' && tool.name === 'query_database') {
        const result = await this.pgPool.query(args.query, args.params || []);
        return { success: true, rows: result.rows, rowCount: result.rowCount };
      }
      
      // Special handling for coordination tools
      if (tool.category === 'coordination') {
        if (tool.name === 'deposit_pheromone') {
          return await this.depositPheromone(args);
        } else if (tool.name === 'sense_pheromones') {
          return await this.sensePheromones(args);
        }
      }
      
      // Execute tool handler
      const result = await tool.handler(args);
      
      const duration = Date.now() - startTime;
      logger.info({
        executionId,
        tool: tool.name,
        duration
      }, 'Tool execution completed');
      
      return result;
    } catch (error: any) {
      const duration = Date.now() - startTime;
      logger.error({
        executionId,
        tool: tool.name,
        duration,
        error: error.message
      }, 'Tool execution failed');
      throw error;
    }
  }
  
  private async depositPheromone(args: any): Promise<any> {
    const key = `pheromone:${JSON.stringify(args.position)}`;
    const value = JSON.stringify({
      agent_id: args.agent_id,
      trail_type: args.trail_type,
      concentration: args.concentration,
      timestamp: Date.now()
    });
    
    // Calculate TTL based on evaporation (10 seconds default)
    const ttl = 10;
    
    await this.redisClient.setEx(key, ttl, value);
    
    logger.debug({
      position: args.position,
      agent_id: args.agent_id,
      trail_type: args.trail_type
    }, 'Pheromone deposited');
    
    return { success: true, position: args.position };
  }
  
  private async sensePheromones(args: any): Promise<any> {
    const key = `pheromone:${JSON.stringify(args.position)}`;
    const value = await this.redisClient.get(key);
    
    if (!value) {
      return { success: true, pheromones: [] };
    }
    
    const pheromone = JSON.parse(value);
    
    return {
      success: true,
      pheromones: [pheromone]
    };
  }
  
  private async getHealthStatus(): Promise<any> {
    const checks: Record<string, any> = {
      servers: {},
      database: 'unknown',
      redis: 'unknown',
      orchestrator: 'unknown'
    };
    
    // Check MCP servers
    for (const [category, server] of this.servers) {
      checks.servers[category] = 'healthy';
    }
    
    // Check database
    try {
      await this.pgPool.query('SELECT 1');
      checks.database = 'healthy';
    } catch (error) {
      checks.database = 'unhealthy';
    }
    
    // Check Redis
    try {
      await this.redisClient.ping();
      checks.redis = 'healthy';
    } catch (error) {
      checks.redis = 'unhealthy';
    }
    
    // Check orchestrator
    try {
      const axios = (await import('axios')).default;
      const response = await axios.get(`${CONFIG.ORCHESTRATOR_URL}/health`, {
        timeout: 5000
      });
      checks.orchestrator = response.data.status === 'healthy' ? 'healthy' : 'unhealthy';
    } catch (error) {
      checks.orchestrator = 'unhealthy';
    }
    
    const allHealthy = Object.values(checks).every(v => 
      typeof v === 'object' ? Object.values(v).every(x => x === 'healthy') : v === 'healthy'
    );
    
    return {
      status: allHealthy ? 'healthy' : 'degraded',
      checks,
      timestamp: new Date().toISOString()
    };
  }
  
  private async getCoordinationStatus(): Promise<any> {
    // Get pheromone trail count
    const keys = await this.redisClient.keys('pheromone:*');
    
    // Get orchestrator status
    const axios = (await import('axios')).default;
    const orchResponse = await axios.get(`${CONFIG.ORCHESTRATOR_URL}/agents/status`);
    
    return {
      mcp_servers: Array.from(this.servers.keys()),
      active_pheromone_trails: keys.length,
      orchestrator_status: orchResponse.data
    };
  }
  
  async start(): Promise<void> {
    await this.initialize();
    
    this.app.listen(CONFIG.MCP_PORT, () => {
      logger.info({
        port: CONFIG.MCP_PORT,
        env: CONFIG.NODE_ENV
      }, 'MCP Server Coordinator listening');
    });
  }
  
  async shutdown(): Promise<void> {
    logger.info('Shutting down MCP Server Coordinator...');
    
    // Close Redis connection
    if (this.redisClient) {
      await this.redisClient.quit();
    }
    
    // Close database pool
    await this.pgPool.end();
    
    logger.info('MCP Server Coordinator shutdown complete');
  }
}

// ══════════════════════════════════════════════════════════════════════════════
// MAIN ENTRY POINT
// ══════════════════════════════════════════════════════════════════════════════

async function main() {
  const coordinator = new MCPServerCoordinator();
  
  // Handle graceful shutdown
  process.on('SIGINT', async () => {
    logger.info('Received SIGINT, shutting down gracefully...');
    await coordinator.shutdown();
    process.exit(0);
  });
  
  process.on('SIGTERM', async () => {
    logger.info('Received SIGTERM, shutting down gracefully...');
    await coordinator.shutdown();
    process.exit(0);
  });
  
  try {
    await coordinator.start();
  } catch (error: any) {
    logger.error({ error: error.message }, 'Failed to start MCP Server Coordinator');
    process.exit(1);
  }
}

main();
