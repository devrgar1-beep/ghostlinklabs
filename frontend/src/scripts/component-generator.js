#!/usr/bin/env node
/**
 * GhostLink React Component Generator
 * 
 * A sophisticated tool to generate React components following best practices
 * for the Unified Dashboard project. This script creates all necessary files
 * for a new component with proper TypeScript typing and styling.
 * 
 * Usage:
 * node component-generator.js create-component [options]
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const CONFIG = {
  basePath: process.env.DASHBOARD_DIR || '/Users/ghost/Projects/unified-dashboard',
  featuresPath: 'src/features',
  sharedComponentsPath: 'src/shared/components',
  types: ['component', 'page', 'layout', 'form', 'card', 'modal', 'table', 'chart']
};

// Templates for different files
const TEMPLATES = {
  component: (name, type) => `import React from 'react';
import { ${name}Props } from './types';
import styles from './${name}.module.css';

export const ${name}: React.FC<${name}Props> = ({
  // Props destructuring
}) => {
  return (
    <div className={styles.container}>
      <h2>${name}</h2>
      {/* Component content */}
    </div>
  );
};
`,

  page: (name) => `import React from 'react';
import { ${name}Props } from './types';
import styles from './${name}.module.css';

export const ${name}: React.FC<${name}Props> = ({
  // Props destructuring
}) => {
  return (
    <div className={styles.pageContainer}>
      <h1>${name.replace(/Page$/, '')}</h1>
      <div className={styles.content}>
        {/* Page content */}
      </div>
    </div>
  );
};
`,

  types: (name, type) => `export interface ${name}Props {
  // Define props here
  className?: string;
  children?: React.ReactNode;
}
`,

  css: (name, type) => {
    if (type === 'page') {
      return `.pageContainer {
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  gap: 1.5rem;
}

.content {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}`;
    }
    
    return `.container {
  /* Component styles */
}`;
  },

  index: (name) => `export * from './${name}';
`,

  test: (name) => `import React from 'react';
import { render, screen } from '@testing-library/react';
import { ${name} } from './${name}';

describe('${name}', () => {
  it('renders without crashing', () => {
    render(<${name} />);
    expect(screen.getByText('${name}')).toBeInTheDocument();
  });

  // Add more tests here
});
`
};

/**
 * Creates a new component with all necessary files
 * @param {Object} options - Component options
 */
function createComponent(options) {
  const { name, type = 'component', feature, shared = false } = options;
  
  // Validate component name
  if (!name) {
    console.error('Error: Component name is required');
    process.exit(1);
  }
  
  // Validate component type
  if (!CONFIG.types.includes(type)) {
    console.error(`Error: Invalid component type. Must be one of: ${CONFIG.types.join(', ')}`);
    process.exit(1);
  }
  
  // Determine component path
  let componentPath;
  if (shared) {
    componentPath = path.join(CONFIG.basePath, CONFIG.sharedComponentsPath, type, name);
  } else {
    if (!feature) {
      console.error('Error: Feature name is required for non-shared components');
      process.exit(1);
    }
    componentPath = path.join(CONFIG.basePath, CONFIG.featuresPath, feature, 'components', name);
  }
  
  // Create component directory
  if (fs.existsSync(componentPath)) {
    console.error(`Error: Component directory already exists: ${componentPath}`);
    process.exit(1);
  }
  
  fs.mkdirSync(componentPath, { recursive: true });
  console.log(`Created component directory: ${componentPath}`);
  
  // Create component files
  const files = [
    { name: `${name}.tsx`, template: type === 'page' ? TEMPLATES.page(name) : TEMPLATES.component(name, type) },
    { name: 'types.ts', template: TEMPLATES.types(name, type) },
    { name: `${name}.module.css`, template: TEMPLATES.css(name, type) },
    { name: 'index.ts', template: TEMPLATES.index(name) },
    { name: `${name}.test.tsx`, template: TEMPLATES.test(name) }
  ];
  
  files.forEach(file => {
    const filePath = path.join(componentPath, file.name);
    fs.writeFileSync(filePath, file.template);
    console.log(`Created file: ${filePath}`);
  });
  
  // If this is a feature component, update the feature index.ts file
  if (!shared && feature) {
    const featurePath = path.join(CONFIG.basePath, CONFIG.featuresPath, feature);
    const indexPath = path.join(featurePath, 'index.ts');
    
    // Create feature index if it doesn't exist
    if (!fs.existsSync(indexPath)) {
      fs.writeFileSync(indexPath, `// Feature exports for ${feature}\n`);
      console.log(`Created feature index: ${indexPath}`);
    }
    
    // Add component export to feature index
    const exportLine = `export * from './components/${name}';\n`;
    let indexContent = fs.readFileSync(indexPath, 'utf8');
    
    if (!indexContent.includes(exportLine)) {
      fs.appendFileSync(indexPath, exportLine);
      console.log(`Updated feature index with ${name} export`);
    }
  }
  
  // Log GhostLink integration
  try {
    const ghostlinkDir = process.env.GHOSTLINK_DIR || '/Users/ghost/GhostLink';
    const logCommand = `bash "${ghostlinkDir}/ghostlink_control.sh" speak "Component ${name} created successfully"`;
    execSync(logCommand);
  } catch (error) {
    // Silently fail if GhostLink integration is not available
  }
  
  console.log(`\n✅ Component ${name} created successfully!`);
  console.log(`Type: ${type}`);
  console.log(`Location: ${shared ? 'shared' : feature}`);
  console.log(`Path: ${componentPath}`);
}

