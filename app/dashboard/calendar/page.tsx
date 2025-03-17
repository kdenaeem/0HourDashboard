import { DashboardHeader } from "@/components/dashboard-header"
import { CalendarView } from "@/components/calendar-view"
import { Card, CardContent } from "@/components/ui/card"

export default function CalendarPage() {
  return (
    <div className="space-y-6">
      <DashboardHeader title="Calendar" description="View and manage your schedule" />

      <Card>
        <CardContent className="p-6">
          <CalendarView fullView />
        </CardContent>
      </Card>
    </div>
  )
}

