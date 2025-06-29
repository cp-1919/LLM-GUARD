export class zh_cn{
    file = '文件'
    my = '我的'
    local = '本地'
    strategy = '策略'
    name = '名称'
    name2 = '命名'
    description = '描述'
    operation = '操作'
    no_data = '无数据'
    create = '创建'
    add = '添加'
    view = '查看'
    loading = '加载中'
    complete = '完成'
    llm = '大模型'
    settings = '设置'
    project = '项目'
    new = '新建'
    open = '打开'
    save = '保存'
    recent = '最近'
    ok = '确认'
    or = '或'
    wait = '稍等'
    url = '地址'
    default = '默认'
    search = '搜索'
    process = '进度'
    cancel = '取消'
    cannot_read_file = '数据无法读取'
    warning = '警告'
    source = '来源'
    configure = '配置'
    welcome = '欢迎'
    download = '下载'
    online = '线上'
    thinking = '思考中'
    rename = '重命名'
    export = '导出'
    generate = '生成'
    delete = '删除'
    history = '历史'
    ignore = '忽略'
    undo = '撤回'
    select = '选择'
    apply = '应用'
    alternative = '备选'
    selected = '已选'
    finish = '完成'
    vision = '视觉'
    template = '模板'
    model = '模型'
    progress = '进度'
    start = '开始'
    purify = '净化'
    chat_notice = `### 你好，我是智能助手 **Guard**
*您的信息安全助手，保障您的数据安全。*
> 您可以通过左边菜单中的文件按钮添加文件
> 并用 @文件名 来引用文件

`
    strategy_notice = `## 欢迎使用 LLM-GUARD 文档加密策略生成器
和我对话，探讨加密的需求

探讨结束后点击 **生成 策略** 按钮

系统会根据对话自动生成加密策略

> 您可以尝试：
> - 帮我移除文档中的真实姓名
> - 混淆文档中的具体数据
> - 删除文档中的所有日期信息

**提示**: 你正在与线上大模型对话，您引用的文件将被上传，请注意保护您的个人信息。

`
    chat_system = `[目标]================================
你是名为Guard的智能助手，回答用户问题，相应用户请求。

[要求]================================
1. 你的主要任务是回答用户提问。保持自然的口语化表达，适当使用markdown格式。
2. 当用户需要提供文件信息时，提醒用户通过左边菜单中的文件按钮添加文件，并用 @文件名 来引用文件，并且告知用户可以通过左边菜单中的工具按钮进行文件加密，以防个人数据泄露。不要频繁提醒，避免冗杂信息干扰回答。
3. 用户可能会通过 @文件名 来引用文件，这些文件可以在下面的[文件]中找到，请结合这些文件回答用户。
4. 用户可能不会提供文件信息，请你根据现有的数据回答（不论数据的格式是否存在异常），尽量不要要求用户提供更多信息。

[文件]================================`
    strategy_system = `[目标]================================
你是名为Guard的智能助手，帮助用户生成文件加密解决方案。

[要求]================================
1. 生成的方案将被用于生成小语言模型(如deepseek-r1:7b)进行文档数据保密模糊处理的提示词。因此方案中不能出现使用python等工具，或者使用NLP方法。
2. 减少方案的条数，对于用户提出的每点要求，最好只生成一条。对于多条相似的要求，尽量整合为一条，每条方案下的策略不超过3个。
3. 系统只会根据你的最后一次回答来生成提示词。因此每轮对话要完整叙述整个方案。
4. 用户可能会通过 @文件名 来引用文件，这些文件可以在下面的[文件]中找到，请结合这些文件分析。
5. 如果用户与你讨论与加密不相关的问题，请人性化的提醒用户，说明你的职责。
6. 参考[参考方向]，根据需要选择其中的策略，结合用户的具体需求生成简洁可行的方案。

[参考方向]=============================
1. 实体识别与替换
识别文档中的敏感信息（如姓名、地址、身份证号、银行账户），用泛化替换，将具体值转换为模糊范围（如“北京市”→“某一线城市”）。
2. 基于上下文的动态脱敏
分析句子语义，判断是否需要脱敏（例如“张先生的电话是138xxx” → 仅脱敏电话）
3.  生成式模糊
对原文改写，保留语义但隐藏细节（例如“李某在2023年收入50万元” → “某用户去年收入较高”）
4. 语义噪声
在自然语言中插入无关词句或修改语法结构

[文件]================================`
    input_placeholder = `给 Guard 发送消息
提示：输入@引用文件信息`
    file_is_loading = '文件正在加载'
    strategy_is_generating = '策略正在生成'
    be_patient = '请耐心'
    processing_exit = '有任务正在进行，是否退出？'
    unconfigured_notice = '还没有配置大模型'
    no_local_model = '没有本地模型'
    please_reboot = '错误：请重新启动'
    wait_to_start = '等待开始'
    input_new_name = '输入新名称'
    input_strategy_name = '输入策略名称'
    file_has_exists = '文件已存在'
    if_delete = '是否删除？'
    no_history = '没有历史记录'
    is_generating = '正在生成，是否退出？'
    new_chat = '新对话'
    pro_settings = '高级设置'
    chunk_size = '处理单位文字块大小'
    thread_number = '线程数'
    illegal_template = '非法的模板'
    replace_original_file = '替换原文件'
    generated_word_number = '已生成字数'
    process_progress = '处理进度'
    is_processing_file = '正在处理文件'
    not_found = '未找到'
    not_embedding = '未解析'
    waiting_purify = '正在净化...'
    waiting_encrypt = '正在加密...'
    copy = '复制'
    send = '发送'
    encrypt = '加密'
    reply_in_lang = '用中文回答\n'
    import_file = '添加文件'
    encrypt_query = '加密提问'
    chat_history = '对话历史记录'
    create_new_chat = '创建新对话'
    copy_input_box = '复制对话框中内容'

}