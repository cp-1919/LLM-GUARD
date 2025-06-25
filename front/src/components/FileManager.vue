<script setup>
import {ref, computed} from "vue";
import {UseLang} from "@/languages/language.js";
import {MdPreview} from 'md-editor-v3';
import 'md-editor-v3/lib/preview.css';
import {api} from '@/api.js';
import {ElMessage} from "element-plus";
import {wait_until} from "@/util.js";
import {CloseBold} from "@element-plus/icons-vue";

const doc_loading = ref(true)
const mode = ref('none')
const lang = UseLang()
const file_list = ref([])
const search = ref('')
const filter_file_list = computed(()=>
  file_list.value.filter((data)=>!search.value ||
      data.name.toLowerCase().includes(search.value.toLowerCase()))
)
const file_read_state = ref('')
const text = ref(lang.loading);

(async () => {
  if(await api().file.get_state() != 'done'){
    mode.value = 'loading'
    await wait_until(async ()=>{
      file_read_state.value = await api().file.get_state()
      return file_read_state.value == 'done'
    },1)
  }
  file_list.value = await api().file.list()
  mode.value = 'list'
})()

const onAddFile = async () => {
  mode.value = 'loading'
  api().file.add()
  await wait_until(async ()=>{
    file_read_state.value = await api().file.get_state()
    return file_read_state.value == 'done'
  },1)
  file_list.value = await api().file.list()
  mode.value = 'list'
}

const onReadFile = async (idx) => {
  doc_loading.value = true
  text.value = (await api().file.get(file_list.value[idx].name)).content
  mode.value = 'read'
  doc_loading.value = false
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
  await api().file.remove(file_list.value[idx].name);
  file_list.value = await api().file.list()
  mode.value = 'list'
}

const onRename = async (idx) => {
  const new_name = (await ElMessageBox.prompt(lang.input_new_name,lang.rename,{
    confirmButtonText: lang.ok,
    cancelButtonText: lang.cancel,
  })).value
  if(await api().file.rename(file_list.value[idx].name, new_name)){
    mode.value = ''
    file_list.value = await api().file.list()
    mode.value = 'list'
  }else{
    ElMessageBox.alert(lang.file_has_exists, lang.warning, {confirmButtonText: lang.ok})
  }
}

const onExport = async (idx) => {
  await api().file.export(file_list.value[idx].name);
}

</script>

<template>
  <transition name="el-fade-in-linear" mode="out-in">


    <div class="transition-box workspace-container" v-if="mode=='list'">
      <el-divider content-position="left">{{ lang.file }}</el-divider>
      <el-button class="mt-4" style="width: 100%" @click="onAddFile">
        {{ `${lang.add} ${lang.file}` }}
      </el-button>
      <el-table :data="filter_file_list" style="width: 100%" max-height="250">
        <el-table-column fixed prop="name" :label="`${lang.file} ${lang.name}`"/>
        <el-table-column fixed prop="from" :label="lang.source"/>
        <el-table-column fixed="right" :label="lang.operation" width="200">
          <template #header>
          <el-input v-model="search" size="small" :placeholder="lang.search" />
        </template>
          <template #default="scope">
            <el-button
                link
                type="primary"
                size="small"
                @click.prevent="onReadFile(scope.$index)"
            >
              {{ lang.view }}
            </el-button>
            <el-button
              link
              type="primary"
              size="small"
              @click.prevent="onRename(scope.$index)"
            >
              {{ lang.rename }}
            </el-button>
            <el-button
                link
                type="primary"
                size="small"
                @click.prevent="onExport(scope.$index)"
            >
              {{ lang.export }}
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

    </div>


    <div v-loading="doc_loading" class="transition-box workspace-container" v-else-if="mode=='read'">
      <el-affix :offset="110">
        <el-button class="close_btn" type="primary" :icon="CloseBold" @click="mode='list'" circle></el-button>
      </el-affix>
      <MdPreview :modelValue="text"/>
    </div>


    <div class="transition-box full-container" v-else-if="mode=='loading'">
      <el-result icon="info" :title="lang.file_is_loading">
        <template #sub-title>
          <p>{{ lang.be_patient }}</p>
          <p>{{`${lang.progress}:${file_read_state}`}}</p>
        </template>
      </el-result>
    </div>


  </transition>

</template>

<style scoped>
  .close_btn {
    margin-left: 0;
  }
</style>