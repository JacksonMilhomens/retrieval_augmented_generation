# Manual do Usuário para Aplicação de Geração de Respostas com Recuperação de Documentos

## Índice

1. [Introdução](#introdução)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Uso](#uso)
5. [Funcionalidades](#funcionalidades)
6. [Estrutura do Código](#estrutura-do-código)
7. [FAQ](#faq)
8. [Suporte](#suporte)

## Introdução

Bem-vindo ao manual do usuário da aplicação de Geração de Respostas com Recuperação de Documentos. Esta aplicação permite que você carregue documentos PDF e faça perguntas baseadas no conteúdo desses documentos. A aplicação utiliza técnicas avançadas de processamento de linguagem natural para fornecer respostas precisas e contextuais.

## Instalação

Para instalar a aplicação, siga os passos abaixo:

1. Clone o repositório:

```bash
git clone https://github.com/JacksonMilhomens/retrieval_augmented_generation.git
cd retrieval_augmented_generation
```

2. Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Para Linux/MacOS
venv\Scripts\activate  # Para Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente: Crie um arquivo .env na raiz do projeto e adicione suas chaves de API e outras configurações necessárias.

## Configuração

Certifique-se de que você tenha as seguintes variáveis de ambiente configuradas no arquivo .env:
* OPENAI_API_KEY: Chave de API para o OpenAI.

## Uso

Para iniciar a aplicação, execute o seguinte comando:
```bash
streamlit run app.py
```

A aplicação será aberta no seu navegador padrão. Siga os passos abaixo para usar a aplicação:
1. Carregue seus documentos PDF:
    - No painel lateral, clique em "Carregar" e selecione os arquivos PDF que deseja carregar.
3. Faça perguntas:
    - Após carregar e processar os documentos, você pode digitar suas perguntas no campo de entrada de chat.

## Funcionalidades

##### Carregamento de Documentos PDF

- Carregar Múltiplos Arquivos: Você pode carregar múltiplos arquivos PDF de uma vez.
- Processamento de Texto: O texto dos PDFs é extraído e dividido em partes menores para facilitar a recuperação de informações.

##### Geração de Respostas

- Respostas Contextuais: A aplicação utiliza o modelo GPT-3.5-turbo para gerar respostas baseadas no conteúdo dos documentos e no histórico da conversa.
- Histórico de Conversa: O histórico da conversa é mantido para fornecer respostas mais contextuais.

## Estrutura do Código

##### Funções Principais

- get_pdf_text(pdf_docs)
    - Extrai o texto dos documentos PDF carregados.
- get_text_chunks(text)
    - Divide o texto extraído em partes menores.
- get_vectorstore(text_chunks)
    - Cria um vetor de armazenamento para recuperação de informações.
- get_conversation_chain(vectorstore)
    - Cria a cadeia de conversação que utiliza o modelo GPT-3.5-turbo para gerar respostas.
 
##### Interface do Usuário

- Streamlit: A interface do usuário é construída usando o Streamlit, que permite a criação de aplicações web interativas de forma rápida e fácil.

##### Fluxo de Trabalho

1. Carregamento de Documentos: O usuário carrega os documentos PDF.
2. Processamento de Texto: O texto é extraído e dividido em partes menores.
3. Criação de Vetor de Armazenamento: Um vetor de armazenamento é criado para facilitar a recuperação de informações.
4. Geração de Respostas: O usuário faz perguntas e a aplicação gera respostas baseadas no conteúdo dos documentos e no histórico da conversa.

## FAQ

#### Quais tipos de arquivos são suportados?  

Atualmente, a aplicação suporta apenas arquivos PDF.

#### Como posso melhorar a precisão das respostas? 

Certifique-se de carregar documentos PDF de alta qualidade e bem formatados. Além disso, perguntas mais específicas tendem a gerar respostas mais precisas.

#### Posso usar outros modelos de linguagem?  

Sim, a aplicação é modular e permite a integração de outros modelos de linguagem, desde que sejam compatíveis com a API utilizada.

## Suporte
Se você encontrar problemas ou tiver dúvidas, entre em contato com nossa equipe de suporte através do email: jacksonferreira599@gmail.com.

Obrigado por usar nossa aplicação! Esperamos que ela seja útil para suas necessidades de recuperação de informações e geração de respostas.
