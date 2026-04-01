# Lab 2 Submission README

## Student Information
- Name: Abigail Reyes
- Date: 2026-04-01

## Deliverables Included
- `inference_api/Dockerfile`
- `preprocessor/Dockerfile`
- `inference_api/app.py` (with `/health` and `/stats`)
- `sample_classifications_20.jsonl` (first 20 lines from logs)
- `Reflection.md`

## Docker Build Commands Used

### Inference API
```bash
docker build -t inference-api .
```

### Preprocessor
```bash
docker build -t preprocessor .
```

## Docker Run Commands Used

### Inference API Container
```bash
docker run -d --name inference-api -p 8000:8000 -v C:\Users\aesme\OneDrive\Documents\Code\bus675_s26\labs\LAB02_submission\inference_api\logs:/logs inference-api
```

### Preprocessor Container
```bash
docker run -d --name preprocessor -v C:\Users\aesme\OneDrive\Documents\Code\bus675_s26\labs\LAB02_submission\incoming:/incoming -e API_URL=http://host.docker.internal:8000 preprocessor
```

## Brief Explanation: How the Containers Communicate

The preprocessor container polls the `/incoming` folder every 2 seconds for new image files. When it finds one, it sends a POST request to the inference API's `/predict` endpoint, passing the image and metadata (customer ID, product ID) extracted from the filename. The API URL is configured via the `API_URL` environment variable set at container startup.

Both containers run on the same host machine but are isolated from each other. Using `localhost` inside the preprocessor container would refer to the container itself, not the host — so `host.docker.internal` is used instead, which Docker Desktop resolves to the host machine's IP address.

Images and logs persist on the host through volume mounts: the `incoming/` folder is mounted to `/incoming` in the preprocessor container, and a `logs/` folder is mounted to `/logs` in the inference API container. This means processed images and classification results survive container restarts.

