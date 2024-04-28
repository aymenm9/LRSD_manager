async function get_html(url, id, args = "") {
    let response = await fetch(url + args);
    const elem = document.getElementById(id);
    elem.innerHTML = await response.text();
}
//get_html("/add_production","add_production");

get_html("/add_production","form","?p=polycopes");

const links = document.querySelectorAll(".production");
console.log("fake cs");
console.dir(links);
links.forEach(a => a.addEventListener("click", function () {
    console.log("fake cs2");
    links.forEach(an => an.classList.remove("text-primary", "active"));
    a.classList.add("text-primary", "active");
    get_html("/add_production","form","?p="+a.id);

}));


/*
get_html("/teachers", "list", "?l=3");
const all = document.getElementById("all");
all.addEventListener("click", function () {
    if (all.innerText == "view all") {
        all.innerText = "view less";
        get_html("/teachers", "list");
        }
        else {
        all.innerText = "view all";
        get_html("/teachers", "list", "?l=3");
            }
        });
const searchBtn = document.getElementById("search_btn");
const searchInp = document.getElementById("search");
[searchBtn, searchInp].forEach(search => search.addEventListener("input", function () {
    get_html("/teachers", "list", "?q=" + search.value);
    all.innerText = "Cancel";
    }));
*/ 