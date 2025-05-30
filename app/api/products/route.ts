import { type NextRequest, NextResponse } from "next/server"

// This would be replaced with actual product data from the Excel file
const mockProducts = Array(30)
  .fill(null)
  .map((_, i) => {
    const categories = ["Cleansers", "Moisturizers", "Serums", "Masks", "Toners"]
    const randomCategory = categories[Math.floor(Math.random() * categories.length)]

    return {
      id: i + 1,
      name: `${randomCategory.slice(0, -1)} ${i + 1}`,
      category: randomCategory,
      price: Math.floor(Math.random() * 30) + 10,
      margin: Math.floor(Math.random() * 40) + 30,
      image: `/placeholder.svg?height=200&width=200`,
      description: `A premium skincare product for all skin types.`,
    }
  })

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const category = searchParams.get("category")

    let filteredProducts = mockProducts

    if (category) {
      filteredProducts = mockProducts.filter((p) => p.category === category)
    }

    return NextResponse.json(filteredProducts)
  } catch (error) {
    console.error("Error fetching products:", error)
    return NextResponse.json({ error: "Failed to fetch products" }, { status: 500 })
  }
}
