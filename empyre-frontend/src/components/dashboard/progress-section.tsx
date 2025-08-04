'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { motion } from 'framer-motion'
import { Activity, Calendar, Target, Plus, BarChart3 } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ProgressLog, getProgress, logProgress, formatDate } from '@/lib/utils'

interface ProgressSectionProps {
  userId: string
}

export function ProgressSection({ userId }: ProgressSectionProps) {
  const [progressLogs, setProgressLogs] = useState<ProgressLog[]>([])
  const [loading, setLoading] = useState(true)
  const [showLogForm, setShowLogForm] = useState(false)
  const [logForm, setLogForm] = useState({
    type: 'workout',
    duration: '',
    exercises: '',
    notes: ''
  })

  const fetchProgress = useCallback(async () => {
    try {
      const data = await getProgress(userId)
      setProgressLogs(data)
    } catch (error) {
      console.error('Error fetching progress:', error)
    } finally {
      setLoading(false)
    }
  }, [userId])

  useEffect(() => {
    fetchProgress()
  }, [fetchProgress])

  const handleLogProgress = async () => {
    try {
      const logData = {
        type: logForm.type,
        duration: parseInt(logForm.duration) || 0,
        exercises: logForm.exercises.split(',').map(e => e.trim()).filter(Boolean),
        notes: logForm.notes
      }

      await logProgress(userId, logForm.type, logData)
      await fetchProgress()
      
      // Reset form
      setLogForm({
        type: 'workout',
        duration: '',
        exercises: '',
        notes: ''
      })
      setShowLogForm(false)
    } catch (error) {
      console.error('Error logging progress:', error)
    }
  }

  const getLogIcon = (type: string) => {
    switch (type) {
      case 'workout':
        return <Activity className="h-5 w-5 text-green-500" />
      case 'measurement':
        return <BarChart3 className="h-5 w-5 text-blue-500" />
      case 'goal':
        return <Target className="h-5 w-5 text-purple-500" />
      default:
        return <Calendar className="h-5 w-5 text-gray-500" />
    }
  }

  if (loading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-muted rounded w-1/4"></div>
            <div className="space-y-2">
              <div className="h-4 bg-muted rounded"></div>
              <div className="h-4 bg-muted rounded w-5/6"></div>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {/* Quick Log */}
      <Card className="glass">
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span className="flex items-center space-x-2">
              <Activity className="h-5 w-5 text-primary" />
              <span>Progress Tracking</span>
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowLogForm(!showLogForm)}
            >
              <Plus className="h-4 w-4 mr-2" />
              Log Progress
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {showLogForm && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="space-y-4 p-4 border rounded-lg bg-background"
            >
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Type</label>
                  <select
                    value={logForm.type}
                    onChange={(e) => setLogForm({ ...logForm, type: e.target.value })}
                    className="w-full mt-1 p-2 border rounded-md bg-background"
                  >
                    <option value="workout">Workout</option>
                    <option value="measurement">Measurement</option>
                    <option value="goal">Goal</option>
                  </select>
                </div>
                <div>
                  <label className="text-sm font-medium">Duration (minutes)</label>
                  <Input
                    type="number"
                    value={logForm.duration}
                    onChange={(e) => setLogForm({ ...logForm, duration: e.target.value })}
                    placeholder="45"
                  />
                </div>
              </div>
              <div>
                <label className="text-sm font-medium">Exercises (comma-separated)</label>
                <Input
                  value={logForm.exercises}
                  onChange={(e) => setLogForm({ ...logForm, exercises: e.target.value })}
                  placeholder="Squats, Deadlifts, Bench Press"
                />
              </div>
              <div>
                <label className="text-sm font-medium">Notes</label>
                <Input
                  value={logForm.notes}
                  onChange={(e) => setLogForm({ ...logForm, notes: e.target.value })}
                  placeholder="How did the workout feel?"
                />
              </div>
              <div className="flex space-x-2">
                <Button onClick={handleLogProgress} className="flex-1">
                  Log Progress
                </Button>
                <Button
                  variant="outline"
                  onClick={() => setShowLogForm(false)}
                >
                  Cancel
                </Button>
              </div>
            </motion.div>
          )}
        </CardContent>
      </Card>

      {/* Progress History */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Progress</CardTitle>
        </CardHeader>
        <CardContent>
          {progressLogs.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              <Activity className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No progress logged yet. Start tracking your fitness journey!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {progressLogs.map((log) => (
                <motion.div
                  key={log.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex items-start space-x-4 p-4 rounded-lg border bg-card"
                >
                  {getLogIcon(log.log_type)}
                  <div className="flex-1">
                    <h4 className="font-medium capitalize">
                      {log.log_type}
                    </h4>
                    <div className="text-sm text-muted-foreground space-y-1">
                      <p>Type: {log.log_type}</p>
                      <p>Logged: {formatDate(log.created_at)}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-muted-foreground">
                      {formatDate(log.created_at)}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
} 