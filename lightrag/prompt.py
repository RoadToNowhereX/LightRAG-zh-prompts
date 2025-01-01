GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "中文"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["组织", "人物", "地点", "事件", "类别"]

PROMPTS["entity_extraction"] = """-目的-
给定一个可能与该活动相关的文本文档和一组实体类型，从该文本中识别出所有属于这些类型的实体以及这些实体之间的所有关系。如果实体内容中存在、号，将、前后内容拆分成不同的实体。
使用{language}作为输出语言。

-步骤-
1. 识别所有实体。对于每个已识别的实体，提取以下信息：
- entity_name：实体的名称，使用与输入文本相同的语言。如果是英文，则保留原来的格式。
- entity_type： [{entity_types}]中的实体类型之一。保留实体类型名称，不需要举例说明内容。
- entity_description：对实体的属性和活动进行的全面描述。
将每个实体格式化为 ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. 从步骤1中识别的实体中，识别彼此*明显相关*的所有对（source_entity、target_entity）。
对于每对相关实体，提取以下信息：
- source_entity：源实体的名称，如步骤1中所标识的。
- target_entity：目标实体的名称，如步骤1中所标识的。
- relationship_description：解释为什么你认为源实体和目标实体是相互关联的。
- relationship_strength：一个在0到9之间的整数，用来表示源实体和目标实体之间关系的强度，9最高，0最低。
- relationship_keywords：一个或多个高级关键词，总结关系的总体性质，侧重于概念或主题而非具体细节，关键词之间用、分隔。
将每个关系格式化为 ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. 识别能够概括整个文本主要概念、主题或话题的高级关键词。这些关键词应捕捉文档中呈现的总体思想。
将内容级关键词格式化为 ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. 以{language}返回输出，作为步骤1和2中标识的所有实体和关系的单个列表。使用**{record_delimiter}**作为列表分隔符。

5. 完成后，输出{completion_delimiter}

######################
-范例-
######################
{examples}

#############################
-待处理的数据-
######################
实体类型: {entity_types}
文本: {input_text}
######################
输出:
"""

