import { Calendar, Cloud, HardDrive, Home, Mail, Menu, Zap } from 'lucide-react'
import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Button } from './ui/button'

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Google Drive', href: '/drive', icon: HardDrive },
  { name: 'Gmail', href: '/gmail', icon: Mail },
  { name: 'Calendar', href: '/calendar', icon: Calendar },
  { name: 'Vercel', href: '/vercel', icon: Zap },
  { name: 'Cloudflare', href: '/cloudflare', icon: Cloud },
]

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <div className={`w-64 bg-card border-r ${sidebarOpen ? 'block' : 'hidden'} md:block fixed md:relative z-10 h-full`}>
        <div className="p-4 border-b">
          <h1 className="text-xl font-bold text-foreground">GhostLink</h1>
        </div>
        <nav className="p-4">
          <ul className="space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.href
              return (
                <li key={item.name}>
                  <Link
                    to={item.href}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-md transition-colors ${
                      isActive
                        ? 'bg-primary text-primary-foreground'
                        : 'hover:bg-accent hover:text-accent-foreground'
                    }`}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <Icon className="h-5 w-5" />
                    <span>{item.name}</span>
                  </Link>
                </li>
              )
            })}
          </ul>
        </nav>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden md:ml-0">
        <header className="bg-card border-b px-4 py-3 flex items-center justify-between">
          <Button
            variant="ghost"
            size="sm"
            className="md:hidden"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            <Menu className="h-6 w-6" />
          </Button>
          <div className="flex items-center space-x-4 ml-auto">
            <Button variant="outline" size="sm">
              Settings
            </Button>
          </div>
        </header>

        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-5 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  )
}

export default Layout