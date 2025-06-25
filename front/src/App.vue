<template>
  <div class="full-container">
    <div class="full-container">
      <div class="auto-fixed-container">
        <menu-bar v-model="workspace"></menu-bar>
      </div>
      <div class="auto-follow-container">
        <transition class="full-container" name="el-fade-in-linear" mode="out-in">
            <div class="transition-box" v-if="workspace=='file'"><file-manager></file-manager></div>
            <div class="transition-box" v-else-if="workspace=='strategy'"><strategy-manager></strategy-manager></div>
            <div class="transition-box" v-else-if="workspace=='chat'"><chat></chat></div>
            <div class="transition-box" :style="{height:infer_height+'px', position: 'relative'}" v-else-if="workspace=='none'">
              <el-result class="vertical_middle" icon="info" :title="lang.welcome">
                <template #sub-title>
                  <p>{{lang.open}} {{lang.or}} {{lang.create}} {{lang.project}}</p>
                </template>
                <template #extra>
                  <el-button type="primary" @click="openProject">{{ lang.open }} {{ lang.project }}</el-button>
                  <el-button type="primary" @click="newProject">{{ lang.new }} {{ lang.project }}</el-button>
                </template>
              </el-result>
            </div>
            <div class="transition-box" :style="{height:infer_height+'px', position:'relative'}" v-else-if="workspace=='new'">
              <el-result class="vertical_middle" icon="warning" :title="lang.welcome">
                <template #sub-title>
                  <p>{{ lang.unconfigured_notice }}</p>
                </template>
                <template #extra>
                  <el-button type="primary" @click="configure">{{ lang.configure }} LLM-GURAD</el-button>
                </template>
              </el-result>
            </div>
        </transition>
      </div>
    </div>
  </div>

  <side-bar v-model="workspace"></side-bar>


</template>

<script setup>
import { ref } from 'vue'
import MenuBar from '@/components/MenuBar.vue'
import StrategyManager from "@/components/StrategyManager.vue"
import FileManager from "@/components/FileManager.vue"
import Chat from "@/components/Chat.vue"
import SideBar from "@/components/SideBar.vue"
import {api} from "@/api.js";
import {sleep, window_resize} from "@/util.js";
import {UseLang} from "@/languages/language.js";

const workspace = ref('');
const lang = UseLang();
const infer_height = ref(0);

(async () => {
  await sleep(0.8)
  console.log(api())
  if(await api().is_new()){
    workspace.value = 'new'
  }else{
    workspace.value = 'none'
  }
})()

window_resize((w,h)=>{
  infer_height.value = h-200
})

const configure = async () => {
  await window.open_settings();
  workspace.value = 'none'
}

const newProject = async () => {
  try {
    await api().file.create(
        await ElMessageBox.prompt(`${lang.project} ${lang.name}`, '', {
          confirmButtonText: lang.ok,
          cancelButtonText: lang.cancel,
        })
    )
    workspace.value = 'chat'
  }catch (e){}
}

const openProject = async () => {
  if(await api().file.open()){
    workspace.value = 'chat'
  }else{
    ElMessageBox.alert(lang.cannot_read_file, lang.warning, {confirmButtonText: lang.ok})
  }
}
</script>
<style scoped>
</style>