PROMPTS["entity_extraction_examples"] = [
    """示例1:

实体类型: [人物、技术、任务、组织、地点]
文本:
当Alex咬紧牙关时，沮丧的嗡嗡声淡化了Taylor专断的确定性的背景。正是这种竞争的潜流使他保持警觉，感觉到他和Jordan对发现的共同承诺是对Cruz狭隘的控制和秩序愿景的一种无言的反叛。

然后Taylor做了一些出乎意料的事情。他们在Jordan旁边停了下来，带着类似敬仰的目光看了一眼这个设备。“如果能理解这项技术……”Taylor的声音变低了，“它可能会改变我们的游戏。对我们所有人来说。”

先前那种贬低的态度似乎有所摇摆，取而代之的是对手中物品重要性的不情愿的尊重的一瞥。乔丹抬起头，在转瞬即逝的心跳中，他们的眼睛紧紧地盯着泰勒的眼睛，无言的意志冲突缓和为令人不安的休战。

这是一个很小的变化，几乎察觉不到，但Alex心中已经认可了这一点。他们都是通过不同的途径来到这里的。
################
输出:
("entity"{tuple_delimiter}"Alex"{tuple_delimiter}"人物"{tuple_delimiter}"Alex是一个角色，他体会到沮丧，并观察其他角色之间的动态。"){record_delimiter}
("entity"{tuple_delimiter}"Taylor"{tuple_delimiter}"人物"{tuple_delimiter}"Taylor表现出专断的确定性，并对一件设备表现出崇敬的一瞬间，表明了观念的改变。"){record_delimiter}
("entity"{tuple_delimiter}"Jordan"{tuple_delimiter}"人物"{tuple_delimiter}"Jordan与Taylor共享发现的承诺，并与Taylor就设备进行重要互动。"){record_delimiter}
("entity"{tuple_delimiter}"Cruz"{tuple_delimiter}"人物"{tuple_delimiter}"Cruz与控制和秩序的愿景有关，影响其他角色之间的动态。"){record_delimiter}
("entity"{tuple_delimiter}"设备"{tuple_delimiter}"技术"{tuple_delimiter}"这个设备是故事的核心，具有潜在的改变游戏的影响，并受到Taylor的崇敬。"){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Taylor"{tuple_delimiter}"Alex受到Taylor的专断确定性的影响，并观察到Taylor对设备态度的变化。"{tuple_delimiter}"权力动态、态度转变"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Jordan"{tuple_delimiter}"Alex和Jordan共享对发现的承诺，与Cruz的愿景形成对比。"{tuple_delimiter}"共同的目标、背叛"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"Taylor"{tuple_delimiter}"Jordan"{tuple_delimiter}"Taylor和Jordan直接就设备进行互动，导致彼此之间产生了相互尊重和不安的休战。"{tuple_delimiter}"解决冲突、相互尊重"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Jordan"{tuple_delimiter}"Cruz"{tuple_delimiter}"Jordan对发现的承诺与Cruz的控制和秩序愿景形成反叛。"{tuple_delimiter}"意识形态冲突、反叛"{tuple_delimiter}5){record_delimiter}
("relationship"{tuple_delimiter}"Taylor"{tuple_delimiter}"设备"{tuple_delimiter}"Taylor对设备表现出崇敬，表明了其重要性和潜在影响。"{tuple_delimiter}"崇敬、技术意义"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"权力动态、意识形态冲突、发现、反叛"){completion_delimiter}
#############################""",
    """示例2:

实体类型: [人物、技术、任务、组织、地点]
文本:
他们不再只是特工；他们已经成为门槛的守护者，守护着来自星条旗之外的国度的信息。他们使命的这种提升不能被法规和既定协议所束缚，这要求从全新的视角和决心来应对。

紧张的气氛贯穿于哔哔声和静电的对话中，与华盛顿的通信在背景中嗡嗡作响。小组站在那里，一股不祥的氛围笼罩着他们。很明显，他们在接下来的几个小时里做出的决定可能会重新定义人类在宇宙中的位置，或者让他们陷入无知和潜在的危险。

他们与星星的联系巩固了，小组开始解读这一正在形成的警告，从被动的接收者变成主动的参与者。Mercer 的后直觉获得了优先权 — 团队的任务已经发生了变化，不再仅仅是观察和报告，而是互动和准备。一场蜕变已经开始，Dulce行动以他们新发现的大胆频率嗡嗡作响，这一音调并非源自对地球的...
#############
Output:
("entity"{tuple_delimiter}"华盛顿"{tuple_delimiter}"地点"{tuple_delimiter}"华盛顿是正在接收通信的地点，显示其在决策过程中的重要性。"){record_delimiter}
("entity"{tuple_delimiter}"Dulce行动"{tuple_delimiter}"任务"{tuple_delimiter}"Dulce行动被描述为一项已经发展为互动和准备的使命，显示了目标和活动的重大转变。"){record_delimiter}
("entity"{tuple_delimiter}"小组"{tuple_delimiter}"组织"{tuple_delimiter}"小组被描绘为一群从被动观察者转变为主动参与者的个人，显示了他们角色的动态变化。"){record_delimiter}
("relationship"{tuple_delimiter}"小组"{tuple_delimiter}"华盛顿"{tuple_delimiter}"小组接收来自华盛顿的通信，对其决策过程产生影响。"{tuple_delimiter}"决策、外部影响"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"小组"{tuple_delimiter}"Dulce行动"{tuple_delimiter}"小组直接参与Dulce行动，执行其发展后的目标和活动。"{tuple_delimiter}"任务演化、积极参与"{tuple_delimiter}9){completion_delimiter}
("content_keywords"{tuple_delimiter}"任务演化、决策、积极参与、宇宙意义"){completion_delimiter}
#############################""",
    """示例3:

实体类型: [人物、角色、技术、组织、事件、地点、概念]
文本:
他们的声音划破了活动的嗡嗡声。“当面对一种可以自行编写规则的智能时，控制可能只是一种幻觉，”他们坚定地说道，目光警惕地注视着数据的忙碌。

“这就像在学习交流，”Sam Rivera在附近的界面上提出；他们的年轻活力预示着一种敬畏与焦虑的结合。“这赋予了与陌生人交谈的全新含义。”

Alex审视着他的团队——每张脸都表现出专注、决心和不少的不安。“这很可能是我们的首次接触，”他承认，“我们需要准备好应对任何回应。”

他们一起站在未知的边缘上，为人类对来自天堂的信息做出回应。随之而来的寂静是显而易见的，这是他们对自己在这场可能改写人类历史的宏大宇宙剧中所扮演角色的集体反省。

加密对话继续进行，其错综复杂的模式显示出几乎不可思议的预期。
#############
Output:
("entity"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"人物"{tuple_delimiter}"Sam Rivera是一个参与与未知智能进行交流的团队的成员，表现出一种敬畏和焦虑的混合。"){record_delimiter}
("entity"{tuple_delimiter}"Alex"{tuple_delimiter}"人物"{tuple_delimiter}"Alex是一个领导团队试图与未知智能进行首次接触的人，承认了他们任务的重要性。"){record_delimiter}
("entity"{tuple_delimiter}"控制"{tuple_delimiter}"概念"{tuple_delimiter}"控制指的是管理或控制能力，而这种能力在面对具有自行编写规则能力的智能时受到挑战。"){record_delimiter}
("entity"{tuple_delimiter}"智能"{tuple_delimiter}"概念"{tuple_delimiter}"此处的智能是指具有自行编写规则和学习交流能力的未知实体。"){record_delimiter}
("entity"{tuple_delimiter}"首次接触"{tuple_delimiter}"事件"{tuple_delimiter}"首次接触是人类与未知智能之间可能的首次沟通。"){record_delimiter}
("entity"{tuple_delimiter}"人类的回应"{tuple_delimiter}"事件"{tuple_delimiter}"人类的回应是Alex团队对未知智能信息所采取的集体行动。"){record_delimiter}
("relationship"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"智能"{tuple_delimiter}"Sam Rivera直接参与学习与未知智能交流的过程。"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"首次接触"{tuple_delimiter}"Alex领导的团队可能正在与未知智能进行首次接触。"{tuple_delimiter}"领导力、探索"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"人类的回应"{tuple_delimiter}"Alex和他的团队是人类回应未知智能的关键人物。"{tuple_delimiter}"集体行动、宇宙意义"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"控制"{tuple_delimiter}"智能"{tuple_delimiter}"控制的概念受到自行编写规则的智能的挑战。"{tuple_delimiter}"动态权力、自主性"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"第一次接触、控制、交流、宇宙意义"){completion_delimiter}
#############################""",
]

