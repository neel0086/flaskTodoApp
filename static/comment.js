var sub1 = document.getElementById('algin-form')
console.log(sub1)
var sbutton1 = sub1.querySelector('.btn')
var att = sub1.getAttribute('data')
var att1 = sub1.getAttribute('data1')
console.log(att,att1)
sbutton1.addEventListener('click',(e) =>{
    e.preventDefault()
    var data = new FormData(document.getElementById("algin-form"));
    fetch(`/${att}/comment/${att1}`, { method: "post", body: data });
    location.reload()
})