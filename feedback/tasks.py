from celery import shared_task
from .models import Feedback
from os import getenv, path
from langchain_openai import OpenAI
from langchain_community.llms import VLLMOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from logging import getLogger
from pathlib import Path
from django.conf import settings

logger = getLogger(__name__)

MODEL_API_KEY = getenv('MODEL_API_KEY', None)
MODEL_API_URL = getenv('MODEL_API_URL', None)
MODEL_NAME = getenv('MODEL_NAME', None)
MODEL_FAMILY = getenv('MODEL_FAMILY', None)

# sets llm and template
match(MODEL_FAMILY):
    case 'openai':
        template = Path(path.join(settings.BASE_DIR, 'prompts', 'openai.txt')).read_text(encoding='utf-8')
        llm = OpenAI(
            api_key=MODEL_API_KEY,
            model=MODEL_NAME,
            temperature=0.01,
            timeout=None,
            max_retries=2,
        )
    case 'mistral':
        # https://www.promptingguide.ai/models/mistral-7b
        template = Path(path.join(settings.BASE_DIR, 'prompts', 'mistral.txt')).read_text(encoding='utf-8')
        llm = VLLMOpenAI(
            openai_api_key="EMPTY",
            openai_api_base=f"{MODEL_API_URL}/v1",
            model_name=MODEL_NAME,
            streaming=False,
            verbose=False,
            temperature=0.01,
            max_tokens=900,
            top_p=0.85,
            presence_penalty=1.05,
        )
    case 'granite':
        # https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-models-ibm-lab.html?context=wx&audience=wdp
        template = Path(path.join(settings.BASE_DIR, 'prompts', 'granite.txt')).read_text(encoding='utf-8')
        llm = VLLMOpenAI(
            openai_api_key="EMPTY",
            openai_api_base=f"{MODEL_API_URL}/v1",
            model_name=MODEL_NAME,
            streaming=False,
            verbose=False,
            temperature=0.01,
            max_tokens=512,
            top_p=0.95,
            presence_penalty=1.03,
        )
    case _:
        template = None
        llm = None

def update_feedback(pk, sentiment):
    feedback = Feedback.objects.get(pk=pk)
    feedback.sentiment = sentiment.strip()
    feedback.save()
    return feedback

@shared_task
def find_sentiment(pk, body):
    if llm is None or template is None:
        return
    prompt_template = PromptTemplate(input_variables=['text'], template=template)
    bot_response = llm.invoke(prompt_template.format(text=body.strip())).split('\n')
    if len(bot_response) > 0:
        logger.debug(f"{body.strip()}: {bot_response[0]}")
        update_feedback(pk, bot_response[0])
