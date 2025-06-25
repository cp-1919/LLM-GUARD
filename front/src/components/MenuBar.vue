<script setup>
import {ref} from 'vue'
import {api} from "@/api.js"
import {UseLang} from "@/languages/language.js"
import WindowClose from "@/assets/icons/WindowClose.vue"
import WindowMaximize from "@/assets/icons/WindowMaximize.vue"
import WindowUnmaximize from "@/assets/icons/WindowUnmaximize.vue"
import WindowMinimize from "@/assets/icons/WindowMinimize.vue"
import SettingsIcon from "@/assets/icons/Settings.vue"
import Settings from "@/components/Settings.vue"
import {sleep} from "@/util.js"

const model = defineModel()
const lang = UseLang()
const maximized = ref(false)
const window_maximize_btn_swap = async ()=>{
  window.onresize()
  if(maximized.value){
    api().window.restore()
  }else{
    api().window.maximize()
  }
  maximized.value = !maximized.value
  const current_mode = model.value
  model.value = ''
  await sleep(0.8)
  model.value = current_mode
}

const refresh_env = async () => {
  window.history_idx = 0
  window.messages = null
  window.gen_messages = null
  model.value = ''
  await sleep(0.8)
  model.value = 'chat'
}

const newProject = async () => {
  if(await api().file.get_state() == 'loading'){
    try{
      ElMessageBox.confirm(
        lang.processing_exit,
        lang.warning,
        {
          confirmButtonText: lang.ok,
          cancelButtonText: lang.cancel,
          type: 'warning',
        }
      )
    }catch (e){return}
  }
  try {
    await api().file.create(
        await ElMessageBox.prompt(`${lang.project} ${lang.name}`, '', {
          confirmButtonText: lang.ok,
          cancelButtonText: lang.cancel,
        })
    )
  }catch (e){
    return
  }
  await refresh_env()
}
const open = async () => {
  if(await api().file.get_state() == 'loading'){
    try{
      ElMessageBox.confirm(
        lang.processing_exit,
        lang.warning,
        {
          confirmButtonText: lang.ok,
          cancelButtonText: lang.cancel,
          type: 'warning',
        }
      )
    }catch (e){return}
  }
  if(await api().file.open()){
    await refresh_env()
  }else{
    ElMessageBox.alert(lang.cannot_read_file, lang.warning, {confirmButtonText: lang.ok})
  }
}
const exit = async () => {
  if(await api().file.get_state() == 'loading'){
     ElMessageBox.confirm(
      lang.processing_exit,
      lang.warning,
      {
        confirmButtonText: lang.ok,
        cancelButtonText: lang.cancel,
        type: 'warning',
      }
    ).then(()=>api().exit())
  }else{
    api().exit()
  }
}

const open_setting = async () => {
  await window.open_settings()
}

</script>

<template>
  <el-menu
      :default-active="activeIndex"
      class="menu-container pywebview-drag-region"
      mode="horizontal"
      :ellipsis="false"
      @select="handleSelect"
      height="20px"
  >
    <h3 class="menu-bar-item">LLM-GUARD</h3>
    <el-sub-menu index="0">
      <template #title>{{ lang.file }}</template>
      <el-menu-item index="2-1" @click="newProject">{{ lang.new }}...</el-menu-item>
      <el-menu-item index="2-2" @click="open">{{ lang.open }}...</el-menu-item>
      <el-menu-item index="2-3" @click="api().file.save()">{{ lang.save }}...</el-menu-item>
      <el-sub-menu index="2-4" v-if="false">
        <template #title>{{ lang.recent }}</template>
        <el-menu-item>item one</el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
    <el-menu-item index="1">

    </el-menu-item>
    <settings-icon class="menu-bar-item" @click="open_setting" :style="{ fontSize: '20px' }"/>
    <window-minimize class="menu-bar-item" @click="api().window.minimize()" :style="{ fontSize: '20px' }"/>
    <component :is="maximized?WindowUnmaximize:WindowMaximize" class="menu-bar-item" @click="window_maximize_btn_swap" :style="{ fontSize: '20px' }"/>
    <window-close class="menu-bar-item" @click="exit" :style="{ fontSize: '20px' }"/>
  </el-menu>

  <settings></settings>
</template>

<style scoped>
.menu-container {
  padding: 10px;
  width: 100%;
  z-index: 100000;
}

.el-menu--horizontal > .el-menu-item:nth-child(3) {
  margin-right: auto;
}

.menu-bar-item {
  margin-top: auto;
  margin-bottom: auto;
  margin-left: 8px;
  margin-right: 8px;
}
</style>