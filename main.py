from streamlit import session_state
from gigachat_api import Giga
import streamlit as st
from utils import get_src

st.title(":blue[Чат] бот от Евгения :grin:")

if "token" not in session_state:
    try:
        st.session_state.token = Giga.get_access_token()
        st.toast("Токен успешно получен!")
    except Exception as exc:
        st.toast(f"Нет токена доступа {exc}")

if "messages" not in session_state:
    st.session_state.messages = [{"role": "ai", "content": "Чем могу быть полезен?"}]

for msg in st.session_state.messages:
    if msg.get("is_image"):
        st.chat_message(msg["role"]).image(msg["content"])
    else:
        st.chat_message(msg["role"]).write(msg["content"])

if user_promt := st.chat_input():
    st.chat_message("user").write(user_promt)
    st.session_state.messages.append({"role": "user", "content": user_promt})

    with st.spinner("Думаю..."):
        responce, total_tokens = Giga.send_promt(st.session_state.token, user_promt)
        data, img_id, is_image = get_src(responce)

        if is_image:
            resp = Giga.get_images(st.session_state.token, img_id)
            st.chat_message("ai").image(resp)
            st.chat_message("ai").write(data)
            st.toast(total_tokens)
            st.session_state.messages.append({"role": "user", "content": resp, "is_image": True})
            st.session_state.messages.append({"role": "ai", "content": data})
        else:
            st.chat_message("ai").write(data)
            st.toast(total_tokens)
            st.session_state.messages.append({"role": "ai", "content": data})





