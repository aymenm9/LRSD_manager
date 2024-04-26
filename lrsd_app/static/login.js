const btns =document.getElementsByName("btnradio");
const adminForm = document.getElementById("admin");
const teacherFrom = document.getElementById("teacher");

btns.forEach(btn => {
    btn.addEventListener("change", function(){
        if (btn.checked){
            if (btn.value == "admin"){
                    teacherFrom.classList.remove("d-block");
                    teacherFrom.classList.add("d-none");
                    adminForm.classList.remove("d-none");
                    adminForm.classList.add("d-block");
            }
            else{
                adminForm.classList.remove("d-block");
                adminForm.classList.add("d-none");
                teacherFrom.classList.remove("d-none");
                teacherFrom.classList.add("d-block");
            }
        }
    })
});