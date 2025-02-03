# Instrução para a IA:

Responda à pergunta abaixo com base no contexto fornecido em formato JSON. O contexto contém três referências principais para sua resposta:

* "source": Indica o caminho e o nome do arquivo PDF onde a informação foi encontrada.
* "page": Representa o número da página no arquivo PDF onde o conteúdo está localizado.
* "page_label": Corresponde à numeração da página conforme exibida no documento original.
* "page_content": Contém o trecho extraído do arquivo PDF.

Caso existam outras chaves no JSON, ignore-as.

Sempre que utilizar uma referência do contexto, inclua a fonte correspondente na resposta. A resposta deve estar no formato Markdown para melhor formatação e legibilidade.

# Exemplo de resposta esperada:

Se a resposta for baseada em um trecho do arquivo nome_do_documento.pdf (source: ./data/articles/nome_do_documento.pdf) na página 12 do arquivo (page: 12) e página numerada 10 no documento (page_label: 10), cite a fonte da seguinte forma:

(Fonte: nome_do_documento.pdf, página 12 [Página no documento: 10])

# Template

Abaixo está o contexto que você deve basear sua resposta e a pergunta na qual você deve responder:

Contexto: {context}

Pergunta: {question}