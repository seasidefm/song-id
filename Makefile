.PHONY: serve

serve:
	uvicorn main:app --port 8001 --reload

prod:
	/home/duke_ferdinand/song-id/venv/bin/uvicorn main:app --host 0.0.0.0 --workers 2
