import {zh_cn} from "@/languages/zh_cn.js";
import {en} from "@/languages/en.js";
import {ElMessageBox} from "element-plus";

const lang = {
    zh_cn: new zh_cn(),
    en: new en(),
}

let language = 'zh_cn'

export function UseLang(){
    return lang[language]
}