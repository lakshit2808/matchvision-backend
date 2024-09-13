MatchVision Backend

# Digital Ocean Droplet Config
- ssh root@143.110.190.53
- Droplet password: MatchVision24@ai

# Ollama Server
- URL: http://143.110.190.53:11434/
- starting ollama on droplet: `sudo systemctl start ollama`
- stopping ollama on droplet: `sudo systemctl stop ollama`
- restart ollama on droplet: `sudo systemctl restart ollama`
- check ollama status on droplet: `sudo systemctl status ollama`
- Enable or Disable the Service at Boot: `sudo systemctl enable ollama`


# Streamlit Dashboard
- URL: http://143.110.190.53:8501/
- To keep the Streamlit app running even after you log out, you can use nohup: `nohup - streamlit run Dashboard.py --server.port 8501 --server.headless true --server.enableCORS false &`
- `ps aux | grep streamlit`
- `kill process_id`

# FastAPI DB Processing
- URL: http://143.110.190.53:8000/
- `nohup uvicorn app:app --host 0.0.0.0 --port 8000 &`
- `ps aux | grep uvicorn`
- `kill process_id`

# stripe
- `nohup stripe listen --forward-to localhost:8000/webhook &`
- `ps aux | grep stripe`
- `kill process_id`