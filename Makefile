.PHONY: serve

serve:
	uvicorn main:app --port 8001 --reload

prod:
	uvicorn --workers 4 main:app
