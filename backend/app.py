from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import docx
import re

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Product data from the spreadsheet
product_data = [
    {
        "id": "SRM001",
        "name": "Radiant Renewal Serum",
        "category": "Serum",
        "description": "Brightens dull skin and smooths fine lines for a lit-from-within glow.",
        "top_ingredients": "Ascorbic Acid (Vitamin C); Hyaluronic Acid; Niacinamide",
        "tags": ["antiaging", "brightening", "hydration"],
        "price": 72,
        "margin": 0.45
    },
    {
        "id": "SRM002",
        "name": "Dewdrop Hydration Elixir",
        "category": "Serum",
        "description": "Water-weight serum that drenches skin in long-lasting moisture and repairs the barrier.",
        "top_ingredients": "Hyaluronic Acid; Panthenol; Vitamin F (Linoleic Acid)",
        "tags": ["hydration", "barrier-repair", "dry-skin"],
        "price": 58,
        "margin": 0.42
    },
    {
        "id": "SRM003",
        "name": "Clear Slate BHA Serum",
        "category": "Serum",
        "description": "Clarifies congested pores and keeps oil in check without over-drying.",
        "top_ingredients": "Salicylic Acid; Zinc PCA; Green-Tea Extract",
        "tags": ["acne-prone", "oil-control", "pore-care"],
        "price": 46,
        "margin": 0.4
    },
    {
        "id": "SRM004",
        "name": "Midnight Peptide Firming Serum",
        "category": "Serum",
        "description": "Overnight peptide complex visibly firms and nourishes mature skin.",
        "top_ingredients": "Palmitoyl Tripeptide-5; Soluble Collagen; Vitamin E",
        "tags": ["antiaging", "firming", "dry-skin"],
        "price": 85,
        "margin": 0.52
    },
    {
        "id": "SRM005",
        "name": "Calm & Soothe Sensitive Serum",
        "category": "Serum",
        "description": "Lightweight gel serum that calms redness and strengthens sensitive skin.",
        "top_ingredients": "Centella Asiatica; Allantoin; Beta-Glucan",
        "tags": ["sensitive", "redness-relief", "hydration"],
        "price": 49,
        "margin": 0.38
    },
    {
        "id": "SRM006",
        "name": "Flash Fade Spot Corrector",
        "category": "Serum",
        "description": "Targets dark spots and post-acne marks for an even, luminous tone.",
        "top_ingredients": "Tranexamic Acid; Niacinamide; Licorice Root Extract",
        "tags": ["brightening", "antiaging", "hyperpigmentation"],
        "price": 79,
        "margin": 0.5
    },
    {
        "id": "SRM007",
        "name": "Velvet Matte Pore Serum",
        "category": "Serum",
        "description": "Blurs shine and minimizes pores for a soft-focus finish.",
        "top_ingredients": "Niacinamide; Tremella Mushroom Extract; Willow-Bark",
        "tags": ["oily-skin", "pore-refining", "matte"],
        "price": 54,
        "margin": 0.41
    },
    {
        "id": "SRM008",
        "name": "AquaShield Barrier Booster",
        "category": "Serum",
        "description": "Ceramide-rich serum that reinforces the lipid barrier and locks in moisture.",
        "top_ingredients": "Ceramides NP+AP+EOP; Vitamin F; Squalane",
        "tags": ["hydration", "barrier-repair", "dry-skin"],
        "price": 65,
        "margin": 0.44
    },
    {
        "id": "SRM009",
        "name": "Sunrise Retinal Serum",
        "category": "Serum",
        "description": "Next-gen retinaldehyde visibly smooths wrinkles with less irritation.",
        "top_ingredients": "Retinaldehyde; Bakuchiol; Hyaluronic Acid",
        "tags": ["antiaging", "fine-lines", "brightening"],
        "price": 95,
        "margin": 0.55
    },
    {
        "id": "SRM010",
        "name": "Glow Guard Antioxidant Serum",
        "category": "Serum",
        "description": "Potent antioxidant trio defends against pollution and UV stress.",
        "top_ingredients": "Ferulic Acid; Ascorbic Acid (Vit C); Vitamin E",
        "tags": ["antioxidant", "brightening", "antiaging"],
        "price": 82,
        "margin": 0.47
    },
    {
        "id": "TNR001",
        "name": "Rosewater Rescue Hydrating Toner",
        "category": "Toner",
        "description": "Alcohol-free rosewater blend that replenishes moisture and soothes tight, very dry skin.",
        "top_ingredients": "Damask Rose Water; Glycerin; Aloe Vera Juice",
        "tags": ["hydration", "very-dry", "sensitive", "natural"],
        "price": 32,
        "margin": 0.4
    },
    {
        "id": "TNR002",
        "name": "ClearWave 2% BHA Toner",
        "category": "Toner",
        "description": "Oil-controlling liquid exfoliant unclogs pores and keeps breakouts at bay for oily, acne-prone skin.",
        "top_ingredients": "Salicylic Acid 2%; Witch Hazel; Niacinamide",
        "tags": ["oily", "acne-prone", "pore-care", "BHA"],
        "price": 38,
        "margin": 0.45
    },
    # Add more products as needed
]

