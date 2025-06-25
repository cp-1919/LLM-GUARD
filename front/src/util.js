export function sleep(second){
    return new Promise(resolve => setTimeout(resolve, second*1000))
}

export function wait_until(func, second) {
    return new Promise(resolve => {
        const interval = setInterval(
            async ()=>{
                if(await func()){
                    clearInterval(interval)
                    resolve()
                }
            },
            second*1000
        )
    })
}

const resize_events = []
window.onresize = ()=>{
    for(let i of resize_events)i(window.innerWidth, window.innerHeight)
}
export function window_resize(func){
    resize_events.push(func)
    func(window.innerWidth, window.innerHeight)
}