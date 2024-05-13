async function get_html(url, id, args = "") {
    let response = await fetch(url + args);
    const elem = document.getElementById(id);
    elem.innerHTML = await response.text();
}

get_html("/add_production","form","?p=polycopes");

function tab(){
    get_html("/productions","production_list").then(() => {
    $(document).ready(function() {
        $('#productions_table').DataTable({
            "pageLength": 5
        });
    });
    var edit = document.querySelectorAll(".edit_production");
    var editBtn = document.querySelectorAll(".btn-edit-production");
    editBtn.forEach(element => {
        element.addEventListener("click", function(){
            let delement = document.getElementById(element.classList[3]);
            get_html("/edit_production",delement.id,"?p="+delement.classList[1]+"&id="+delement.classList[2]);
        }) 
    });
    });
}

tab();

const links = document.querySelectorAll(".production");

links.forEach(a => a.addEventListener("click", function () {
    links.forEach(an => an.classList.remove("text-primary", "active"));
    a.classList.add("text-primary", "active");
    get_html("/add_production","form","?p="+a.id);

}));
