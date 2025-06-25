<script setup>
import Folder from "@/assets/icons/Folder.vue";
import Chat from "@/assets/icons/Chat.vue";
import Tool from "@/assets/icons/Tool.vue";
import {UseLang} from "@/languages/language.js";
const lang = UseLang()
const workspace = defineModel()

const update = async (mode) => {
  if ('generating' in window && window.generating){
    try{
       await ElMessageBox.confirm(lang.is_generating, lang.warning, {
        confirmButtonText: lang.ignore,
        cancelButtonText: lang.cancel,
      })
    }catch (e){
      return
    }
    window.generating = false
  }
  if (workspace.value != 'none' && workspace.value != 'new')
    workspace.value = mode
}
</script>

<template>
<div class="box-radius side-bar">
    <el-row class="menu-button">
      <Chat class="menu-bar-button"
            @click="update('chat')"
            :color="workspace=='chat'?'var(--el-color-primary)':'black'"
            :style="{ fontSize: '25px' }" />
    </el-row>
    <el-row class="menu-button">
      <folder class="menu-bar-button"
            @click="update('file')"
            :color="workspace=='file'?'var(--el-color-primary)':'black'"
            :style="{ fontSize: '25px' }" />
    </el-row>
    <el-row class="menu-button">
      <tool class="menu-bar-button"
            @click="update('strategy')"
            :color="workspace=='strategy'?'var(--el-color-primary)':'black'"
            :style="{ fontSize: '25px' }" />
    </el-row>
  </div>
</template>

<style scoped>
.menu-button {
  margin: 15px;
}

.side-bar {
  position: fixed;
  top: 50%;
  margin-left: 10px;
  transform: translate(0%, -50%);
}

</style>