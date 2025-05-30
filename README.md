# Conversational Store Mini POC

A proof-of-concept for a conversational e-commerce experience with a personal shopper assistant powered by RAG (Retrieval Augmented Generation).

## Features

- Product catalog with 30+ SKUs across multiple categories
- Conversational search interface that asks clarifying questions
- Product recommendations ranked by margin
- FAQ answering system using RAG
- Responsive UI built with Next.js and TypeScript

## Tech Stack

- **Frontend**: Next.js with TypeScript, React, and Tailwind CSS
- **Backend**: Python FastAPI
- **Vector Search**: FAISS
- **Embeddings**: Sentence Transformers
- **Data Processing**: Pandas

## Project Structure

\`\`\`
conversational-store/
├── app/                  # Next.js app directory
│   ├── api/              # API routes
│   └── page.tsx          # Main page
├── components/           # React components
├── backend/              # Python backend
│   ├── app.py            # FastAPI application
│   └── requirements.txt  # Python dependencies
├── data/                 # Data files
│   ├── skincare_catalogue.xlsx  # Product data
│   └── additional_info.docx     # Knowledge base content
└── README.md             # Project documentation
\`\`\`

## Setup Instructions

### Frontend (Next.js)

1. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

2. Run the development server:
   \`\`\`bash
   npm run dev
   \`\`\`

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Backend (Python FastAPI)

1. Navigate to the backend directory:
   \`\`\`bash
   cd backend
   \`\`\`

2. Create a virtual environment:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

3. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Run the server:
   \`\`\`bash
   uvicorn app:app --reload
   \`\`\`

5. The API will be available at [http://localhost:8000](http://localhost:8000).

## Environment Variables

Create a `.env.local` file in the root directory with the following variables:

\`\`\`
NEXT_PUBLIC_API_URL=http://localhost:8000
\`\`\`

## Next Steps

- Integrate with a real LLM provider (OpenAI, Gemini, etc.)
- Implement user authentication and session management
- Add a shopping cart and checkout functionality
- Enhance the RAG pipeline with better chunking and retrieval strategies
- Implement product filtering and sorting options
- Add analytics to track user interactions and improve recommendations
