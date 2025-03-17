"use client"

import { useState } from "react"
import { Checkbox } from "@/components/ui/checkbox"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Plus, Trash2 } from "lucide-react"

interface TasksListProps {
  fullView?: boolean
}

// Mock data for tasks
const initialTasks = [
  { id: 1, title: "Prepare presentation for meeting", completed: false },
  { id: 2, title: "Review project proposal", completed: false },
  { id: 3, title: "Send follow-up emails", completed: true },
  { id: 4, title: "Update weekly report", completed: false },
]

export function TasksList({ fullView = false }: TasksListProps) {
  const [tasks, setTasks] = useState(initialTasks)
  const [newTaskTitle, setNewTaskTitle] = useState("")

  const toggleTaskCompletion = (taskId: number) => {
    setTasks(tasks.map((task) => (task.id === taskId ? { ...task, completed: !task.completed } : task)))
  }

  const addTask = () => {
    if (newTaskTitle.trim()) {
      const newTask = {
        id: Math.max(0, ...tasks.map((t) => t.id)) + 1,
        title: newTaskTitle.trim(),
        completed: false,
      }
      setTasks([...tasks, newTask])
      setNewTaskTitle("")
    }
  }

  const deleteTask = (taskId: number) => {
    setTasks(tasks.filter((task) => task.id !== taskId))
  }

  return (
    <div className={`space-y-4 ${fullView ? "min-h-[calc(100vh-16rem)]" : ""}`}>
      <div className="flex space-x-2">
        <Input
          placeholder="Add a new task..."
          value={newTaskTitle}
          onChange={(e) => setNewTaskTitle(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && addTask()}
        />
        <Button onClick={addTask}>
          <Plus className="h-4 w-4" />
        </Button>
      </div>

      <div className="space-y-2">
        {tasks.length > 0 ? (
          tasks.map((task) => (
            <div key={task.id} className="flex items-center justify-between p-2 rounded-md border">
              <div className="flex items-center space-x-2">
                <Checkbox
                  checked={task.completed}
                  onCheckedChange={() => toggleTaskCompletion(task.id)}
                  id={`task-${task.id}`}
                />
                <label
                  htmlFor={`task-${task.id}`}
                  className={`text-sm ${task.completed ? "line-through text-muted-foreground" : ""}`}
                >
                  {task.title}
                </label>
              </div>
              <Button variant="ghost" size="sm" onClick={() => deleteTask(task.id)}>
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          ))
        ) : (
          <p className="text-center text-muted-foreground py-4">No tasks yet. Add one above!</p>
        )}
      </div>
    </div>
  )
}

