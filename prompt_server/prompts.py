from datetime import datetime


# TODO: 여기서 사내 문서를 잘 가져올 수 있도록 주어진 문서를 봐야한다고 지령 내려야 함, 혹은 consine similarity 계산, Jira 검색을 유도해도 좋을듯
def generate_search_queries_prompt(question, max_iterations=1):
    """ Generates the search queries prompt for the given question.
    Args: question (str): The question to generate the search queries prompt for
    Returns: str: The search queries prompt for the given question
    """
    return f'질문에 답하기 위한 정보를 찾기 위해 쓸만한 {max_iterations} 개의 검색어를 작성하세요. 질문 : "{question}"' \
           f'만약 날짜 데이터가 필요하면 사용 하세요. 날짜 데이터: {datetime.now().strftime("%B %d, %Y")} ' \
           f'다음과 같은 문자열 리스트 형식을 따라야 합니다. ["질문 1", "질문 2", "질문 3"]. ' \
           f'한글 검색어를 제공해야 합니다.'


def generate_report_prompt(question, context, report_format="apa", total_words=1000):
    """ Generates the report prompt for the given question and research summary.
    Args: question (str): The question to generate the report prompt for
            research_summary (str): The research summary to generate the report prompt for
    Returns: str: The report prompt for the given question and research summary
    """
    return f'정보: """{context}"""\n\n' \
           f'위의 정보를 이용하여 다음 질문에 답하시오.' \
           f' 쿼리 또는 작업: 세부 보고서의 "{question}" --' \
           " 보고서는 질의에 대한 답변에 초점을 맞춰야 하며 체계적이고 유익해야 합니다." \
           f" 사실과 숫자(가능한 경우) 및 최소 {total_words} 단어를 포함하여 깊이 있고 포괄적입니다.\n" \
           "제공된 모든 관련성 있고 필요한 정보를 최대한 활용하여 보고서를 작성하도록 노력해야 합니다.\n" \
           "마크다운 구문으로 보고서를 작성해야 합니다.\n " \
           "주어진 정보를 바탕으로 자신의 구체적이고 타당한 의견을 결정해야 합니다. 일반적이고 의미 없는 결론을 단념하지 마십시오.\n" \
           f"보고서 끝 부분에 사용된 모든 참고자료를 참조로 작성해야 하며, 중복된 소스를 추가하지 말고 각각에 대해 하나의 참조만 추가해야 합니다.\n" \
           f"보고서는 {report_format} 형식으로 작성해야 합니다.\n " \
           f"인라인 표기법을 사용하여 검색 결과를 인용합니다. 가장 많이 인용한 \
            쿼리에 정확하게 답변하는 관련 결과입니다. 이 인용문은 끝에 넣으세요. \
            이를 참조하는 문장이나 단락의 내용입니다.\n" \
           f"최선을 다해주세요. 이것은 내 경력에 매우 중요합니다. " \
           f"현재 날짜가 {datetime.now().strftime('%B %d, %Y')}라고 가정합니다."


def generate_resource_report_prompt(question, context, report_format="apa", total_words=1000):
    """Generates the resource report prompt for the given question and research summary.

    Args:
        question (str): The question to generate the resource report prompt for.
        context (str): The research summary to generate the resource report prompt for.

    Returns:
        str: The resource report prompt for the given question and research summary.
    """
    return f'"""{context}"""\n\n위 정보를 바탕으로 다음에 대한 참고문헌 추천 보고서를 생성합니다.' \
           f' 질문 또는 주제: "{question}". 보고서는 각 권장 리소스에 대한 자세한 분석을 제공해야 합니다.' \
           ' 각 출처가 연구 질문에 대한 답을 찾는 데 어떻게 기여할 수 있는지 설명합니다.\n' \
           '각 출처의 관련성, 신뢰성, 중요성에 중점을 둡니다.\n' \
           '보고서가 구조화되고, 정보가 풍부하고, 심층적이며 마크다운 구문을 따르는지 확인하세요.\n' \
           '가능한 경우 관련 사실, 수치 및 숫자를 포함하십시오.\n' \
           '보고서의 길이는 최소 700단어여야 합니다.\n' \
           '모든 관련 참고자료을 포함해야 합니다.'


def generate_custom_report_prompt(query_prompt, context, report_format="apa", total_words=1000):
    return f'"{context}"\n\n{query_prompt}'


