export function show_loading() {
    document.getElementById("loading-overlay").classList.add('active')
}

export function hide_loading() {
    document.getElementById("loading-overlay").classList.remove('active')
}