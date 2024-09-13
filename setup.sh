#!/bin/bash

uvicorn app:app --reload --port 4242   
stripe listen --forward-to localhost:4242/webhook                                     
ollama pull llama3:8b
ollama serve
streamlit run Dashboard.py                                                  