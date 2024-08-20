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
        model='gpt-3.5-turbo-instruct',
        temperature=0.01,
        timeout=None,
        max_retries=2,
    )
elif vllm_base_url is not None and vllm_model_name is not None:
    # mistral
    # max_tokens=512,
    # top_p=0.95,
    # presence_penalty=1.03,

    # granite-7b-lab
    # max_tokens=900,
    # top_p=0.85,
    # presence_penalty=1.05,
    llm = VLLMOpenAI(
        openai_api_key="EMPTY",
        openai_api_base=f"{vllm_base_url}/v1",
        model_name=vllm_model_name,
        streaming=False,
        verbose=False,
        temperature=0.01,
        max_tokens=900,
        top_p=0.85,
        presence_penalty=1.05,
    )
else:
    llm = None

def update_feedback(pk, sentiment):
    feedback = Feedback.objects.get(pk=pk)
    feedback.sentiment = sentiment.strip()
    feedback.save()
    return feedback

@shared_task
def find_sentiment(pk, body):
    if llm is None:
        return
    user_input = body.strip()

    # mistral or openai
    # https://www.promptingguide.ai/models/mistral-7b
    # template = """<s>[INST] What is the sentiment of the following text? Respond in one word. [/INST] Positive or Negative</s>[INST] {text} [/INST]"""

    # granite
    # https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-models-ibm-lab.html?context=wx&audience=wdp
    template = """<|system|>
You are an AI language model developed by IBM Research. You are a cautious assistant. You carefully follow instructions. You are helpful and harmless and you follow ethical guidelines and promote positive behavior.
<|user|>
For each feedback, specify whether the content is Positive or Negative. Your response should only include the answer. Do not provide any further explanation.
Here are some examples, complete the last one:
Feedback:
Carol, the service rep was so helpful. She answered all of my questions and explained things beautifully.
Class:
Positive

Feedback:
The service representative did not listen to a word I said. It was a waste of my time.
Class:
Negative

Feedback:
{text}
Class:
<|assistant|>
"""
    template = PromptTemplate(input_variables=['text'], template=template)

    # mistral and openai
    # response = llm.invoke(template.format(text=user_input)).strip()
    # logger.info(f"{user_input}: {response}")
    # update_feedback(pk, response)

    # granite
    response = llm.invoke(template.format(text=user_input))
    bot_response = response.split('\n')
    if len(bot_response) > 0:
        update_feedback(pk, bot_response[0])
