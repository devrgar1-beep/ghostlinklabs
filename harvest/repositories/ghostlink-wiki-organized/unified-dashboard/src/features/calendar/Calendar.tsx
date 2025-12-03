import { Clock, Plus } from 'lucide-react'
import React from 'react'
import { Button } from '../../shared/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../shared/components/ui/card'

const CalendarComponent: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Calendar</h1>
        <p className="text-muted-foreground">
          View and manage your schedule and events.
        </p>
      </div>

      <div className="flex space-x-4">
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          New Event
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Today's Events</CardTitle>
          <CardDescription>
            Your schedule for today
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center space-x-4 p-4 border rounded-lg">
              <Clock className="h-8 w-8 text-blue-500" />
              <div className="flex-1">
                <h3 className="font-medium">Team Meeting</h3>
                <p className="text-sm text-muted-foreground">2:00 PM - 3:00 PM</p>
              </div>
              <Button variant="ghost" size="sm">Join</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default CalendarComponent