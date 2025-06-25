<script setup>
import {h, ref} from 'vue'
import {UseLang} from "@/languages/language.js"
import {api, download_model} from '@/api.js'
import {sleep, wait_until} from "@/util.js";

const lang = UseLang()
const model_list = ref([])
const settings = ref({})
const loading = ref(true)
const model = ref(false)
let close_handle = ()=>null

window.open_settings = async () => {
  loading.value = true;
  model.value = true
  settings.value = await api().config.gets()
  model_list.value = await api().llm.list()
  while(model_list.value.length == 0){
    const model_name = await download_model('bge-m3')
    model_list.value = await api().llm.list()
    settings.value.local_model = model_name
  }
  loading.value = false
  await new Promise(resolve=>{close_handle=resolve})
}

const on_close = async (done) => {
  if(settings.value.local_model == ''){
    ElMessageBox.alert(lang.no_local_model, lang.warning, {
      confirmButtonText: lang.ok,
    })
    return
  }
  await api().config.update(settings.value)
  close_handle()
  done()
}

const use_local_llm = async () => {
  settings.value.online_model = await download_model('deepseek-r1:14b')
  settings.value.online_base_url = 'https://127.0.0.1:11434/v1'
  settings.value.api_key = 'ollama'
}

</script>

<template>
  <el-drawer
    v-model="model"
    style="z-index: 99999"
    :before-close="on_close"
  >
    <h4>{{ lang.settings }}</h4>
    <div v-if="loading">
      <el-result
        :title="lang.loading"
      >
      </el-result>
    </div>
    <div v-else="loading">

      <el-divider content-position="left">{{ lang.llm }} API {{ lang.url }}</el-divider>
      <el-input
        v-model="settings.online_base_url"
        :placeholder="'API'+lang.url"
        spellcheck="false"
        clearable
      />
      <el-divider content-position="left">{{ lang.llm }} {{ lang.name }}</el-divider>
      <el-input
        v-model="settings.online_model"
        :placeholder="lang.llm+' '+lang.name"
        spellcheck="false"
        clearable
      />
      <el-divider content-position="left">API KEY</el-divider>
      <el-input
        v-model="settings.api_key"
        placeholder="API KEY"
        spellcheck="false"
        type="password"
        show-password
      />
      <el-divider content-position="left">{{ lang.local }} Embedding {{ lang.model }}</el-divider>
      <el-select
        v-model="settings.local_model"
        placeholder="Select"
      >
        <el-option
          v-for="item in model_list"
          :key="item"
          :label="item"
          :value="item"
        />
      </el-select>
      <el-divider content-position="left">{{ lang.download }} {{ lang.local }} {{ lang.llm }}</el-divider>
      <el-button style="width: 100%" @click="use_local_llm" plain>{{lang.download}}</el-button>

       <el-collapse v-model="activeNames" @change="handleChange">
         <el-collapse-item :title="lang.pro_settings">
           <el-divider content-position="left">{{lang.chunk_size}}</el-divider>
           <el-input
              v-model="settings.chunk_size"
              placeholder=""
              type="number"
           />
           <el-divider content-position="left">{{lang.thread_number}}</el-divider>
           <el-input
              v-model="settings.thread_number"
              placeholder=""
              type="number"
           />
         </el-collapse-item>
       </el-collapse>
    </div>
  </el-drawer>
</template>

<style scoped>

</style>