export class en {
    file = 'File'
    my = 'My'
    local = 'Local'
    strategy = 'Strategy'
    name = 'Name'
    name2 = 'Rename'
    description = 'Description'
    operation = 'Action'
    no_data = 'No Data'
    create = 'Create'
    add = 'Add'
    view = 'View'
    loading = 'Loading'
    complete = 'Complete'
    llm = 'LLM'
    settings = 'Settings'
    project = 'Project'
    new = 'New'
    open = 'Open'
    save = 'Save'
    recent = 'Recent'
    ok = 'OK'
    or = 'or'
    wait = 'Please Wait'
    url = 'URL'
    default = 'Default'
    search = 'Search'
    process = 'Process'
    cancel = 'Cancel'
    cannot_read_file = 'Unable to read data'
    warning = 'Warning'
    source = 'Source'
    configure = 'Configure'
    welcome = 'Welcome'
    download = 'Download'
    online = 'Online'
    thinking = 'Thinking'
    rename = 'Rename'
    export = 'Export'
    generate = 'Generate'
    delete = 'Delete'
    history = 'History'
    ignore = 'Ignore'
    undo = 'Undo'
    select = 'Select'
    apply = 'Apply'
    alternative = 'Alternative'
    selected = 'Selected'
    finish = 'Finish'
    vision = 'Vision'
    template = 'Template'
    model = 'Model'
    progress = 'Progress'
    start = 'Start'
    purify = 'Purify'
    chat_notice = `### Hello, I'm ​**Guard**, your AI assistant
*Your information security assistant, safeguarding your data.*
> You can add files using the File button in the left menu
> Use @filename to reference files
`
    strategy_notice = `## Welcome to the LLM-GUARD Document Encryption Strategy Generator
Discuss encryption requirements with me

After discussion, click the ​**Generate Strategy**​ button

The system will automatically generate an encryption strategy based on our conversation

> You can try:
> - Help me remove real names from the document
> - Obfuscate specific data in the document
> - Delete all date information in the document

​**Note**: You are conversing with an online LLM. Files you reference will be uploaded. Please protect your personal information.
`
    chat_system = `[Objective]================================
You are Guard, an AI assistant tasked with answering user questions and responding to their requests.

[Requirements]================================
1. Maintain a natural, conversational tone. Use markdown formatting appropriately.
2. When the user needs to provide file information, remind them to add files using the File button in the left menu and reference them using @filename. Inform users they can use the Tools button in the left menu to encrypt files to prevent personal data leaks.
3. Users might reference files using @filename. These files are available in the [Files] section below. Incorporate these files into your responses.

[Files]================================`
    strategy_system = `[Objective]================================
You are Guard, an AI assistant helping users generate file encryption solutions.

[Requirements]================================
1. The generated solution will be used to create prompts for small language models (e.g., deepseek-r1:7b) for confidential document data blurring/obscuring. Therefore, the solution MUST NOT involve tools like Python or NLP methods.
2. Reduce the number of solution items. For each user requirement, ideally generate only one item. Consolidate similar requirements into one item. Each item should contain a maximum of 3 strategies.
3. The system will ONLY use your last response to generate the prompt. Therefore, each response must contain the complete, full solution.
4. Users might reference files using @filename. These files are available in the [Files] section below. Analyze user needs incorporating these files.
5. If the user discusses topics unrelated to encryption, politely remind them of your core function.
6. Refer to the [Reference Directions]. Select strategies from them as needed, combining them with the user's specific requirements to create concise, actionable solutions.

[Reference Directions]=============================
1. Entity Recognition & Replacement
Identify sensitive information (names, addresses, IDs, bank accounts) and replace it with generalized terms or convert specific values to fuzzy ranges (e.g., "Beijing" → "a first-tier city").
2. Context-Based Dynamic Masking
Analyze sentence semantics to determine if masking is needed (e.g., "Mr. Zhang's phone number is 138xxx" → only mask the phone number).
3. Generative Obfuscation
Paraphrase the original text, preserving meaning while hiding details (e.g., "Li earned 500,000 yuan in 2023" → "A user had a high income last year").
4. Semantic Noise
Insert irrelevant phrases or alter grammatical structures within the natural language flow.

[Files]================================`
    input_placeholder = `Send a message to Guard
Tip: Use @ to reference file information`
    file_is_loading = 'File is loading'
    strategy_is_generating = 'Strategy is generating'
    be_patient = 'Please be patient'
    processing_exit = 'Tasks are in progress. Exit anyway?'
    unconfigured_notice = 'No LLM configured'
    no_local_model = 'No local model available'
    please_reboot = 'Error: Please restart'
    wait_to_start = 'Waiting to start'
    input_new_name = 'Enter new name'
    input_strategy_name = 'Enter strategy name'
    file_has_exists = 'File already exists'
    if_delete = 'Delete?'
    no_history = 'No history'
    is_generating = 'Generation in progress. Exit?'
    new_chat = 'New Chat'
    pro_settings = 'Advanced Settings'
    chunk_size = 'Processing chunk size'
    thread_number = 'Number of threads'
    illegal_template = 'Invalid template'
    replace_original_file = 'Replace original file'
    generated_word_number = 'Words generated'
    process_progress = 'Processing progress'
    is_processing_file = 'Processing file'
    not_found = 'Not found'
    not_embedding = 'Not parsed'
    waiting_purify = 'Purifying...'
    waiting_encrypt = 'Encrypting...'
    copy_encrypt = 'Copy ciphertext'
    reply_in_lang = 'Reply in Chinese\n'
    import_file = 'Add File'
}