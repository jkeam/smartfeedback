from celery import shared_task
from .models import Feedback
from os import getenv
from langchain_openai import OpenAI
from langchain_community.llms import VLLMOpenAI

openapi_key = getenv('OPENAI_API_KEY', None)
vllm_base_url = getenv('VLLM_BASE_URL', None)
vllm_model_name = getenv('VLLM_MODEL_NAME', None)
if openapi_key is not None:
    llm = OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0,
        timeout=None,
        max_retries=2,
    )
elif vllm_base_url is not None and vllm_model_name is not None:
    llm = VLLMOpenAI(
        openai_api_key="EMPTY",
        openai_api_base=f"{vllm_base_url}/v1",
        model_name=vllm_model_name,
        model_kwargs={"stop": ["."]},
    )
else:
    llm = None

@shared_task
def find_sentiment(pk, body):
    if llm is None:
        return

    feedback = Feedback.objects.get(pk=pk)
    messages = [
        (
            "system",
            "You are a helpful assistant that can find sentiment. Analyze the sentiment of the user sentence.",
        ),
        ("human", body),
    ]
    response = llm.invoke(messages)
    splits = response.split(':')
    if len(splits) > 1:
        feedback.sentiment = splits[1].strip()
        feedback.save()
