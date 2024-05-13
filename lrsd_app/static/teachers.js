async function get_html(url, id, args = "") {
    let response = await fetch(url + args);
    const elem = document.getElementById(id);
    elem.innerHTML = await response.text();
    $(document).ready(function() {
        $('#tablelist').DataTable({
            "pageLength": 5
        });
    });
}
get_html("/teachers","list");
