requirements:
    pip-compile --strip-extras requirements.in

run:
    uvicorn app:app --reload

test:
    pytest