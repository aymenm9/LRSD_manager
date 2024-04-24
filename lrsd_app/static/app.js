async function get_html(url,id,args = "") {

    let response = await fetch(url+args);
    const elem = document.getElementById(id);
    elem.innerHTML = await response.text();
    console.log("qdefeefez");
}