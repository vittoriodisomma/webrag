# Welcome to `Webrag Chatbot`

This repository is the development of the Webrag Chatbot for scrapying a website and extracting information from it.


## Introduction

Webrag is an intelligent chatbot designed to receive the URL of a website as input and return an index of its contents. The collected information (page URLs and related textual content) is stored in the Milvus vector database.                                                                                                                         At the start of each conversation, the chatbot displays a welcome message with available user options, which are described in detail in the following sections: website indexing and information extraction from an indexed site.

### Content Extraction

In the initial version, Webrag analyzes only the homepage corresponding to the provided URL. In future versions, a generative AI model will be used to identify a meaningful set of associated pages within the website.


### Summary Generation

To comply with Milvus’s storage constraints, the content of each page is summarized using a generative AI model. This produces concise yet informative summaries.


### Storage in Milvus

Each page is stored as a dictionary containing its URL and the corresponding summary. At the end of the process, the user receives a confirmation message with the outcome of the operation.


##  Information Extraction

To query a previously indexed website, the user can simply enter a natural language question (not a URL). In response, Webrag performs a semantic search on Milvus and returns:

- The most relevant information related to the query.
- A customizable list of the pages from which the information was extracted, providing transparency and opportunities for deeper exploration.





