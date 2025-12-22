# InsightGen Backend

GenAI-based Dashboard Generator Backend API built with FastAPI and Google Gemini AI.

## Features

- 🤖 **Natural Language to SQL**: Convert business questions to SQL queries using Google Gemini
- 📊 **Auto Visualization**: AI determines the best chart type for your data
- 💡 **Smart Insights**: Generate actionable business insights automatically
- 🔒 **Security First**: SQL validation, read-only queries, rate limiting
- ⚡ **Fast & Scalable**: Built with FastAPI and async support

## Tech Stack

- **Framework**: FastAPI
- **AI/LLM**: Google Gemini Pro
- **Database**: PostgreSQL with SQLAlchemy
- **Security**: SQL parser, rate limiting
- **Validation**: Pydantic v2

## Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Google AI Studio API Key

## Installation

### 1. Clone and Navigate

```bash
cd insightgen-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

The `.env` file is already created with your Google AI API key. Update the database URL if needed:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/insightgen
GOOGLE_API_KEY=your_key_here
```

### 5. Set Up PostgreSQL

**Install PostgreSQL** (if not already installed):
- Windows: Download from https://www.postgresql.org/download/windows/
- Use default settings, remember your password

**Create Database:**

```bash
# Open PostgreSQL command line (psql)
psql -U postgres

# Create database
CREATE DATABASE insightgen;

# Exit
\q
```

### 6. Initialize Database

```bash
python init_db.py
```

This will:
- Create all tables (products, customers, orders)
- Populate with 500 sample orders
- Set up realistic sales data for testing

## Running the Server

```bash
# Development mode (with auto-reload)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or simply
python app/main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Generate Dashboard

**POST** `/api/v1/dashboard/generate`

```json
{
  "query": "Show sales trends by category for last quarter"
}
```

**Response:**

```json
{
  "dashboard_id": "uuid",
  "query": "Show sales trends...",
  "sql": "SELECT ...",
  "charts": [
    {
      "id": "chart_1",
      "type": "line",
      "title": "Sales Trends by Category",
      "data": [...],
      "config": {
        "x_axis": "month",
        "y_axis": "revenue",
        "group_by": "category"
      }
    }
  ],
  "insights": [
    "Electronics sales increased 18% MoM",
    "Clothing category showed highest growth"
  ],
  "metadata": {
    "rows_returned": 120,
    "execution_time_ms": 45
  }
}
```

### Health Check

**GET** `/api/v1/health`

```json
{
  "status": "healthy",
  "message": "InsightGen API is running"
}
```

## Example Queries

Try these natural language questions:

- "Show me total sales by category"
- "Top 10 customers by revenue"
- "Monthly sales trends for electronics"
- "Which region has the highest sales?"
- "Show product performance for last month"
- "Compare sales across all categories"

## Project Structure

```
insightgen-backend/
├── app/
│   ├── api/              # API endpoints
│   ├── db/               # Database models & session
│   ├── llm/              # Google Gemini integration
│   ├── security/         # SQL validator & rate limiter
│   ├── services/         # Business logic
│   ├── schemas/          # Pydantic models
│   ├── config.py         # Configuration
│   └── main.py           # FastAPI app
├── init_db.py            # Database setup script
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables
```

## Security Features

- ✅ SQL injection prevention
- ✅ Read-only queries (SELECT only)
- ✅ Dangerous keyword blocking (DROP, DELETE, etc.)
- ✅ Table access validation
- ✅ Row limits (max 10,000)
- ✅ Query timeout (30 seconds)
- ✅ Rate limiting (10 requests/minute)

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black app/

# Lint
flake8 app/
```

## Troubleshooting

### Database Connection Error

- Ensure PostgreSQL is running
- Check DATABASE_URL in `.env`
- Verify database exists: `psql -U postgres -l`

### Google AI API Error

- Verify API key in `.env`
- Check API quota at https://makersuite.google.com/app/apikey
- Ensure you're using Gemini Pro model

### Import Errors

- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

## Next Steps

1. ✅ Backend is ready!
2. 📱 Build the frontend (Next.js)
3. 🔗 Connect frontend to backend
4. 🧪 Test end-to-end
5. 🚀 Deploy

## License

MIT
