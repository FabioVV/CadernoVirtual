let a = document.getElementById('msg')


setTimeout(() =>{
    a.classList.add('removed')
    a.addEventListener("transitionend",() =>{
        a.remove()
    })
}, 1300)


let input = document.querySelector('#te')
  input.addEventListener('input', async function(){
    let response = await fetch('/searchh?q=' + input.value)
    let shows = await response.json()
    let html = ''
    for(let x in shows){
      let title = shows[x].title.replace('<', '&lt;')
      html += '<li>' + title + '</li>'
    }
    document.querySelector('ul').innerHTML = html
  })