/**
 * Creates a new hook
 * @param {Object} options - Hook options
 */
function createHook(options) {
  const { name, feature, shared = false } = options;
  
  // Validate hook name
  if (!name) {
    console.error('Error: Hook name is required');
    process.exit(1);
  }
  
  // Ensure hook name starts with 'use'
  const hookName = name.startsWith('use') ? name : `use${name}`;
  
  // Determine hook path
  let hookPath;
  if (shared) {
    hookPath = path.join(CONFIG.basePath, 'src/shared/hooks');
  } else {
    if (!feature) {
      console.error('Error: Feature name is required for non-shared hooks');
      process.exit(1);
    }
    hookPath = path.join(CONFIG.basePath, CONFIG.featuresPath, feature, 'hooks');
  }
  
  // Create hook directory if it doesn't exist
  fs.mkdirSync(hookPath, { recursive: true });
  
  // Create hook file
  const hookFilePath = path.join(hookPath, `${hookName}.ts`);
  
  // Check if hook already exists
  if (fs.existsSync(hookFilePath)) {
    console.error(`Error: Hook file already exists: ${hookFilePath}`);
    process.exit(1);
  }
  
  // Hook template
  const hookTemplate = `import { useState, useEffect } from 'react';

/**
 * ${hookName} - Custom hook for handling ${hookName.replace(/^use/, '')} functionality
 * 
 * @returns Hook values and functions
 */
export const ${hookName} = () => {
  // State
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [data, setData] = useState<any>(null);
  
  // Effects
  useEffect(() => {
    // Hook logic
  }, []);
  
  // Actions
  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Fetch data logic
      const result = await Promise.resolve({});
      setData(result);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  };
  
  return {
    loading,
    error,
    data,
    fetchData
  };
};
`;
  
  fs.writeFileSync(hookFilePath, hookTemplate);
  console.log(`Created hook: ${hookFilePath}`);
  
  // Create test file
  const testFilePath = path.join(hookPath, `${hookName}.test.ts`);
  const testTemplate = `import { renderHook, act } from '@testing-library/react-hooks';
import { ${hookName} } from './${hookName}';

describe('${hookName}', () => {
  it('should initialize with default values', () => {
    const { result } = renderHook(() => ${hookName}());
    
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
    expect(result.current.data).toBeNull();
  });
  
  // Add more tests here
});
`;
  
  fs.writeFileSync(testFilePath, testTemplate);
  console.log(`Created test: ${testFilePath}`);
  
  // If this is a feature hook, update the index.ts file
  if (!shared && feature) {
    const indexPath = path.join(hookPath, 'index.ts');
    
    // Create hooks index if it doesn't exist
    if (!fs.existsSync(indexPath)) {
      fs.writeFileSync(indexPath, `// Hook exports for ${feature}\n`);
      console.log(`Created hooks index: ${indexPath}`);
    }
    
    // Add hook export to index
    const exportLine = `export * from './${hookName}';\n`;
    let indexContent = fs.readFileSync(indexPath, 'utf8');
    
    if (!indexContent.includes(exportLine)) {
      fs.appendFileSync(indexPath, exportLine);
      console.log(`Updated hooks index with ${hookName} export`);
    }
  }
  
  // Log GhostLink integration
  try {
    const ghostlinkDir = process.env.GHOSTLINK_DIR || '/Users/ghost/GhostLink';
    const logCommand = `bash "${ghostlinkDir}/ghostlink_control.sh" speak "Hook ${hookName} created successfully"`;
    execSync(logCommand);
  } catch (error) {
    // Silently fail if GhostLink integration is not available
  }
  
  console.log(`\n✅ Hook ${hookName} created successfully!`);
  console.log(`Location: ${shared ? 'shared' : feature}`);
  console.log(`Path: ${hookFilePath}`);
}

