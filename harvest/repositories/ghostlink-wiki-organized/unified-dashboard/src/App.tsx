import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import { Toaster } from 'sonner'
import './App.css'
import Calendar from './features/calendar/Calendar'
import Cloudflare from './features/cloudflare/Cloudflare'
import Dashboard from './features/dashboard/Dashboard'
import Gmail from './features/gmail/Gmail'
import GoogleDrive from './features/google-drive/GoogleDrive'
import Vercel from './features/vercel/Vercel'
import Layout from './shared/components/Layout'
import { AuthProvider } from './shared/hooks/useAuth'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/drive" element={<GoogleDrive />} />
              <Route path="/gmail" element={<Gmail />} />
              <Route path="/calendar" element={<Calendar />} />
              <Route path="/vercel" element={<Vercel />} />
              <Route path="/cloudflare" element={<Cloudflare />} />
            </Routes>
          </Layout>
          <Toaster position="top-right" />
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App