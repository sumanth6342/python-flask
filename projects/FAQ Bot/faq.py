import knowledge_bank


def faq_bot_legacy(question):
    knowledge_bank_local = {
        "Who is the PM of India?": "Narendra Modi",
        "When did India get its independence?": "1947",
        "What is the currency of India?": "Rupee"
    }

    knowledge_bank_updated = {}

    for _question, _answer in knowledge_bank_local.items():
        knowledge_bank_updated[_question.lower()] = _answer

    question_updated = question.lower()

    if question_updated in knowledge_bank_updated:
        answer = knowledge_bank_updated[question_updated]
        user_reply = f"The answer is : {answer}"
    else:
        user_reply = "knowledge bank does not have this answer"

    return user_reply


def faq_bot(question):
    knowledge_bank_updated = {}

    for _question, _answer in knowledge_bank.KNOWLEDGE_BANK.items():
        knowledge_bank_updated[_question.lower()] = _answer

    question_updated = question.lower()

    if question_updated in knowledge_bank_updated:
        answer = knowledge_bank_updated[question_updated]
        user_reply = f"The answer is : {answer}"
    else:
        user_reply = "knowledge bank does not have this answer at this moment"

    return user_reply


def customized_print(variable):
    return f"The output is : {variable}"
