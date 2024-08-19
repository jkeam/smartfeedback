from celery import shared_task
from .models import Feedback
from os import getenv
from langchain_openai import OpenAI
from langchain_community.llms import VLLMOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from logging import getLogger

logger = getLogger(__name__)

openapi_key = getenv('OPENAI_API_KEY', None)
vllm_base_url = getenv('VLLM_BASE_URL', None)
vllm_model_name = getenv('VLLM_MODEL_NAME', None)
if openapi_key is not None:
    llm = OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0.01,
        timeout=None,
        max_retries=2,
    )
elif vllm_base_url is not None and vllm_model_name is not None:
    llm = VLLMOpenAI(
        openai_api_key="EMPTY",
        openai_api_base=f"{vllm_base_url}/v1",
        model_name=vllm_model_name,
        max_tokens=512,
        top_p=0.95,
        temperature=0.01,
        presence_penalty=1.03,
        streaming=False,
        verbose=False,
    )
else:
    llm = None

@shared_task
def find_sentiment(pk, body):
    if llm is None:
        return
    template = """Is the predominant sentiment of the user in the following text positive, negative, or neutral?
Respond in one word: Positive, Negative, or Neutral. Text: {text}"""
    template = PromptTemplate(input_variables=['text'], template=template)

    user_input = body.strip()
    response = llm.invoke(template.format(text=user_input)).strip()
    logger.info(f"{user_input}: {response}")

    feedback = Feedback.objects.get(pk=pk)
    feedback.sentiment = response
    feedback.save()
