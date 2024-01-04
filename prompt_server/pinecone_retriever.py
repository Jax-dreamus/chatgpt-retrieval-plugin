import json

import requests


class PineconeRetriever:
    def __init__(self, pinecone_retrieve_api_url, max_results, **kwargs):
        self.max_results = max_results
        self.kwargs = kwargs
        self.pinecone_retrieve_api_url = pinecone_retrieve_api_url

    def _get_pinecone_retrieve(self, query):
        data = requests.post(url=f'{self.pinecone_retrieve_api_url}/query',
                             data=json.dumps(
                                 {"queries": [
                                     {
                                         "query": query,
                                         "top_k": self.max_results
                                     }
                                 ]})).json()
        relevant_docs = [result for result
                         in sorted(data['results'][0]['results'],
                                   key=lambda x: x['score'],
                                   reverse=True)]
        return relevant_docs

    def _pretty_print_docs(self, docs):
        return f"\n".join(f"Source: {d['metadata'].get('source')}\n"
                          f"Title: {d['metadata'].get('document_id')}\n"
                          f"Content: {d['text']}\n"
                          for d in docs)

    def get_context(self, query):
        # TODO: relevant_docs는 pinecone에서 뽑도록 수정
        relevant_docs = self._get_pinecone_retrieve(query)
        return self._pretty_print_docs(relevant_docs)
