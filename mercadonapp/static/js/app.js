const searchInput = document.querySelector('.input-search')

searchInput.addEventListener('input', (e) =>{
    let value = e.target.value

    if (value && value.trim().length > 0){
        value = value.trim().toLowerCase()
    } else{

    }
})

