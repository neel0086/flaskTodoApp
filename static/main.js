var sub = document.getElementById('addtask')

var sbutton = sub.querySelector('.submit-op')
var att = sub.getAttribute('data')
console.log(att)
sbutton.addEventListener('click',(e) =>{
    
    e.preventDefault()
    var data = new FormData(document.getElementById("addtask"));
    fetch(`/${att}/home`, { method: "post", body: data });
    location.reload()
})

