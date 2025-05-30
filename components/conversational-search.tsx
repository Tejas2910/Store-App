"use client"

import type React from "react"

import { useState } from "react"
import { Send, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface ConversationalSearchProps {
  onResults: (results: any[]) => void
}

export default function ConversationalSearch({ onResults }: ConversationalSearchProps) {
  const [query, setQuery] = useState("")
  const [conversation, setConversation] = useState<
    {
      type: "user" | "assistant" | "thinking"
      content: string
    }[]
  >([])
  const [loading, setLoading] = useState(false)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    // Add user message to conversation
    setConversation([...conversation, { type: "user", content: query }])
    setLoading(true)

    try {
      // In a real implementation, this would call your backend API
      // For now, we'll simulate a response
      setTimeout(() => {
        let response

        if (query.toLowerCase().includes("serum") || query.toLowerCase().includes("moisturizer")) {
          // Specific product query
          response = `Based on your interest in ${query.toLowerCase().includes("serum") ? "serums" : "moisturizers"}, would you prefer products for sensitive, oily, or dry skin?`
        } else if (query.toLowerCase().includes("sensitive") || query.toLowerCase().includes("gentle")) {
          // Specific concern
          response =
            "I've found some gentle products for sensitive skin. Would you prefer a cleanser, moisturizer, or serum?"
        } else if (query.toLowerCase().includes("is") || query.toLowerCase().includes("how")) {
          // FAQ-type question
          response =
            "Based on our product information and customer reviews, our Vitamin C serum is suitable for most skin types, including sensitive skin when used as directed. Many customers with sensitive skin have reported positive results without irritation."
        } else {
          // General query
          response =
            "I'd like to help you find the right skincare products. Could you tell me your skin type (dry, oily, combination, sensitive) and what specific concerns you're looking to address?"
        }

        setConversation((prev) => [...prev, { type: "assistant", content: response }])

        // Simulate product results for demonstration
        if (query.toLowerCase().includes("serum")) {
          const serumProducts = [
            {
              id: "SRM001",
              name: "Radiant Renewal Serum",
              category: "Serum",
              description: "Brightens dull skin and smooths fine lines for a lit-from-within glow.",
              top_ingredients: "Ascorbic Acid (Vitamin C); Hyaluronic Acid; Niacinamide",
              tags: ["antiaging", "brightening", "hydration"],
              price: 72,
              margin: 0.45,
              image: `/placeholder.svg?height=200&width=200`,
            },
            {
              id: "SRM002",
              name: "Dewdrop Hydration Elixir",
              category: "Serum",
              description: "Water-weight serum that drenches skin in long-lasting moisture and repairs the barrier.",
              top_ingredients: "Hyaluronic Acid; Panthenol; Vitamin F (Linoleic Acid)",
              tags: ["hydration", "barrier-repair", "dry-skin"],
              price: 58,
              margin: 0.42,
              image: `/placeholder.svg?height=200&width=200`,
            },
            {
              id: "SRM005",
              name: "Calm & Soothe Sensitive Serum",
              category: "Serum",
              description: "Lightweight gel serum that calms redness and strengthens sensitive skin.",
              top_ingredients: "Centella Asiatica; Allantoin; Beta-Glucan",
              tags: ["sensitive", "redness-relief", "hydration"],
              price: 49,
              margin: 0.38,
              image: `/placeholder.svg?height=200&width=200`,
            },
            {
              id: "SRM009",
              name: "Sunrise Retinal Serum",
              category: "Serum",
              description: "Next-gen retinaldehyde visibly smooths wrinkles with less irritation.",
              top_ingredients: "Retinaldehyde; Bakuchiol; Hyaluronic Acid",
              tags: ["antiaging", "fine-lines", "brightening"],
              price: 95,
              margin: 0.55,
              image: `/placeholder.svg?height=200&width=200`,
            },
          ]

          // Sort by margin (highest first)
          onResults(serumProducts.sort((a, b) => b.margin - a.margin))
        } else if (query.toLowerCase().includes("moisturizer")) {
          const moisturizerProducts = [
            {
              id: "CRM002",
              name: "Velvet Night Repair Cream",
              category: "Cream / Moisturizer",
              description:
                "Luxurious overnight treatment that boosts collagen and repairs the skin barrier while you sleep.",
              top_ingredients: "Retinol; Peptides; Squalane",
              tags: ["night-repair", "antiaging", "dry-skin"],
              price: 68,
              margin: 0.48,
              image: `/placeholder.svg?height=200&width=200`,
            },
            {
              id: "CRM003",
              name: "Radiance Spot-Bright Eye Cream",
              category: "Cream / Moisturizer",
              description: "Brightens dark circles and smooths fine lines around delicate eye area.",
              top_ingredients: "Vitamin C; Caffeine; Niacinamide",
              tags: ["eye-care", "brightening", "antiaging", "hydration"],
              price: 55,
              margin: 0.46,
              image: `/placeholder.svg?height=200&width=200`,
            },
          ]

          onResults(moisturizerProducts.sort((a, b) => b.margin - a.margin))
        }

        setLoading(false)
        setQuery("")
      }, 1500)
    } catch (error) {
      console.error("Error fetching response:", error)
      setConversation((prev) => [
        ...prev,
        {
          type: "assistant",
          content: "I'm sorry, I encountered an error. Please try again.",
        },
      ])
      setLoading(false)
    }
  }

  return (
    <div className="w-full">
      <form onSubmit={handleSearch} className="flex items-center space-x-2 mb-4">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about products or describe what you're looking for..."
          className="flex-1"
          disabled={loading}
        />
        <Button type="submit" size="icon" disabled={loading}>
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
        </Button>
      </form>

      {conversation.length > 0 && (
        <div className="space-y-3 mb-4">
          {conversation.map((message, index) => (
            <div
              key={index}
              className={`p-3 rounded-lg ${
                message.type === "user" ? "bg-primary/10 ml-auto max-w-[80%]" : "bg-gray-100 mr-auto max-w-[80%]"
              }`}
            >
              {message.content}
            </div>
          ))}
          {loading && (
            <div className="bg-gray-100 p-3 rounded-lg flex items-center space-x-2 mr-auto max-w-[80%]">
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Thinking...</span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
