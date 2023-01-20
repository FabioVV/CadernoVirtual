let a = document.getElementById('msg')


setTimeout(() =>{
    a.classList.add('removed')
    a.addEventListener("transitionend",() =>{
        a.remove()
    })
}, 1300)


