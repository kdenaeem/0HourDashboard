import { openai } from "@ai-sdk/openai"
import { streamText } from "ai"

// Allow streaming responses up to 30 seconds
export const maxDuration = 30

export async function POST(req: Request) {
  const { messages } = await req.json()

  const result = streamText({
    model: openai("gpt-4o"),
    system:
      "You are a helpful assistant that helps users manage their Google Tasks and Calendar. You can provide suggestions, reminders, and help organize their schedule efficiently.",
    messages,
  })

  return result.toDataStreamResponse()
}

