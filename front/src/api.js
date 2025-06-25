import {h, ref} from "vue";
import {ElMessageBox}  from "element-plus";
import {sleep, wait_until} from "@/util.js";
import {UseLang} from "@/languages/language.js";

const lang = UseLang()

let api_obj = null
window.addEventListener('pywebviewready', function () {
    api_obj = window.pywebview.api
})

export function api() {
    return api_obj
}

export async function download_model(default_model) {
    try {
        const res = await ElMessageBox.prompt(`${lang.download} ${lang.model}`, lang.download, {
            inputValue: default_model,
            confirmButtonText: lang.ok,
            cancelButtonText: lang.cancel,
        })
        const process = ref(lang.wait_to_start)
        const process_el = ref()
        ElMessageBox({
            title: lang.wait,
            message: () => h('p', null, [
                h('span', null, lang.process + ': '),
                h('span', {ref: process_el}, process.value),
            ]),
            showCancelButton: false,
            beforeClose: (action, instance, done) => {
                if (process.value == 'done')
                    done()
            },
        })
        api().llm.pull(res.value).then(async res => {
            if (res != 'complete') {
                ElMessageBox.alert(res, lang.please_reboot, {
                    confirmButtonText: lang.ok,
                })
                await sleep(2)
                api().exit()
            }
        })
        await wait_until(async () => {
            process.value = await api().llm.get_state()
            process_el.value.innerText = process.value
            return process.value == 'done'
        }, 1)
        await ElMessageBox.alert(lang.finish, '', {
            confirmButtonText: lang.ok,
        })
        return res.value
    } catch (e) {}
}
