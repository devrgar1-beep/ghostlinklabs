import { useAuthStore } from "@/lib/store"
import React, { createContext, useContext, useEffect } from 'react'

interface AuthContextType {
  user: any
  isAuthenticated: boolean
  isLoading: boolean
  login: (user: any) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isAuthenticated, isLoading, login, logout, setLoading } = useAuthStore()

  useEffect(() => {
    // Check for existing session on mount
    const checkAuth = async () => {
      setLoading(true)
      try {
        // In a real app, you'd check with your backend
        // For now, we'll just check localStorage
        const storedUser = localStorage.getItem('auth-user')
        if (storedUser) {
          login(JSON.parse(storedUser))
        }
      } catch (error) {
        console.error('Auth check failed:', error)
      } finally {
        setLoading(false)
      }
    }

    checkAuth()
  }, [login, setLoading])

  const value = {
    user,
    isAuthenticated,
    isLoading,
    login,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}