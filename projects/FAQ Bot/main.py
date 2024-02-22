import faq
import user


question = user.get_user_input()
reply = faq.faq_bot(question)

print(reply)
