let a = document.getElementById('msg')


setTimeout(() =>{
    a.classList.add('removed')
    a.addEventListener("transitionend",() =>{
        a.remove()
    })
}, 1300)





// Get the button that toggles the dark mode
const toggleButton = document.getElementById("toggle-button");


const body = document.body;
const div = document.querySelectorAll('div')


// Add an event listener to the toggle button that switches the body's class
toggleButton.addEventListener("click", function() {
  if (body.classList.contains("dark-mode")) {

    body.classList.remove("dark-mode");
    

  } else {
    body.classList.add("dark-mode");
    

  }

  div.forEach(e => {
    if (e.classList.contains("dark-mode")){
        e.classList.remove("dark-mode")
    } else{
        e.classList.add("dark-mode")
    }
  });

});
