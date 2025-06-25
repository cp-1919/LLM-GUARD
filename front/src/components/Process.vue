<script setup>
import {ref, onMounted} from 'vue';
import {UseLang} from "@/languages/language.js";
import {api} from "@/api.js";
import {ElMessageBox} from "element-plus";

const mode = defineModel()
const {strategy} = defineProps(['strategy']);

const lang = UseLang();

const selected_file = ref([]);
const file_list = ref([]);
const name_template = ref('')
const replace_file = ref(false)

const onSubmit = async () => {
  if(!name_template.value.includes('{}')){
    await ElMessageBox.alert(lang.illegal_template, lang.warning)
    return
  }
  if(replace_file.value){
    name_template.value = '{}'
  }
  api().llm.process_files(selected_file.value, strategy, name_template.value)
  mode.value = 'processing'
}

onMounted(async () =>  {
  file_list.value = await api().file.list()
  name_template.value = strategy + '_' + '{}'
})
</script>

<template>
  <div class="file-selector-container workspace-container">
    <el-transfer
      v-model="selected_file"
      filterable
      :filter-placeholder="lang.search"
      :data="file_list"
      :titles="[`${lang.alternative} ${lang.file}`, `${lang.selected} ${lang.file}`]"
      :button-texts="[lang.undo, lang.select]"
      :props="{
        key: 'name',
        label: 'name',
      }"
    />
    <br>
    <el-divider content-position="left">{{`${lang.file}${lang.name} ${lang.template}`}}</el-divider>
    <el-input
      v-model="name_template"
      :placeholder="lang.template"
    />
    <h5>
      {{lang.replace_original_file}} <el-switch v-model="replace_file"/>
    </h5>

    <el-button class="mt-4" style="width: 100%" @click="onSubmit">
      {{ `${lang.start} ${lang.generate}` }}
    </el-button>
  </div>
</template>

<style scoped>
.file-selector-container {
  width: 620px;
  align-items: center;
}
</style>