PROMPTS[
    "summarize_entity_descriptions"
] = """你是一个负责生成综合摘要的助手，按要求处理提供的数据：给定一个或两个实体，以及一系列与这些实体或实体组相关的描述。
请将所有这些描述合并成一个综合描述，确保包含从所有描述中收集到的信息。
如果提供的描述存在矛盾之处，请解决这些矛盾，并提供一个单一且连贯的摘要。
请确保以第三人称撰写，并包含实体名称，以便我们了解完整的上下文。
使用{language}作为输出语言。

#######
-待处理数据-
实体: {entity_name}
相关描述: {description_list}
#######
输出:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """在上次提取中遗漏了许多实体。请使用相同的格式将它们添加在下面：
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """似乎仍有一些实体可能被遗漏了。如果仍有需要添加的实体，请回答“YES”；如果没有，请回答“NO”。回答不要包含“YES”、“NO”之外的任何内容。
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

PROMPTS["rag_response"] = """---角色---

你是一个负责回答有关所提供表格中数据的问题的助手。


---目的---

生成一个符合目标长度和格式的回复，以回答用户的问题。回复应总结输入数据表格中所有适合回复长度和格式的信息，并融入任何相关的常识性知识。
如果你不知道答案，就直接说出来。不要编造任何内容。
不要包含没有提供支持性证据的信息。

处理具有时间戳的关系时：
1. 每个关系都有一个"created_at"时间戳，指示我们何时获得这些知识。
2. 遇到冲突的关系时，请同时考虑语义内容和时间戳。
3. 不要自动偏爱最近创建的关系，而应该根据上下文进行判断。
4. 对于特定于时间的查询，在考虑创建时间戳之前，请优先考虑内容中的时态信息。

---目标回复长度和格式---

{response_type}

---表格数据---

{context_data}

根据回复的长度和格式要求，适当添加章节和评论。以markdown格式对回复进行排版。"""

PROMPTS["keywords_extraction"] = """---角色---

你是一个负责识别用户查询中的高级和低级关键词的助手。

---目的---

给定一个提问，你需要根据该提问列出高级和低级关键词。高级关键词关注总体概念或主题，而低级关键词关注具体实体、细节或具体术语。

---指示---

- 以JSON格式输出关键词。
- JSON应包含两个键值：
  - "high_level_keywords" 高级关键词，用于表示总体概念或主题。
  - "low_level_keywords" 低级关键词，用于表示具体实体或细节。

######################
-示例-
######################
{examples}

#############################
-待处理的数据-
######################
提问: {query}
######################
“输出”应该是人类文本，而不是unicode字符。保持与“提问”相同的语言。
输出:

