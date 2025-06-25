<script setup>
import {UseLang} from "@/languages/language.js";
import {ref} from 'vue';

const {options, select} = defineProps(['options', 'select'])
const lang = UseLang()
const content = defineModel()
const input_el = ref()

window.content = content
</script>
<template>
  <div class="input-box box-radius" ref="input_el">
    <el-mention
      class="input-box-inside"
      v-model="content"
      resize="none"
      @select="select"
      :options="options"
      whole
      :autosize="{ minRows: 2, maxRows: 8 }"
      type="textarea"
      :placeholder="lang.input_placeholder"
      spellcheck="false"
    />
    <slot></slot>
  </div>
</template>

<style scoped>

.input-box-inside {
  background-color: transparent;
}

.input-box-inside > textarea {
  width: 100%;
  border: none;
  resize: none;
  outline: none;
  background-color: transparent;
}

.input-box {
  width: 70%;
  min-width: 360px;
  min-height: 50px;
  margin-left: auto;
  margin-right: auto;
  margin-top: auto;
  margin-bottom: 10px;
  z-index: 999;
  background-color: white;
  padding: 10px;
}

</style>

<style>

.el-textarea__inner {
  --el-border-color: transparent;
  --el-input-hover-border: transparent;
  --el-input-focus-border: transparent;
  --el-input-focus-border-color: transparent;
  --el-input-hover-border-color: transparent;
  box-shadow: none;
}

</style>