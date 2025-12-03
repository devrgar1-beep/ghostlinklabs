import { Activity, Calendar, Cloud, HardDrive, Mail, Zap } from 'lucide-react'
import React from 'react'
import { Button } from '../../shared/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../shared/components/ui/card'

const Dashboard: React.FC = () => {
  const services = [
    {
      name: 'Google Drive',
      icon: HardDrive,
      description: 'Manage your files and documents',
      status: 'Connected',
      href: '/drive',
    },
    {
      name: 'Gmail',
      icon: Mail,
      description: 'Access your email and messages',
      status: 'Connected',
      href: '/gmail',
    },
    {
      name: 'Calendar',
      icon: Calendar,
      description: 'View and manage your schedule',
      status: 'Connected',
      href: '/calendar',
    },
    {
      name: 'Vercel',
      icon: Zap,
      description: 'Deploy and monitor your applications',
      status: 'Connected',
      href: '/vercel',
    },
    {
      name: 'Cloudflare',
      icon: Cloud,
      description: 'Manage your DNS and security',
      status: 'Connected',
      href: '/cloudflare',
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome to GhostLink Unified Dashboard. Manage all your services in one place.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {services.map((service) => {
          const Icon = service.icon
          return (
            <Card key={service.name} className="hover:shadow-md transition-shadow">
              <CardHeader className="flex flex-row items-center space-y-0 pb-2">
                <Icon className="h-8 w-8 text-primary" />
                <div className="ml-4">
                  <CardTitle className="text-lg">{service.name}</CardTitle>
                  <CardDescription>{service.description}</CardDescription>
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">
                    Status: <span className="text-green-600">{service.status}</span>
                  </span>
                  <Button variant="outline" size="sm" asChild>
                    <a href={service.href}>Open</a>
                  </Button>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Activity className="h-5 w-5" />
            <span>System Overview</span>
          </CardTitle>
          <CardDescription>
            Current status of all integrated services
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">5</div>
              <div className="text-sm text-muted-foreground">Services Connected</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">0</div>
              <div className="text-sm text-muted-foreground">Active Alerts</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">100%</div>
              <div className="text-sm text-muted-foreground">Uptime</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">2.1s</div>
              <div className="text-sm text-muted-foreground">Avg Response Time</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard