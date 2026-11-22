# E-Commerce WhatsApp AI Agent

An autonomous WhatsApp AI shopping assistant powered by Google Gemini, FastAPI, and [Neonize](https://github.com/krypton-byte/neonize). Customers can message the bot on WhatsApp to browse categories, search products, manage their cart, checkout, and track or cancel orders.

## Demo

https://github.com/user-attachments/assets/621b79eb-512d-4b18-803a-f17303306072

## Project Structure

- `backend/` — FastAPI e-commerce REST API backed by SQLite (categories, products, cart, and orders)
- `Agent/` — Gemini chat agent, system prompt, configuration, and e-commerce tool definitions
- `whatsapp/` — Neonize WhatsApp client and per-user chat history persistence
- `main.py` — Entry point to start and connect the WhatsApp client

## Prerequisites

- Python 3.13+
- A [Google Gemini API key](https://aistudio.google.com/)
- A WhatsApp account to link via QR code

## Setup

1. **Install dependencies**

   Using `uv`:
   ```bash
   uv sync
   ```

   Or using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**

   Copy `.env.example` to `.env` and fill in your values:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL=gemini-2.5-flash
   BACKEND_URL=http://127.0.0.1:8000
   ```

## How to Run

### 1. Start the Backend First (from the `backend` directory)

Open a terminal, navigate into the `backend` folder, and start the FastAPI server:

```bash
cd backend
uvicorn main:app --reload
```

> **Note:** Make sure to run `uvicorn` from inside the `backend/` directory so the local imports resolve properly. The API will be available at `http://127.0.0.1:8000` (interactive docs at `http://127.0.0.1:8000/docs`).

*(Optional)* If you want to populate the database with sample categories and products, run from inside `backend/`:
```bash
python seed_data.py
```

### 2. Run and Connect WhatsApp (from the root `main.py`)

With the backend running, open a **second terminal** in the project root directory and run:

```bash
python main.py
```

*(Or `uv run main.py` if using `uv`.)*

On first launch, a QR code will appear in the terminal. Open WhatsApp on your phone, go to **Linked Devices → Link a Device**, and scan the QR code. Once connected, you will see `Connected` in the terminal and the agent will reply to incoming direct messages.
