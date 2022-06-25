var sub1 = document.getElementById('algin-form')
console.log(sub1)
var sbutton1 = sub1.querySelector('.btn')
var att = sub1.getAttribute('data')

sbutton1.addEventListener('click',(e) =>{
    e.preventDefault()
    var data = new FormData(document.getElementById("algin-form"));
    fetch(`/comment/${att}`, { method: "post", body: data });
    location.reload()
})