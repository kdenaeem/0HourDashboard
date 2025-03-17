"use client"

import { useState } from "react"
import { Calendar } from "@/components/ui/calendar"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface CalendarViewProps {
  fullView?: boolean
}

// Mock data for calendar events
const mockEvents = [
  { id: 1, title: "Team Meeting", date: new Date(2025, 2, 18, 10, 0), duration: 60 },
  { id: 2, title: "Project Review", date: new Date(2025, 2, 19, 14, 0), duration: 90 },
  { id: 3, title: "Client Call", date: new Date(2025, 2, 20, 11, 30), duration: 45 },
]

export function CalendarView({ fullView = false }: CalendarViewProps) {
  const [date, setDate] = useState<Date | undefined>(new Date())

  // Get events for the selected date
  const selectedDateEvents = mockEvents.filter((event) => date && event.date.toDateString() === date.toDateString())

  return (
    <div className={`space-y-4 ${fullView ? "h-[calc(100vh-16rem)]" : ""}`}>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Calendar mode="single" selected={date} onSelect={setDate} className="rounded-md border" />

        <div className="space-y-2">
          <h3 className="font-medium">Events for {date?.toLocaleDateString()}</h3>
          {selectedDateEvents.length > 0 ? (
            <div className="space-y-2">
              {selectedDateEvents.map((event) => (
                <Card key={event.id}>
                  <CardContent className="p-3">
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-medium">{event.title}</p>
                        <p className="text-sm text-muted-foreground">
                          {event.date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                          {" - "}
                          {new Date(event.date.getTime() + event.duration * 60000).toLocaleTimeString([], {
                            hour: "2-digit",
                            minute: "2-digit",
                          })}
                        </p>
                      </div>
                      <Badge>{event.duration} min</Badge>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <p className="text-muted-foreground">No events scheduled for this day.</p>
          )}
        </div>
      </div>
    </div>
  )
}

