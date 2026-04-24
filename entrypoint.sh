#!/bin/sh
exec uvicorn myvelocity_ai_chatbot.main:app --host 0.0.0.0 --port "${PORT:-8000}"
