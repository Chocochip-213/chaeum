import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import torch
import logging
import time

# Configure logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Global variables
model = None
queue = asyncio.Queue()
BATCH_SIZE = 32
BATCH_TIMEOUT = 0.05  # 50ms latency budget for batching


class EmbeddingRequest(BaseModel):
    text: str


@app.on_event("startup")
async def startup_event():
    # Start model loading in background
    asyncio.create_task(load_model())
    # Start batch processor
    asyncio.create_task(process_batches())


async def load_model():
    global model
    logger.info("Loading model jhgan/ko-sroberta-multitask...")
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info(f"Using device: {device}")
    try:
        # Run model loading in a thread
        model = await asyncio.to_thread(SentenceTransformer, 'jhgan/ko-sroberta-multitask', device = device)
        logger.info("Model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        # We don't raise here to keep the server running for healthchecks
        # The /embed endpoint will fail until model is loaded or if loading failed


async def process_batches():
    logger.info("Batch processor started.")
    while True:
        batch = []
        try:
            # Wait for the first item
            item = await queue.get()
            batch.append(item)

            # Try to fill the batch within the timeout
            start_time = time.time()
            while len(batch) < BATCH_SIZE:
                remaining_time = BATCH_TIMEOUT - (time.time() - start_time)
                if remaining_time <= 0:
                    break

                try:
                    # Wait for next item with timeout
                    item = await asyncio.wait_for(queue.get(), timeout = remaining_time)
                    batch.append(item)
                except asyncio.TimeoutError:
                    break

            # Process the batch
            if batch:
                texts = [item[0] for item in batch]
                futures = [item[1] for item in batch]

                try:
                    # Run inference in thread pool
                    # logger.info(f"Processing batch of size {len(batch)}")
                    embeddings = await asyncio.to_thread(model.encode, texts)
                    embeddings_list = embeddings.tolist()

                    for i, future in enumerate(futures):
                        if not future.done():
                            future.set_result(embeddings_list[i])
                except Exception as e:
                    logger.error(f"Batch processing error: {e}")
                    for future in futures:
                        if not future.done():
                            future.set_exception(e)

        except Exception as e:
            logger.error(f"Error in batch processor loop: {e}")
            await asyncio.sleep(1)


@app.post("/embed")
async def embed(request: EmbeddingRequest):
    if model is None:
        raise HTTPException(status_code = 503, detail = "Model not loaded")

    loop = asyncio.get_running_loop()
    future = loop.create_future()

    await queue.put((request.text, future))

    try:
        result = await future
        return {"vector": result}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))


@app.get("/health")
async def health():
    if model is None:
        return {"status": "loading"}
    return {"status": "healthy"}
