import {zh_cn} from "@/languages/zh_cn.js";
import {en} from "@/languages/en.js";
import {ElMessageBox} from "element-plus";

const lang = {
    zh_cn: new zh_cn(),
    en: new en(),
}

let language = 'zh_cn'

window.addEventListener('pywebviewready', async function () {
    const api = window.pywebview.api
    const res = await api.config.gets()
    language = res.language
    if(language==''){
        language = (await ElMessageBox.prompt(`Select your language`, 'Language', {
            inputValue: 'zh_cn',
            confirmButtonText: lang.ok,
            showCancelButton: false,
        })).value
        res.language = language
        api.config.update(res)
    }
})

export function UseLang(){
    return lang[language]
}