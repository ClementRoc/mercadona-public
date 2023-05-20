const $dropdownButton = $('.dropdown-menu--button')
const $toggleMenuMobile = $('.js-menu-toggler')
const $dropdownMenu = $('.dropdown-menu')
const $exitDropdown = $('.exit-dropdown')
const $dropdownMenuAnchors = $('.categories a')
const $pages = $('.page')
const $searchInput = $('.input-search')
const $searchImg = $('.input-img')
let $url = location.href

// Trigger the dropdown menu
$dropdownButton.on('click', function() {
    $dropdownMenu.removeClass('hidden')
    $dropdownMenu.addClass('lazyload')
    $pages.css('filter', 'blur(0.5rem)')
})

// Shutdown the dropdown menu
$exitDropdown.on('click', function() {
    $dropdownMenu.addClass('hidden')
    $dropdownMenu.removeClass('lazyload')
    $pages.css('filter', 'unset')
})

// Shutdown the dropdown menu and put the link clicked on the breadcrumb display
// If the current page is home, you will be relocated to the catalog page
$dropdownMenuAnchors.on('click', function() {
    $dropdownMenu.addClass('hidden')
    $dropdownMenu.removeClass('lazyload')
    $pages.css('filter', 'unset')
    if ($pages.hasClass('page-home')) {
        location.assign($url + 'catalogue')
    }
    let $select = $('<div class="breadcrumb-display"></div>')
    $(this).parents('li').each(function(n, li) {
        $select.prepend($(li).children('a').clone().removeClass())
    })
    $('.breadcrumb').html($select.prepend('<a>Catalogue</a>'))
})

// Toggle the mobile hamburger menu on mobile version of the website
$toggleMenuMobile.on('click', function() {
    let togglerInner = $('#toggler')

    if ($dropdownMenu.hasClass('hidden')){
        togglerInner.removeClass('header-toggler-inner--close')
        togglerInner.addClass('header-toggler-inner--open')
        $dropdownMenu.removeClass('hidden')
        $dropdownMenu.addClass('lazyload')
    } else {
        togglerInner.removeClass('header-toggler-inner--open')
        togglerInner.addClass('header-toggler-inner--close')
        $dropdownMenu.addClass('hidden')
        $dropdownMenu.removeClass('lazyload')
    }
})

// Hide the searchbar image
$searchInput.on('click', function() {
    $searchImg.addClass('hidden')
})

// Show the searchbar image when the searchbar is unfocused and empty
$searchInput.on('blur', function() {
    if (!$searchInput[0].value){
        $searchImg.removeClass('hidden')
    }
})

// Searchbar function, it shows the result and hide the article not concerned
$searchInput.on('input', e => {
    const value = e.target.value
    $articlesList.forEach(article => {
        const isVisible = article.name.toLowerCase().includes(value.toLowerCase()) || article.brand.toLowerCase().includes(value.toLowerCase())
        document.getElementById(article.name).classList.toggle('hide', !isVisible)
    })
})