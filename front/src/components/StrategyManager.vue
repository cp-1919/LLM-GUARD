<script setup>
import InputBox from "@/components/InputBox.vue";
import { Promotion } from '@element-plus/icons-vue';
import {ref, computed, watch, onBeforeUnmount} from "vue";
import {UseLang} from "@/languages/language.js";
import {MdPreview} from 'md-editor-v3';
import 'md-editor-v3/lib/preview.css';
import {sleep, wait_until, window_resize} from "@/util.js";
import {api} from "@/api.js";
import OpenAI from "openai";

import Process from "@/components/Process.vue";

const mode = ref('');
const lang = UseLang();
const padding_height = ref(0)
const messages = ref([])
const new_chunk_content = ref('')
const project_strategy_select = ref('')
const project_strategy = ref([])
const filter_project_strategy = computed(()=>
    project_strategy.value.filter(data=>!project_strategy_select.value ||
    data.name.toLowerCase().includes(project_strategy_select.value.toLowerCase()))
);
const selected_strategy = ref('')

const unmounted = ref(false)
onBeforeUnmount(()=>unmounted.value=true)

const resetGPTContext = async () => {
  window.gen_messages = [
    {role: 'user', content: lang.strategy_system},
    {role: 'assistant', content: ''}
  ]
  messages.value = window.gen_messages
}

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

const onAddStrategy = async () => {
  input_options.value = (await api().file.list()).map(item=>({value: item.name, label: item.name}))
  if(!('gen_messages' in window) || window.gen_messages == null){
    await resetGPTContext()
  }else{
    messages.value = window.gen_messages
  }
  mode.value = 'chat'
  await sleep(0.8)
  scrollBottom()
}

const onGPTCalled = async () => {
  if(input_disabled.value)return
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
  // find selected files
  let file_info = ''
  for(let i of input_select.value){
    if(input.value.indexOf('@'+i)!=-1){
      file_info += `\n\n\n==${i}============================================\n`
      file_info += (await api().file.get(i)).content
    }
  }
  input.value = ''
  new_chunk_content.value = lang.thinking + '...'
  scrollBottom()
  messages.value[0].content = lang.strategy_system+file_info
  window.gen_messages = messages.value
  const stream = await client.chat.completions.create({
    model: conf.online_model,
    messages: window.gen_messages,
    stream: true,
  });
  let thinking = true
  for await (const chunk of stream) {
    if(thinking){
      if(unmounted.value)return
      if((chunk.choices[0]?.delta?.content || '') != ''){
        new_chunk_content.value = chunk.choices[0]?.delta.content
        thinking = false
      }
      continue
    }
    new_chunk_content.value += (chunk.choices[0]?.delta?.content || '');
  }
  messages.value.push({
    role:'assistant', content:new_chunk_content.value
  })
  new_chunk_content.value = ''
  input_disabled.value = false
  window.generating = false
}

const onCommit = async () => {
  let name = (await (ElMessageBox.prompt(lang.input_strategy_name, lang.name2, {
    confirmButtonText: lang.ok,
    cancelButtonText: lang.cancel,
  }))).value
  const file_names = project_strategy.value.map(item=>item.name)
  while(file_names.includes(name)){
    name = (await (ElMessageBox.prompt(lang.input_strategy_name, lang.file_has_exists, {
      confirmButtonText: lang.ok,
      cancelButtonText: lang.cancel,
    }))).value
  }
  mode.value = 'generating'
  await api().llm.generate_strategy(messages.value[messages.value.length-1].content, name)
  window.gen_messages = null
  project_strategy.value = await api().file.get_strategies()
  mode.value = 'list'
}
const onCancel = async () => {
  window.gen_messages = null
  mode.value = 'list'
}
const deleteRow = async (idx) => {
  try{
    await ElMessageBox.confirm(lang.if_delete, lang.delete, {
      confirmButtonText: lang.ok,
      cancelButtonText: lang.cancel,
    })
  }catch (e){
    return
  }
  mode.value = ''
  await api().file.remove_strategy(project_strategy.value[idx].name)
  project_strategy.value = await api().file.get_strategies()
  mode.value = 'list'
}
const onCallProcess = async (idx) => {
  selected_strategy.value = project_strategy.value[idx].name
  console.log(selected_strategy.value)
  mode.value = 'process'
}

