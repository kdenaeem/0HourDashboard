import { DashboardHeader } from "@/components/dashboard-header"
import { ChatInterface } from "@/components/chat-interface"
import { Card, CardContent } from "@/components/ui/card"

export default function AssistantPage() {
  return (
    <div className="space-y-6">
      <DashboardHeader title="AI Assistant" description="Get help managing your schedule and tasks" />

      <Card className="h-[calc(100vh-12rem)]">
        <CardContent className="p-6 h-full">
          <ChatInterface />
        </CardContent>
      </Card>
    </div>
  )
}