/**
 * Creates a new service
 * @param {Object} options - Service options
 */
function createService(options) {
  const { name, feature } = options;
  
  // Validate service name
  if (!name) {
    console.error('Error: Service name is required');
    process.exit(1);
  }
  
  // Determine service path
  let servicePath;
  if (feature) {
    servicePath = path.join(CONFIG.basePath, CONFIG.featuresPath, feature, 'services');
  } else {
    servicePath = path.join(CONFIG.basePath, 'src/services');
  }
  
  // Create service directory if it doesn't exist
  fs.mkdirSync(servicePath, { recursive: true });
  
  // Create service file
  const serviceName = name.endsWith('Service') ? name : `${name}Service`;
  const serviceFilePath = path.join(servicePath, `${serviceName}.ts`);
  
  // Check if service already exists
  if (fs.existsSync(serviceFilePath)) {
    console.error(`Error: Service file already exists: ${serviceFilePath}`);
    process.exit(1);
  }
  
  // Service template
  const serviceTemplate = `import axios from 'axios';

/**
 * ${serviceName} - Service for handling ${name} API interactions
 */
export const ${serviceName} = {
  /**
   * Get all items
   * @returns Promise resolving to items array
   */
  getAll: async () => {
    try {
      const response = await axios.get('/api/${name.toLowerCase()}');
      return response.data;
    } catch (error) {
      console.error('Error fetching ${name} items:', error);
      throw error;
    }
  },
  
  /**
   * Get item by ID
   * @param id - Item ID
   * @returns Promise resolving to the item
   */
  getById: async (id: string) => {
    try {
      const response = await axios.get(\`/api/${name.toLowerCase()}/\${id}\`);
      return response.data;
    } catch (error) {
      console.error(\`Error fetching ${name} with ID \${id}:\`, error);
      throw error;
    }
  },
  
  /**
   * Create new item
   * @param data - Item data
   * @returns Promise resolving to the created item
   */
  create: async (data: any) => {
    try {
      const response = await axios.post(\`/api/${name.toLowerCase()}\`, data);
      return response.data;
    } catch (error) {
      console.error('Error creating ${name}:', error);
      throw error;
    }
  },
  
  /**
   * Update existing item
   * @param id - Item ID
   * @param data - Updated item data
   * @returns Promise resolving to the updated item
   */
  update: async (id: string, data: any) => {
    try {
      const response = await axios.put(\`/api/${name.toLowerCase()}/\${id}\`, data);
      return response.data;
    } catch (error) {
      console.error(\`Error updating ${name} with ID \${id}:\`, error);
      throw error;
    }
  },
  
  /**
   * Delete item
   * @param id - Item ID
   * @returns Promise resolving to success status
   */
  delete: async (id: string) => {
    try {
      const response = await axios.delete(\`/api/${name.toLowerCase()}/\${id}\`);
      return response.data;
    } catch (error) {
      console.error(\`Error deleting ${name} with ID \${id}:\`, error);
      throw error;
    }
  }
};
`;
  
  fs.writeFileSync(serviceFilePath, serviceTemplate);
  console.log(`Created service: ${serviceFilePath}`);
  
  // Create test file
  const testFilePath = path.join(servicePath, `${serviceName}.test.ts`);
  const testTemplate = `import axios from 'axios';
import { ${serviceName} } from './${serviceName}';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('${serviceName}', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  describe('getAll', () => {
    it('should fetch all items successfully', async () => {
      const mockData = [{ id: '1', name: 'Test' }];
      mockedAxios.get.mockResolvedValueOnce({ data: mockData });
      
      const result = await ${serviceName}.getAll();
      
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/${name.toLowerCase()}');
      expect(result).toEqual(mockData);
    });
    
    it('should handle errors', async () => {
      const mockError = new Error('Network error');
      mockedAxios.get.mockRejectedValueOnce(mockError);
      
      await expect(${serviceName}.getAll()).rejects.toThrow(mockError);
    });
  });
  
  // Add more tests for other methods
});
`;
  
  fs.writeFileSync(testFilePath, testTemplate);
  console.log(`Created test: ${testFilePath}`);
  
  // Create index file if in a feature
  if (feature) {
    const indexPath = path.join(servicePath, 'index.ts');
    
    // Create services index if it doesn't exist
    if (!fs.existsSync(indexPath)) {
      fs.writeFileSync(indexPath, `// Service exports for ${feature}\n`);
      console.log(`Created services index: ${indexPath}`);
    }
    
    // Add service export to index
    const exportLine = `export * from './${serviceName}';\n`;
    let indexContent = fs.readFileSync(indexPath, 'utf8');
    
    if (!indexContent.includes(exportLine)) {
      fs.appendFileSync(indexPath, exportLine);
      console.log(`Updated services index with ${serviceName} export`);
    }
  }
  
  // Log GhostLink integration
  try {
    const ghostlinkDir = process.env.GHOSTLINK_DIR || '/Users/ghost/GhostLink';
    const logCommand = `bash "${ghostlinkDir}/ghostlink_control.sh" speak "Service ${serviceName} created successfully"`;
    execSync(logCommand);
  } catch (error) {
    // Silently fail if GhostLink integration is not available
  }
  
  console.log(`\n✅ Service ${serviceName} created successfully!`);
  console.log(`Location: ${feature ? feature : 'global'}`);
  console.log(`Path: ${serviceFilePath}`);
}

