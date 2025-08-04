'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { motion } from 'framer-motion'
import { Trophy, Star, Award, TrendingUp, Activity, Target } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Laurel, getLaurels, awardLaurel } from '@/lib/utils'

interface LaurelsSectionProps {
  userId: string
}

export function LaurelsSection({ userId }: LaurelsSectionProps) {
  const [laurels, setLaurels] = useState<Laurel[]>([])
  const [loading, setLoading] = useState(true)

  const fetchLaurels = useCallback(async () => {
    try {
      const data = await getLaurels(userId)
      setLaurels(data)
    } catch (error) {
      console.error('Error fetching laurels:', error)
    } finally {
      setLoading(false)
    }
  }, [userId])

  useEffect(() => {
    fetchLaurels()
  }, [fetchLaurels])

  const handleAwardLaurel = async (type: string, points: number, description: string) => {
    try {
      await awardLaurel(userId, type, points, description)
      await fetchLaurels() // Refresh the list
    } catch (error) {
      console.error('Error awarding laurel:', error)
    }
  }

  const totalPoints = laurels.reduce((sum, laurel) => sum + laurel.points, 0)

  const getLaurelIcon = (type: string) => {
    switch (type) {
      case 'first_plan':
        return <Trophy className="h-6 w-6 text-yellow-500" />
      case 'workout_streak':
        return <TrendingUp className="h-6 w-6 text-green-500" />
      case 'goal_achieved':
        return <Award className="h-6 w-6 text-blue-500" />
      default:
        return <Star className="h-6 w-6 text-purple-500" />
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
      {/* Stats Overview */}
      <Card className="glass">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Trophy className="h-5 w-5 text-primary" />
            <span>Your Achievements</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{laurels.length}</div>
              <div className="text-sm text-muted-foreground">Laurels Earned</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{totalPoints}</div>
              <div className="text-sm text-muted-foreground">Total Points</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Laurels List */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Laurels</CardTitle>
        </CardHeader>
        <CardContent>
          {laurels.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              <Trophy className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No laurels earned yet. Start your fitness journey to earn achievements!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {laurels.map((laurel) => (
                <motion.div
                  key={laurel.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex items-center space-x-4 p-4 rounded-lg border bg-card"
                >
                  {getLaurelIcon(laurel.laurel_type)}
                  <div className="flex-1">
                    <h4 className="font-medium capitalize">
                      {laurel.laurel_type.replace('_', ' ')}
                    </h4>
                    <p className="text-sm text-muted-foreground">
                      {laurel.description || 'Achievement unlocked!'}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-primary">+{laurel.points}</div>
                    <div className="text-xs text-muted-foreground">
                      {new Date(laurel.created_at).toLocaleDateString()}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <Button
              variant="outline"
              onClick={() => handleAwardLaurel('workout_completed', 10, 'Completed a workout session')}
              className="h-auto p-4 flex flex-col items-center space-y-2"
            >
              <Activity className="h-5 w-5" />
              <span className="text-sm">Log Workout</span>
            </Button>
            <Button
              variant="outline"
              onClick={() => handleAwardLaurel('goal_set', 5, 'Set a new fitness goal')}
              className="h-auto p-4 flex flex-col items-center space-y-2"
            >
              <Target className="h-5 w-5" />
              <span className="text-sm">Set Goal</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
} 