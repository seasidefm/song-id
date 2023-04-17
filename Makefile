.PHONY: serve

serve:
	uvicorn main:app --reload

prod:
	uvicorn --workers 4 main:app