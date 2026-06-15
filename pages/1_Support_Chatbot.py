import streamlit as st
from openai import OpenAI
from data import products

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="MiniStore Support",
    page_icon="💬",
    layout="wide"
)

st.title("💬 MiniStore Customer Support")
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()
st.write(
    "Ask questions about products, orders, refunds, "
    "returns, payments, or delivery."
)

# -----------------------------------------------------
# OPENAI CLIENT
# -----------------------------------------------------

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# -----------------------------------------------------
# PRODUCT CATALOG FOR PROMPT
# -----------------------------------------------------

catalog_text = ""

for product in products:
    catalog_text += f"""
Product: {product['name']}
Category: {product['category']}
Price: ${product['price']}
Description: {product['description']}
"""

# -----------------------------------------------------
# SYSTEM PROMPT
# -----------------------------------------------------

SYSTEM_PROMPT = f"""
You are MiniStore's professional customer support assistant.

Your job is to help customers with:

- Product information
- Orders
- Delivery
- Shipping
- Refunds
- Returns
- Payment methods
- Store policies

Store Catalog:

{catalog_text}

Rules:

1. Answer ONLY MiniStore related questions.

2. If asked unrelated questions such as:
   - coding
   - politics
   - sports
   - history
   - science
   - mathematics
   politely redirect the user back to MiniStore support topics.

3. Use a friendly and professional customer service tone.

4. If the user asks about products,
   use the catalog information provided.

5. Never invent products that are not in the catalog.

6. If order information is unavailable,
   explain that this is a demo store.
"""

# -----------------------------------------------------
# CHAT HISTORY
# -----------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------------------------------
# CHAT INPUT
# -----------------------------------------------------

prompt = st.chat_input(
    "How can I help you today?"
)

if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(st.session_state.messages)

    # OpenAI Response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3
    )

    assistant_reply = response.choices[0].message.content

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)