'use client'

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { MessageCircle, Trophy, Activity, Menu, X } from 'lucide-react'
import { ChatInterface } from '@/components/chat/chat-interface'
import { LaurelsSection } from '@/components/dashboard/laurels-section'
import { ProgressSection } from '@/components/dashboard/progress-section'
import { generateUserId } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { AnimatePresence } from 'framer-motion'

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<'chat' | 'laurels' | 'progress'>('chat')
  const [userId, setUserId] = useState<string>('')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [isClient, setIsClient] = useState(false)

  // Only generate user ID on client side to prevent hydration mismatch
  useEffect(() => {
    setIsClient(true)
    setUserId(generateUserId())
  }, [])

  const tabs = [
    { id: 'chat', label: 'AI Coach', icon: MessageCircle },
    { id: 'laurels', label: 'Achievements', icon: Trophy },
    { id: 'progress', label: 'Progress', icon: Activity },
  ] as const

  // Don't render until client-side to prevent hydration issues
  if (!isClient) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading Empyre...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      {/* Mobile Sidebar */}
      <div className="lg:hidden">
        <div className="fixed top-4 left-4 z-50">
          <Button
            variant="outline"
            size="icon"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="bg-background/80 backdrop-blur-sm"
          >
            {sidebarOpen ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
          </Button>
        </div>

        {sidebarOpen && (
          <motion.div
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            exit={{ x: -300 }}
            className="fixed left-0 top-0 h-full w-80 bg-background/95 backdrop-blur-sm border-r z-40"
          >
            <div className="p-6">
              <div className="flex items-center space-x-3 mb-8">
                <div className="p-2 bg-primary/10 rounded-lg">
                  <Trophy className="h-6 w-6 text-primary" />
                </div>
                <div>
                  <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
                    Empyre
                  </h1>
                  <p className="text-xs text-muted-foreground">AI Fitness Coach</p>
                </div>
              </div>

              <nav className="space-y-2">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => {
                      setActiveTab(tab.id)
                      setSidebarOpen(false)
                    }}
                    className={`w-full flex items-center space-x-3 p-3 rounded-lg text-left transition-colors ${
                      activeTab === tab.id
                        ? 'bg-primary text-primary-foreground'
                        : 'hover:bg-muted'
                    }`}
                  >
                    <tab.icon className="h-5 w-5" />
                    <span className="font-medium">{tab.label}</span>
                  </button>
                ))}
              </nav>
            </div>
          </motion.div>
        )}
      </div>

      {/* Desktop Layout */}
      <div className="flex h-screen">
        {/* Desktop Sidebar */}
        <div className="hidden lg:flex lg:w-80 lg:flex-col lg:fixed lg:inset-y-0">
          <div className="flex flex-col flex-grow bg-background/80 backdrop-blur-sm border-r pt-5 pb-4 overflow-y-auto">
            <div className="flex items-center flex-shrink-0 px-6 mb-8">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-primary/10 rounded-lg">
                  <Trophy className="h-6 w-6 text-primary" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
                    Empyre
                  </h1>
                  <p className="text-sm text-muted-foreground">AI Fitness Coach</p>
                </div>
              </div>
            </div>

            <nav className="flex-1 px-6 space-y-2">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center space-x-3 p-3 rounded-lg text-left transition-colors ${
                    activeTab === tab.id
                      ? 'bg-primary text-primary-foreground shadow-lg'
                      : 'hover:bg-muted'
                  }`}
                >
                  <tab.icon className="h-5 w-5" />
                  <span className="font-medium">{tab.label}</span>
                </button>
              ))}
            </nav>

            <div className="px-6 py-4 border-t">
              <div className="text-xs text-muted-foreground">
                User ID: {userId}
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="lg:pl-80 flex-1 flex flex-col">
          <main className="flex-1 overflow-hidden">
            <AnimatePresence mode="wait">
              {activeTab === 'chat' && (
                <motion.div
                  key="chat"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="h-full"
                >
                  <ChatInterface userId={userId} />
                </motion.div>
              )}

              {activeTab === 'laurels' && (
                <motion.div
                  key="laurels"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="h-full overflow-y-auto p-6"
                >
                  <LaurelsSection userId={userId} />
                </motion.div>
              )}

              {activeTab === 'progress' && (
                <motion.div
                  key="progress"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="h-full overflow-y-auto p-6"
                >
                  <ProgressSection userId={userId} />
                </motion.div>
              )}
            </AnimatePresence>
          </main>
        </div>
      </div>
    </div>
  )
}
