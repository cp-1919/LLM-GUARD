<script setup>
import InputBox from "@/components/InputBox.vue";
import { Promotion, DocumentAdd } from '@element-plus/icons-vue';
import {ref, onBeforeUnmount} from "vue";
import {UseLang} from "@/languages/language.js";
import {MdPreview} from 'md-editor-v3';
import 'md-editor-v3/lib/preview.css';
import {sleep, wait_until, window_resize} from "@/util.js";
import {api} from "@/api.js";
import OpenAI from "openai";
import {ElMessageBox} from "element-plus";

const llm_config = ref({})
const mode = ref('chat');
const lang = UseLang();
const padding_height = ref(0)
const messages = ref([])
const new_chunk_content = ref('')

const unmounted = ref(false)
onBeforeUnmount(()=>unmounted.value=true)

const select_model_panel = ref(false);
const history_panel = ref(false);
const history_idx = ref(0)
const history_list = ref([]);

const scroll_container = ref()
const scroll_body = ref()
const scrollBottom = async () => {
  scroll_container.value.scroll({
    top: scroll_body.value.scrollHeight,
    behavior: 'smooth'
  })
}

const input = ref('')
const input_disabled = ref(false)
const input_options = ref([])
const input_select = ref([])

const onInputSelect = async (selectedItem) => {
  input_select.value.push(selectedItem.value)
}

let file_info = ''
const getFileInfo = async (
    spliter = i=>`\n\n\n==${i}============================================\n`
) => {
  file_info = ''
  for (let i of input_select.value) {
    if (input.value.indexOf('@' + i) != -1) {
      file_info += spliter(i)
      const file_text = await api().file.get(i, input.value)
      if(file_text.state == 'not found'){
        await ElMessageBox.alert(`${i} ${lang.not_found}`, lang.warning)
        return false
      }else if(file_text.state == 'not embedding'){
        await ElMessageBox.alert(`${i} ${lang.not_embedding}`, lang.warning)
        return false
      }
      file_info += file_text.content
    }

  }
  return true
}

const onEncrypt = async () => {
  input_disabled.value = true
  const input_val = input.value
  if(!await getFileInfo(i=>`---\n${i}:\n`))return
  input.value = lang.waiting_encrypt
  const original_prompt = file_info+'\n'+input_val
  const res = await api().llm.encrypt(original_prompt)
  await navigator.clipboard.writeText(lang.reply_in_lang+res)
  input_select.value = []
  input_disabled.value = false
  input.value = lang.reply_in_lang+res
}

const onGPTCalled = async () => {
  if (input_disabled.value) return
  input_disabled.value = true
  window.generating = true
  const conf = await api().config.gets()
  const client = new OpenAI({
    baseURL: conf.online_base_url,
    apiKey: conf.api_key,
    dangerouslyAllowBrowser: true,
  })
  messages.value.push({
    role: 'user', content: input.value,
  })
  if(!await getFileInfo())return
  input.value = ''
  new_chunk_content.value = lang.thinking + '...'
  scrollBottom()
  messages.value[0].content = lang.chat_system + file_info
  const stream = await client.chat.completions.create({
    model: conf.online_model,
    messages: window.messages,
    stream: true,
  });
  let thinking = true
  for await (const chunk of stream) {
    if (unmounted.value)return
    if (thinking) {
      if ((chunk.choices[0]?.delta?.content || '') != '') {
        new_chunk_content.value = chunk.choices[0]?.delta.content
        thinking = false
      }
      continue
    }
    new_chunk_content.value += (chunk.choices[0]?.delta?.content || '');
  }
  messages.value.push({
    role: 'assistant', content: new_chunk_content.value
  })
  window.messages = messages.value
  new_chunk_content.value = ''
  await api().file.update_history(window.history_idx, window.messages)
  input_disabled.value = false
  window.generating = false
}

const createHistory = async () => {
  window.messages = [
    {role: 'system', content: lang.strategy_system}
  ]
  window.history_idx = 0
  history_idx.value = window.history_idx
  await api().file.create_history(window.messages)
  messages.value = window.messages
  history_list.value = await api().file.list_history()
}
const getHistory = async (idx) => {
  if(history_list.value.length == 0){
    await createHistory()
    return
  }
  window.history_idx = idx
  history_idx.value = window.history_idx
  window.messages = await api().file.get_history(idx)
  messages.value = window.messages
  history_panel.value = false
  await sleep(0.8)
  await scrollBottom()
}
const onOpenHistory = async () => {
  history_panel.value = true
}
const onRemoveHistory = async (idx) => {
  if(idx == window.history_idx)getHistory(0)
  if(await api().file.remove_history(idx)){
    history_list.value = await api().file.list_history()
    await getHistory(0)
  }else{}
}

const onUpdateLLM = async (done) => {
  await api().config.update(llm_config.value)
  done()
}