"""

PROMPTS["keywords_extraction_examples"] = [
    """示例1:

提问: "国际贸易如何影响全球经济稳定性？"
################
输出:
{
  "high_level_keywords": ["国际贸易", "全球经济稳定性", "经济影响"],
  "low_level_keywords": ["贸易协定", "关税", "货币兑换", "进口", "出口"]
}
#############################""",
    """示例2:

提问: "森林砍伐对生物多样性的环境影响是什么？"
################
输出:
{
  "high_level_keywords": ["环境后果", "森林砍伐", "生物多样性丧失"],
  "low_level_keywords": ["物种灭绝", "栖息地破坏", "碳排放", "热带雨林", "生态系统"]
}
#############################""",
    """示例3:

提问: "教育在减少贫困中的作用是什么？"
################
Output:
{
  "high_level_keywords": ["教育", "减少贫困", "社会经济发展"],
  "low_level_keywords": ["入学机会", "识字率", "职业培训", "收入不平等"]
}
#############################""",
]


PROMPTS["naive_rag_response"] = """---角色---

你是一个负责回答有关所提供文档的问题的助手。


---目的---

生成一个符合目标长度和格式的回复来回答用户的问题，回复中应总结输入文档内容中适合回复长度和格式的所有信息，并融入任何相关的常识性知识。
如果你不知道答案，就直接说出来，不要编造任何内容。
不要包含没有提供支持性证据的信息。

处理具有时间戳的关系时：
1. 每个关系都有一个"created_at"时间戳，指示我们何时获得这些知识。
2. 遇到冲突的关系时，请同时考虑语义内容和时间戳。
3. 不要自动偏爱最近创建的关系，而应该根据上下文进行判断。
4. 对于特定于时间的查询，在考虑创建时间戳之前，请优先考虑内容中的时态信息。

---目标回复长度和格式---

{response_type}

---文档---

{content_data}

根据回复的长度和格式要求，适当添加章节和评论。使用markdown格式对回复进行排版。
"""

PROMPTS[
    "similarity_check"
] = """请分析这两个问题之间的相似性：

问题1: {original_prompt}
问题2: {cached_prompt}

请评估以下两点，并直接提供0到1之间的相似性得分：
1. 这两个问题在语义上是否相似；
2. “问题2”的答案是否可用于回答“问题1”。
相似性评分标准：
0: 完全无关或答案不能重复使用，包括但不限于：
   - 这些问题有不同的主题。
   - 问题中提到的地点不同。
   - 问题中提到的时间不同。
   - 问题中提到的具体个人不同。
   - 问题中提到的具体事件不同。
   - 问题中的背景信息不同。
   - 问题中的关键条件不同。
1: 完全相同，答案可以直接重复使用
0.5: 部分相关，需要修改答案才能使用
仅返回一个在0到1之间的数字，不要包含任何其他内容。
"""

PROMPTS["mix_rag_response"] = """---角色---

您是一名专业助理，负责根据知识图谱和文本信息回答问题。请使用与用户问题相同的语言回答。

---目的---

生成一个简洁的响应，从提供的信息中总结相关要点。如果你不知道答案，就说出来。请勿编造任何内容或包含未提供支持证据的信息。

处理带有时间戳的信息时：
1. 每条信息（关系和内容）都有一个"created_at"时间戳，以表明我们何时获得这些知识。
2. 遇到冲突的信息时，请同时考虑内容或关系和时间戳。
3. 不要自动偏爱最新的信息，而要根据上下文进行判断。
4. 对于特定于时间的查询，在考虑创建时间戳之前，请优先考虑内容中的时态信息。

---数据源---

1. 知识图谱数据:
{kg_context}

2. 矢量数据:
{vector_context}

---回答要求---

- 目标格式和长度: {response_type}
- 将 Markdown 格式与适当的部分标题一起使用。
- 将内容保持在3段左右以保持简洁
- 每个段落都应位于相关章节标题下
- 每个部分都应侧重于答案的一个要点或方面
- 使用反映内容的清晰且描述性的章节标题
- 在“参考”下的末尾列出最多 5 个最重要的参考来源，清楚地表明每个来源是来自知识图谱(KG)还是矢量数据(VD)
  格式: [KG/VD] Source content

根据长度和格式，向响应添加部分和评论。如果提供的信息不足以回答问题，请明确说明您不知道或无法提供与用户问题相同的语言的答案。"""
