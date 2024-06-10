import time

import streamlit as st
from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from PyPDF2 import PdfReader

load_dotenv()


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore.as_retriever()


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Você é um assistente inteligente que responde perguntas com base no conteúdo de documentos PDF carregados pelo usuário. Use o texto fornecido nos documentos e o histórico da conversa para fornecer respostas precisas e contextuais. 
                Contexto dos documentos: {context}""",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    document_chain = create_stuff_documents_chain(llm, prompt)

    retriever_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            (
                "human",
                "Tendo em conta a conversa acima, criar uma consulta de pesquisa para obter informações relevantes para a conversa.",
            ),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm=llm, retriever=vectorstore, prompt=retriever_prompt
    )

    retriever_chain = create_retrieval_chain(history_aware_retriever, document_chain)

    return retriever_chain


# Streamed response emulator
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("Retrieval Augmented Generation")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversation_chain" not in st.session_state:
    st.session_state.conversation_chain = None
if "document_processed" not in st.session_state:
    st.session_state.document_processed = False

with st.sidebar:
    st.subheader("Seus documentos:")
    pdf_docs = st.file_uploader(
        'Carregue os seus PDFs aqui e clique em "Carregar"',
        accept_multiple_files=True,
        type=["pdf"],
    )

    if pdf_docs:
        if st.button("Carregar"):
            with st.spinner("Processando..."):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation_chain = get_conversation_chain(
                    vectorstore
                )

                st.session_state.document_processed = True

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if st.session_state.document_processed:
    if prompt := st.chat_input("Digite sua pergunta"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append(HumanMessage(content=prompt))

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process assistant response
        response = st.session_state.conversation_chain.invoke(
            {
                "input": prompt,
                "chat_history": st.session_state.chat_history,
            }
        )

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(response["answer"]))

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat_history.append(AIMessage(content=response))

else:
    st.info("Por favor, carregue e processe um documento PDF para habilitar o chat.")
