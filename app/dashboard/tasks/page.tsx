import { DashboardHeader } from "@/components/dashboard-header"
import { TasksList } from "@/components/tasks-list"
import { Card, CardContent } from "@/components/ui/card"

export default function TasksPage() {
  return (
    <div className="space-y-6">
      <DashboardHeader title="Tasks" description="Manage your to-do list" />

      <Card>
        <CardContent className="p-6">
          <TasksList fullView />
        </CardContent>
      </Card>
    </div>
  )
}

