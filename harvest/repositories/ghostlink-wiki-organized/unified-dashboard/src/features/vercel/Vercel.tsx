import { Globe, Settings, Zap } from 'lucide-react'
import React from 'react'
import { Button } from '../../shared/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../shared/components/ui/card'

const Vercel: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Vercel</h1>
        <p className="text-muted-foreground">
          Deploy and monitor your applications.
        </p>
      </div>

      <div className="flex space-x-4">
        <Button>
          <Globe className="h-4 w-4 mr-2" />
          Deploy
        </Button>
        <Button variant="outline">
          <Settings className="h-4 w-4 mr-2" />
          Settings
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Deployments</CardTitle>
          <CardDescription>
            Your recent deployments
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center space-x-4 p-4 border rounded-lg">
              <Zap className="h-8 w-8 text-green-500" />
              <div className="flex-1">
                <h3 className="font-medium">ghostlink-dashboard</h3>
                <p className="text-sm text-muted-foreground">Deployed 1 hour ago</p>
              </div>
              <Button variant="ghost" size="sm">View</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Vercel