# Load models and data at startup
@app.on_event("startup")
async def startup_event():
    global products, embedder, knowledge_base, knowledge_index, knowledge_texts
    
    # Use the product data from above
    products = pd.DataFrame(product_data)
    print(f"Loaded {len(products)} products")
    
    # Load sentence transformer model
    try:
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        print("Loaded sentence transformer model")
    except Exception as e:
        print(f"Error loading sentence transformer model: {e}")
        raise
    
    # Load and process knowledge base
    try:
        knowledge_texts = [
            "Glow Beauty was founded in 2018 with a mission to provide natural skincare products.",
            "Our products are cruelty-free and made with sustainable ingredients.",
            "The Vitamin C serum is suitable for sensitive skin and helps brighten complexion.",
            "For best results, apply moisturizer after cleansing while skin is still damp.",
            "Our Hyaluronic Acid serum is best for dry skin types.",
            "The Niacinamide serum works well for oily and acne-prone skin.",
            "Customer review: 'The Vitamin C serum completely transformed my skin in just two weeks!'",
            "Customer review: 'I love the gentle cleanser, it doesn't dry out my sensitive skin.'",
            "FAQ: How often should I use the exfoliating mask? Answer: 1-2 times per week for most skin types.",
            "FAQ: Are your products vegan? Answer: Yes, all our products are 100% vegan and cruelty-free."
        ]
        
        # Create embeddings and index
        knowledge_embeddings = embedder.encode(knowledge_texts)
        dimension = knowledge_embeddings.shape[1]
        knowledge_index = faiss.IndexFlatL2(dimension)
        knowledge_index.add(np.array(knowledge_embeddings).astype('float32'))
        knowledge_base = knowledge_embeddings
        
        print(f"Created knowledge base with {len(knowledge_texts)} entries")
    except Exception as e:
        print(f"Error creating knowledge base: {e}")
        raise

class Query(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None

class ChatQuery(BaseModel):
    query: str
    conversation_history: Optional[List[Dict[str, str]]] = None

@app.post("/api/search")
async def search(query: Query):
    try:
        # Extract category from query if present
        category = None
        for cat in set(products['category']):
            if cat.lower() in query.query.lower() or cat.lower().rstrip('s') in query.query.lower():
                category = cat
                break
        
        # Filter products by category if specified
        filtered_products = products
        if category:
            filtered_products = products[products['category'] == category]
        
        # Apply any additional filters from the request
        if query.filters:
            for key, value in query.filters.items():
                if key in filtered_products.columns:
                    filtered_products = filtered_products[filtered_products[key] == value]
        
        # Sort by margin (highest first)
        sorted_products = filtered_products.sort_values('margin', ascending=False)
        
        # Convert to list of dictionaries
        results = sorted_products.head(6).to_dict('records')
        
        # Add image placeholder and justification
        for product in results:
            product['image'] = f"/placeholder.svg?height=200&width=200"
            product['justification'] = f"This {product['category'].lower().rstrip('s')} is perfect for your needs based on your query."
        
        return {
            "results": results,
            "summary": f"Here are some {category.lower() if category else 'products'} that match your needs."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(query: ChatQuery):
    try:
        user_query = query.query
        
        # Simple rule-based response for demo
        # In a real implementation, this would use the LLM
        
        if any(word in user_query.lower() for word in ['serum', 'moisturizer']):
            return {
                "response": f"Based on your interest in {'serums' if 'serum' in user_query.lower() else 'moisturizers'}, would you prefer products for sensitive, oily, or dry skin?",
                "needsFollowUp": True,
                "products": []
            }
        elif any(word in user_query.lower() for word in ['sensitive', 'gentle']):
            return {
                "response": "I've found some gentle products for sensitive skin. Would you prefer a cleanser, moisturizer, or serum?",
                "needsFollowUp": True,
                "products": []
            }
        elif any(word in user_query.lower() for word in ['is', 'how', 'why', 'what']):
            # This is likely a question - use RAG to answer
            query_embedding = embedder.encode([user_query])
            D, I = knowledge_index.search(np.array(query_embedding).astype('float32'), k=2)
            
            relevant_texts = [knowledge_texts[idx] for idx in I[0]]
            
            return {
                "response": f"{relevant_texts[0]} {relevant_texts[1] if len(relevant_texts) > 1 else ''}",
                "needsFollowUp": False,
                "products": []
            }
        else:
            return {
                "response": "I'd like to help you find the right skincare products. Could you tell me your skin type (dry, oily, combination, sensitive) and what specific concerns you're looking to address?",
                "needsFollowUp": True,
                "products": []
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products")
async def get_products(category: Optional[str] = None):
    try:
        filtered_products = products
        if category:
            filtered_products = products[products['category'] == category]
        
        # Convert to list of dictionaries
        results = filtered_products.to_dict('records')
        
        # Add image placeholder
        for product in results:
            product['image'] = f"/placeholder.svg?height=200&width=200"
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
