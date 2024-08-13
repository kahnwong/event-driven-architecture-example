start-db:
	docker compose -f docker-compose-postgres.yaml up -d

start-backend:
	cd backend && poetry run uvicorn backend.main:app --port 8080 --reload

# start:
# 	streamlit run article_summarizer/frontend.py --server.port 8501
