import time

from agents.search_agents.memory import Memory
from prompt_server.functions import stream_output, generate_report, choose_agent
from prompt_server.pinecone_retriever import PineconeRetriever
from prompt_server.utils import timeit


class GPTResearcher:
    def __init__(self, query, report_type, websocket=None):
        """
        Initialize the GPT Researcher class.
        Args:
            query:
            report_type:
            config_path:
            websocket:
        """
        self.query = query
        self.agent = None
        self.role = None
        self.report_type = report_type
        self.websocket = websocket
        self.context = []
        self.memory = Memory()
        self.visited_urls = set()

    async def run(self):
        """
        Runs the GPT Researcher
        Returns:
            Report
        """
        print(f"🔎 Running research for '{self.query}'...")
        # Generate Agent
        self.agent, self.role = await choose_agent(self.query)
        await stream_output("logs", self.agent, self.websocket)

        self.context = await self.get_similar_content_by_query(self.query)

        await stream_output("logs", f"✍️ Writing for research task: {self.query}...",
                            self.websocket)
        report = await generate_report(query=self.query, context=self.context,
                                       agent_role_prompt=self.role,
                                       report_type=self.report_type,
                                       websocket=self.websocket)
        time.sleep(2)
        return report

    @timeit
    async def get_similar_content_by_query(self, query):
        await stream_output("logs", f"📃 드림어스 컴퍼니 블로그에서 관련된 정보 찾는중 : {query}...", self.websocket)
        # Summarize Raw Data
        context_compressor = PineconeRetriever(
            pinecone_retrieve_api_url="http://vector-search-server:8001",
            max_results=10
        )
        # Run Tasks
        return context_compressor.get_context(query)
