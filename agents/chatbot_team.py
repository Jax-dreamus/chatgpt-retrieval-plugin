from permchain import Channel

class ChatbotTeam:
    def __init__(self, research_actor, related_colleague_find_actor):
        self.research_actor_instance = research_actor
        self.related_colleague_find_actor_instance = related_colleague_find_actor

    def run(self, query):
        research_chain = (
            Channel.subscribe_to('input')
            | {"draft": lambda x: self.research_actor_instance.run(x["question"])}
            | Channel.write_to('related_colleague_find_actor_inbox')
        )