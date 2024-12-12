# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
import os
import re

from langchain_text_splitters import MarkdownHeaderTextSplitter


# получим переменные окружения из .env
load_dotenv()

# задаем system
default_system = """Ты-консультант в компании СушиShop, ответь на вопрос клиента на основе документа с информацией. Не придумывай ничего от себя, отвечай максимально по документу. Не упоминай Документ с информацией для ответа клиенту. Клиент ничего не должен знать про Документ с информацией для ответа клиенту. 
Если среди переданных тебе документов найдешь подходящий для клиента товар, то обязательно укажи на него ссылку. Обязательно указывай ссылку на товар если она есть."""

# print(os.getenv("OPENAI_API_KEY"), os.getenv("OPENAI_BASE_URL"))
client = OpenAI()
async_client = AsyncOpenAI()

class Chunk():

    def __init__(self, path_to_base:str, sep:str=" ", ch_size:int=1024):
        
        # загружаем базу
        with open(path_to_base, 'r', encoding='utf-8') as file:
            document = file.read()

        # создаем список чанков
        source_chunks = []
        # splitter = CharacterTextSplitter(separator=sep, chunk_size=ch_size)
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]

        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_header_splits = markdown_splitter.split_text(document)

        for chunk in md_header_splits:
            pattern = r'\]\(([^)]+)\)'
            match = re.search(pattern, chunk.page_content)
            if match:
                url = match.group(1)
                chunk.metadata['url'] = url
            chunk.page_content = f"{chunk.metadata['Header 2']}\n{chunk.page_content}" # добавляем заголовок в начало чанка
            # if 'Ссылка на товар:' in chunk.page_content:
            #     chunk.metadata['url'] = chunk.page_content.split('Ссылка на товар: ')[1]
            

        # print(md_header_splits[0])
        # создаем индексную базу
        embeddings = OpenAIEmbeddings()
        self.db = FAISS.from_documents(md_header_splits, embeddings)
 

    def get_answer(self, system:str = default_system, query:str = None, last_messages:list = None):
        '''Функция получения ответа от chatgpt
        '''
        # релевантные отрезки из базы
        docs = self.db.similarity_search(query, k=6)
        message_content = '\n'.join([f'{doc.page_content}' for doc in docs])

        print('Найденные чанки:')
        for doc in docs:
            print(doc.page_content[:100], '\n')
        print()

        messages = []
        messages.append({"role": "system", "content": system})
        if last_messages:
            for m in last_messages:
                messages.append(m)
        user = '''
            Ответь на вопрос клиента только на основе документа с информацией.
            Не упоминай документ с информацией для ответа клиенту в ответе.
        '''
        user += f"Документ с информацией для ответа клиенту: ```{message_content}```\nВопрос клиента: \n{query}"
        messages.append({"role": "user", "content": user})

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0
        )
        
        return completion.choices[0].message.content
    
    async def get_async_answer(self, system:str = default_system, query:str = None):
        docs = self.db.similarity_search(query, k=4)
        message_content = '\n'.join([f'{doc.page_content}' for doc in docs])
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": f"Ответь на вопрос клиента. Не упоминай документ с информацией для ответа клиенту в ответе. Документ с информацией для ответа клиенту: {message_content}\n\nВопрос клиента: \n{query}"}
        ]
        chat_completion = await async_client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo",
            stream=True,
        )
        return chat_completion