/**
 * Parse command line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const command = args[0];
  const options = {};
  
  for (let i = 1; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const value = args[i+1] && !args[i+1].startsWith('--') ? args[i+1] : true;
      options[key] = value;
      if (value !== true) i++;
    }
  }
  
  return { command, options };
}

/**
 * Main execution function
 */
function main() {
  const { command, options } = parseArgs();
  
  console.log('🚀 GhostLink React Component Generator');
  console.log('=======================================');
  
  switch (command) {
    case 'create-component':
      createComponent(options);
      break;
    
    case 'create-hook':
      createHook(options);
      break;
    
    case 'create-service':
      createService(options);
      break;
    
    case 'help':
      console.log(`
Usage:
  node component-generator.js create-component --name ComponentName --type component --feature featureName [--shared]
  node component-generator.js create-hook --name HookName --feature featureName [--shared]
  node component-generator.js create-service --name ServiceName [--feature featureName]

Options:
  --name       Name of the component, hook, or service
  --type       Component type (${CONFIG.types.join(', ')})
  --feature    Feature name (required for feature-specific components)
  --shared     Flag to create shared component or hook

Examples:
  node component-generator.js create-component --name UserProfile --type component --feature user
  node component-generator.js create-component --name Button --type component --shared
  node component-generator.js create-hook --name useAuth --shared
  node component-generator.js create-service --name UserApi
      `);
      break;
    
    default:
      console.error(`Error: Unknown command '${command}'`);
      console.log('Run "node component-generator.js help" for usage information');
      process.exit(1);
  }
}

// Execute main function
main();
