from transformers import DPRQuestionEncoder, DPRContextEncoder, DPRQuestionEncoderTokenizer, DPRContextEncoderTokenizer,pipeline
import logging

logging.basicConfig(level=logging.ERROR)

question_encoder = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
context_encoder = DPRContextEncoder.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")

question_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
context_tokenizer = DPRContextEncoderTokenizer.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")

qa_pipeline = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')

def encode_query(query):
    return question_encoder(**question_tokenizer(query, return_tensors='pt'))['pooler_output']

def encode_context(context):
    return context_encoder(**context_tokenizer(context, return_tensors='pt'))['pooler_output']

def answer_query(query, contexts):
    answers = []
    for context in contexts:
        result = qa_pipeline(question=query, context=context)
        answers.append(result['answer'])
    return answers
