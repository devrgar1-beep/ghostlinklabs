import { Inbox, Mail, Send } from 'lucide-react'
import React from 'react'
import { Button } from '../../shared/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../shared/components/ui/card'

const Gmail: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Gmail</h1>
        <p className="text-muted-foreground">
          Access and manage your email messages.
        </p>
      </div>

      <div className="flex space-x-4">
        <Button>
          <Send className="h-4 w-4 mr-2" />
          Compose
        </Button>
        <Button variant="outline">
          <Inbox className="h-4 w-4 mr-2" />
          Inbox
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Messages</CardTitle>
          <CardDescription>
            Your latest email conversations
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center space-x-4 p-4 border rounded-lg">
              <Mail className="h-8 w-8 text-red-500" />
              <div className="flex-1">
                <h3 className="font-medium">Welcome to GhostLink</h3>
                <p className="text-sm text-muted-foreground">From: support@ghostlink.com</p>
              </div>
              <Button variant="ghost" size="sm">Read</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Gmail