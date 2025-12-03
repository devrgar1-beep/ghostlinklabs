import { Cloud, Settings, Shield } from 'lucide-react'
import React from 'react'
import { Button } from '../../shared/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../shared/components/ui/card'

const Cloudflare: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Cloudflare</h1>
        <p className="text-muted-foreground">
          Manage your DNS and security settings.
        </p>
      </div>

      <div className="flex space-x-4">
        <Button>
          <Shield className="h-4 w-4 mr-2" />
          Security
        </Button>
        <Button variant="outline">
          <Settings className="h-4 w-4 mr-2" />
          DNS
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Domains</CardTitle>
          <CardDescription>
            Your managed domains
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center space-x-4 p-4 border rounded-lg">
              <Cloud className="h-8 w-8 text-orange-500" />
              <div className="flex-1">
                <h3 className="font-medium">ghostlinklabs.com</h3>
                <p className="text-sm text-muted-foreground">Active • SSL: Valid</p>
              </div>
              <Button variant="ghost" size="sm">Manage</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Cloudflare