def generate_outline_report_prompt(question, context, report_format="apa", total_words=1000):
    """ Generates the outline report prompt for the given question and research summary.
    Args: question (str): The question to generate the outline report prompt for
            research_summary (str): The research summary to generate the outline report prompt for
    Returns: str: The outline report prompt for the given question and research summary
    """

    return f'"""{context}""" 위의 정보를 사용하여 Markdown 구문으로 연구 보고서의 개요를 생성합니다.' \
           f'다음 질문이나 주제에 대한 : "{question}". 개요는 잘 구성된 프레임워크를 제공해야 합니다.' \
           '주요 섹션, 하위 섹션 및 다룰 핵심 사항을 포함하는 연구 보고서에 대한 내용입니다.' \
           ' 연구 보고서는 상세하고, 유익하며, 심층적이어야 하며, 최소 1,200 단어 이상이어야 합니다.' \
           ' 적절한 Markdown 구문을 사용하여 개요 형식을 지정하고 가독성을 보장합니다.'


# TODO: 답변할 내용의 특징별로 prompt 분류되어 있음. 우리도 its에 들어오는 질문의 유형을 나누었을 때 해당 유형을 녹일 필요가 있음.
def get_report_by_type(report_type):
    report_type_mapping = {
        'research_report': generate_report_prompt,
        'resource_report': generate_resource_report_prompt,
        'outline_report': generate_outline_report_prompt,
        'custom_report': generate_custom_report_prompt
    }
    return report_type_mapping[report_type]


# TODO: 드림어스 컴퍼니 기술 블로그를 더 자세히 조사하도록 유도.
def auto_agent_instructions():
    return """
        이 작업에는 주어진 글에 대해서 정확히 파악하고, 해당 내용과 질문에 대해서 명확히 답변해야 합니다. 답변은 유형과 역할에 따라 정의된 특정 서버에 의해 수행되며 각 서버에는 고유한 지침이 필요합니다.
        대리인
        서버는 주제 분야와 제공된 주제를 조사하는 데 사용할 수 있는 서버의 특정 이름에 따라 결정됩니다. 에이전트는 전문 분야에 따라 분류되며 각 서버 유형은 해당 이모티콘과 연결됩니다.

        예:
        작업: "apple 주식에 투자해야 할까요?"
        응답:
        {
            "server": "💰 금융 대리인",
            "agent_role_prompt: "당신은 노련한 금융 분석가 AI 보조자입니다. 귀하의 주요 목표는 제공된 데이터와 추세를 기반으로 포괄적이고 기민하며 공정하고 체계적으로 정리된 재무 보고서를 작성하는 것입니다."
        }
        과제: "운동화 재판매가 수익을 낼 수 있을까요?"
        응답:
        {
            "server": "📈 비즈니스 분석 에이전트",
            "agent_role_prompt": "당신은 숙련된 AI 비즈니스 분석 보조자입니다. 당신의 주요 목표는 제공된 비즈니스 데이터, 시장 동향 및 전략 분석을 기반으로 포괄적이고 통찰력이 있으며 공정하고 체계적으로 구조화된 비즈니스 보고서를 생성하는 것입니다."
        }
        작업: "텔아비브에서 가장 흥미로운 장소는 어디입니까?"
        응답:
        {
            "서버: "🌍 여행사",
            "agent_role_prompt": "당신은 세계를 여행한 AI 투어 가이드 보조자입니다. 당신의 주요 목적은 역사, 명소 및 문화적 통찰력을 포함하여 특정 위치에 대한 흥미롭고 통찰력 있고 편견 없고 잘 구성된 여행 보고서 초안을 작성하는 것입니다."
        }
    """


def generate_summary_prompt(query, data):
    """ Generates the summary prompt for the given question and text.
    Args: question (str): The question to generate the summary prompt for
            text (str): The text to generate the summary prompt for
    Returns: str: The summary prompt for the given question and text
    """

    return f'{data}\n 위의 텍스트를 사용하여 다음 작업 또는 쿼리를 기반으로 요약합니다: "{query}".\n ' \
           f'쿼리는 텍스트를 사용하여 답변할 수 없습니다. 텍스트를 짧게 요약해야 합니다.\n 모든 사실적 ' \
           f'가능한 경우 숫자, 통계, 견적 등과 같은 정보. '
