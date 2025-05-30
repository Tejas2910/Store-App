// app/reviews/[productId]/page.tsx
"use client"

import { useParams } from "next/navigation"
import { useState, useEffect } from "react"
import Rating from '@mui/material/Rating'

interface Review {
  id: string
  productId: string
  rating: number
  description: string
}

export default function ReviewPage() {
  const { productId } = useParams()
  const [reviews, setReviews] = useState<Review[]>([])
  const [userRating, setUserRating] = useState<number | null>(null)
  const [description, setDescription] = useState("")

  useEffect(() => {
    // Fetch reviews for this product from backend API
    fetch(`/api/reviews?productId=${productId}`)
      .then(res => res.json())
      .then(data => setReviews(data))
  }, [productId])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!userRating) return
    // Post review to backend
    await fetch(`/api/reviews`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ productId, rating: userRating, description })
    })
    // Refresh reviews
    fetch(`/api/reviews?productId=${productId}`)
      .then(res => res.json())
      .then(data => setReviews(data))
    setUserRating(null)
    setDescription("")
  }

  const averageRating = reviews.length
    ? reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length
    : 0

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-2">Product Reviews</h1>
      <div className="mb-4">
        <Rating value={averageRating} precision={0.5} readOnly />
        <span className="ml-2 text-gray-700">
          {averageRating ? averageRating.toFixed(1) : "No ratings yet"} ({reviews.length} reviews)
        </span>
      </div>
      <form onSubmit={handleSubmit} className="mb-6">
        <div className="mb-2">
          <Rating
            name="user-rating"
            value={userRating}
            onChange={(_, newValue) => setUserRating(newValue)}
          />
        </div>
        <textarea
          className="w-full border rounded p-2 mb-2"
          placeholder="Write your review..."
          value={description}
          onChange={e => setDescription(e.target.value)}
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded" type="submit">
          Submit Review
        </button>
      </form>
      <div>
        <h2 className="text-lg font-semibold mb-2">All Reviews</h2>
        {reviews.length === 0 ? (
          <p>No reviews for this product yet.</p>
        ) : (
          reviews.map((review) => (
            <div key={review.id} className="border-b py-2">
              <Rating value={review.rating} readOnly size="small" />
              <p className="text-sm">{review.description}</p>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
