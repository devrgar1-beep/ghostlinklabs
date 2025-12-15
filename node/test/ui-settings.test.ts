import request from 'supertest'
import { MCPServerCoordinator } from '../src/mcp-coordinator'

describe('UI settings API', () => {
  let coordinator: any

  beforeAll(() => {
    coordinator = new (require('../src/mcp-coordinator').MCPServerCoordinator)()
  })

  it('should return ui settings', async () => {
    const res = await request(coordinator['app']).get('/api/ui/settings')
    expect(res.status).toBe(200)
    expect(res.body).toHaveProperty('uiTransparent')
    expect(res.body).toHaveProperty('uiAlpha')
  })

  it('should accept POST to update settings', async () => {
    const res = await request(coordinator['app']).post('/api/ui/settings').send({ uiTransparent: true, uiAlpha: 0.12 })
    expect(res.status).toBe(200)
    expect(res.body).toHaveProperty('success')
  })
})
