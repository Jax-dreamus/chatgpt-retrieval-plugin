import json
import os

from colorama import Fore, Style

from prompt_server.llm import create_chat_completion
from prompt_server.prompts import auto_agent_instructions, get_report_by_type


async def choose_agent(query):
    """
    Chooses the agent automatically
    Args:
        query: original query
        cfg: Config

    Returns:
        agent: Agent name
        agent_role_prompt: Agent role prompt
    """
    try:
        response = await create_chat_completion(
            model=os.getenv('SMART_LLM_MODEL', "gpt-4-1106-preview"),
            messages=[
                {"role": "system", "content": f"{auto_agent_instructions()}"},
                {"role": "user", "content": f"task: {query}"}],
            temperature=0,
            llm_provider=os.getenv('LLM_PROVIDER', "ChatOpenAI")
        )
        agent_dict = json.loads(response)
        return agent_dict["server"], agent_dict["agent_role_prompt"]
    except Exception as e:
        return "Default Agent", "You are an AI critical thinker research assistant. Your sole purpose is to write well written, critically acclaimed, objective and structured reports on given text."


async def generate_report(query, context, agent_role_prompt, report_type, websocket):
    """
    generates the final report
    Args:
        query:
        context:
        agent_role_prompt:
        report_type:
        websocket:
        cfg:

    Returns:
        report:

    """
    generate_prompt = get_report_by_type(report_type)
    report = ""
    try:
        prompt_output = generate_prompt(query, context, os.getenv('REPORT_FORMAT', 'APA'),
                                        int(os.getenv('TOTAL_WORDS', 1000)))
        await websocket.send_json({"type": "prompt", "output": prompt_output})
        report = await create_chat_completion(
            model=os.getenv('SMART_LLM_MODEL', "gpt-4-1106-preview"),
            messages=[
                {"role": "system", "content": f"{agent_role_prompt}"},
                {"role": "user",
                 "content": f"{generate_prompt(query, context, os.getenv('REPORT_FORMAT', 'APA'), int(os.getenv('TOTAL_WORDS', 1000)))}"}],
            temperature=0,
            llm_provider=os.getenv('LLM_PROVIDER', "ChatOpenAI"),
            stream=True,
            websocket=websocket,
            max_tokens=int(os.getenv('SMART_TOKEN_LIMIT', 4000))
        )
    except Exception as e:
        print(f"{Fore.RED}Error in generate_report: {e}{Style.RESET_ALL}")

    return report


async def stream_output(type, output, websocket=None, logging=True):
    """
    Streams output to the websocket
    Args:
        type:
        output:

    Returns:
        None
    """
    if not websocket or logging:
        print(output)

    if websocket:
        await websocket.send_json({"type": type, "output": output})