const generated_word_number = ref(0)
const process_state = ref('')
watch(mode, async (new_mode) => {
  if(new_mode != 'processing')return;
  await wait_until(async()=>{
    process_state.value = await api().llm.get_state()
    if(process_state.value == 'done')return true
    generated_word_number.value = await api().llm.get_total_word()
    return false
  }, 1)
  mode.value = 'list'
});

(async () => {
  mode.value = ''
  if(await api().llm.get_strategy_gen_state() == 'generating'){
    mode.value = 'generating'
    await wait_until(async()=>await api().llm.get_strategy_gen_state()=='done', 1)
  }
  if(await api().llm.get_state() != 'done'){
    mode.value = 'processing'
  }else {
    if ('gen_messages' in window && window.gen_messages != null) {
      while (window.gen_messages[window.gen_messages.length - 1].role == 'user') {
        window.gen_messages.pop()
      }
      await onAddStrategy()
    } else {
      mode.value = 'list'
    }
  }
  project_strategy.value = await api().file.get_strategies();
})()
</script>

<template>

  <transition name="el-fade-in-linear" mode="out-in">


    <div class="transition-box workspace-container" v-if="mode=='list'">
      <el-divider content-position="left">{{ lang.encrypt }} {{ lang.strategy }}</el-divider>
      <el-table :data="filter_project_strategy" style="width: 100%" max-height="250">
        <el-table-column fixed prop="name" :label="lang.name"/>
        <el-table-column fixed="right" :label="lang.operation" width="120">
          <template #header>
            <el-input v-model="project_strategy_select" size="small" :placeholder="lang.search" />
          </template>
          <template #default="scope">
            <el-button
                plain
                type="success"
                size="small"
                @click.prevent="onCallProcess(scope.$index)"
            >
              {{ lang.apply }}
            </el-button>
            <el-button
                link
                type="danger"
                size="small"
                @click.prevent="deleteRow(scope.$index)"
            >
              {{ lang.delete }}
            </el-button>
          </template>
        </el-table-column>
        <template #empty>
          {{ lang.no_data }}
        </template>
      </el-table>
      <el-button class="mt-4" style="width: 100%" @click="onAddStrategy">
        {{ `${lang.create} ${lang.strategy}` }}
      </el-button>
    </div>


    <div class="transition-box full-container" v-else-if="mode=='chat'">
      <div class="auto-follow-container" ref="scroll_container">
        <div class="workspace-container" ref="scroll_body">
          <MdPreview :modelValue="lang.strategy_notice"/>
          <div v-for="(message, idx) in messages">
            <MdPreview v-if="message.role=='assistant'" :modelValue="message.content"/>
            <div class="box-radius question-box" v-if="message.role=='user'&&idx!=0">{{message.content}}</div>
          </div>
          <MdPreview :modelValue="new_chunk_content"/>
        </div>
      </div>
      <div class="auto-fixed-container">
        <input-box v-model="input" :options="input_options" :select="onInputSelect">
          <div class="input-box-button-container">
            <el-button type="success" :disabled="input_disabled" @click="onCancel" round>{{ lang.cancel }}</el-button>
            <el-button type="success" :disabled="input_disabled" @click="onCommit" round>{{ lang.generate }} {{ lang.strategy }}</el-button>
            <el-button type="success" :disabled="input_disabled" :icon="Promotion" @click="onGPTCalled" round/>
          </div>
        </input-box>
      </div>
    </div>


    <div class="transition-box full-container" v-else-if="mode=='process'">
      <process v-model="mode" :strategy="selected_strategy"></process>
    </div>


    <div class="transition-box workspace-container" v-else-if="mode=='generating'">
      <el-result icon="info" :title="lang.strategy_is_generating">
        <template #sub-title>
          <p>{{ lang.be_patient }}</p>
        </template>
      </el-result>
    </div>



    <div class="transition-box workspace-container" v-else-if="mode=='processing'">
      <el-result icon="info" :title="lang.is_processing_file">
        <template #sub-title>
          <p>{{ lang.be_patient }}</p><br>
        </template>
      </el-result>
      <el-row>
        <el-col style="text-align: center" :span="8"><el-statistic :title="lang.generated_word_number" :value="generated_word_number" /></el-col>
        <el-col :span="8"></el-col>
        <el-col style="text-align: center" :span="8"><el-statistic :title="lang.process_progress" :value="process_state" /></el-col>
      </el-row>
    </div>


  </transition>

</template>

<style scoped>

.input-box-button-container {
  display: flex;
  justify-content: flex-end;
  margin-left: auto;
  margin-right: 10px;
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
</style>