(async () => {
  history_list.value = await api().file.list_history()
  console.log(history_list.value)
  input_options.value = (await api().file.list()).map(item => ({value: item.name, label: item.name}))
  if ('messages' in window && window.messages != null) {
    while (window.messages[window.messages.length - 1].role == 'user') {
      window.messages.pop()
    }
    messages.value = window.messages
  }else{
    await getHistory(0)
  }

  const conf = await api().config.gets()
  if(conf.chat_model == ''){
    conf.chat_model = conf.online_model
    conf.chat_base_url = conf.online_base_url
    conf.chat_api_key = conf.api_key
    await api().config.update(conf)
  }
  llm_config.value = conf

  history_idx.value = window.history_idx
  mode.value = 'chat'
  await sleep(0.8)
  await scrollBottom()
})()

</script>

<template>

  <transition name="el-fade-in-linear" mode="out-in">


    <div class="full-container" v-if="mode=='chat'">
      <div class="auto-follow-container sticky-bottom" ref="scroll_container">
        <div class="transition-box workspace-container" ref="scroll_body">
          <div class="allow-copy">
            <MdPreview :modelValue="lang.chat_notice"/>
            <div v-for="message in messages">
              <MdPreview v-if="message.role=='assistant'" :modelValue="message.content"/>
              <div class="box-radius question-box" v-if="message.role=='user'">{{ message.content }}</div>
            </div>
            <MdPreview :modelValue="new_chunk_content"/>
          </div>
        </div>
      </div>

      <div class="auto-fixed-container">
        <input-box v-model="input" :options="input_options" :select="onInputSelect">
          <div class="input-box-button-container">
            <el-button class="input-box-btn-left" type="success" :disabled="input_disabled" @click="select_model_panel=true" link>@{{ llm_config.chat_model }}</el-button>
            <div class="input-box-btn-right">
              <el-button-group class="input-box-btn">
                <el-button type="success" :disabled="input_disabled" @click="onOpenHistory" round>{{ lang.history }}</el-button>
                <el-button type="success" :disabled="input_disabled" @click="createHistory" round>{{ lang.new_chat }}</el-button>
              </el-button-group>
              <el-button class="input-box-btn" type="success" :disabled="input_disabled" @click="onEncrypt" round>{{ lang.copy_encrypt }}</el-button>
              <el-button class="input-box-btn" type="success" :disabled="input_disabled" @click="api().file.add()" :icon="DocumentAdd" circle size="large"/>
              <el-button class="input-box-btn" type="success" :disabled="input_disabled" @click="onGPTCalled" :icon="Promotion" circle size="large"/>
              <el-button-group class="input-box-btn">
              </el-button-group>
            </div>
            </div>
        </input-box>
      </div>


    </div>


  </transition>

  <el-drawer v-model="history_panel">
    <div class="box-radius history-container" v-for="(value, idx) in history_list">
      <el-text class="w-150px" truncated v-if="idx != history_idx" @click="getHistory(idx)">
        {{value=='new chat'?lang.new_chat:value}}
      </el-text>
      <el-text class="w-150px" truncated v-else :style="{color:'#4084ff'}">
        {{value=='new chat'?lang.new_chat:value}}
      </el-text>
      <el-button class="history-operate-btn" size="small" @click.prevent="onRemoveHistory(idx)" round>
        {{ lang.delete }}
      </el-button>
    </div>
    <el-empty v-if="history_list.length==0" :description="lang.no_history" />
  </el-drawer>

  <el-drawer :before-close="onUpdateLLM" v-model="select_model_panel">
    <h3>{{`${lang.configure} ${lang.llm}`}}</h3>
    <el-divider content-position="left">{{ lang.llm }} API {{ lang.url }}</el-divider>
    <el-input
      v-model="llm_config.chat_base_url"
      :placeholder="'API'+lang.url"
      spellcheck="false"
      clearable
    />
    <el-divider content-position="left">{{ lang.llm }} {{ lang.name }}</el-divider>
    <el-input
      v-model="llm_config.chat_model"
      :placeholder="lang.llm+' '+lang.name"
      spellcheck="false"
      clearable
    />
    <el-divider content-position="left">API KEY</el-divider>
    <el-input
      v-model="llm_config.chat_api_key"
      placeholder="API KEY"
      spellcheck="false"
      type="password"
      show-password
    />
  </el-drawer>

</template>

<style scoped>

.input-box-button-container {
  display: flex;
  width: 100%;
}

.question-box {
  display: flex;
  width: fit-content;
  max-width: 60%;
  margin-left: auto;
  margin-right: 20px;
  padding: 10px;
  background-color: #f3f4f6;
  border: transparent;
}

.history-container {
  display: flex;
  padding: 10px;
}

.history-operate-btn {
  margin-right: 0;
  margin-left: auto;
}

.input-box-btn {
  margin-right: 5px;
  margin-left: 5px;
}

.input-box-btn-left {
  margin-left: 5px;
  margin-right: auto;
}

.input-box-btn-right {
  margin-left: auto;
  margin-right: 5px;
}

.allow-copy {
  -webkit-user-select: text;
  user-select: text;
}

</style>