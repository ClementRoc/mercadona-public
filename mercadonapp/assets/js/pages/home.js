const $promoBtn = $('.presentation-btn')

// Set the localStorage click on true when the homepage button is clicked
$promoBtn.on('click', function() {
    localStorage.setItem('click', 'true')
})