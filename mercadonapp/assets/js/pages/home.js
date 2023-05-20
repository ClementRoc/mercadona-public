const $promoBtn = $('.presentation-btn')
const $filterPromo = $('input[id="promotion"]')[0]

// Homepage promo button, get you to catalog page and check Promotion.
$promoBtn.on('click', function() {
    $filterPromo.checked = true
})