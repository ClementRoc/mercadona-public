const $filterCheckboxes = $('input[type="checkbox"]');
const $filterPrice = $('.sort');
let $breadcrumbDisplay = $('.breadcrumb-display a')
let $articles = $('.article')
let $articlesList = []
let $filterPromo = $('input[id="promotion"]')

// Article class
function Article(name, brand, price, filters, categories) {
  this.name = name
  this.brand = brand
  this.price = price
  this.filters = filters
  this.categories = categories
}

// Fetch all articles based on the HTML
for (let i = 0; i < $articles.length; i++) {
  $articlesList.push(new Article(
      $articles[i].getAttribute('id'),
      $articles[i].getAttribute('data-name'),
      $articles[i].getAttribute('data-price'),
      $articles[i].getAttribute('data-filters'),
      $articles[i].getAttribute('data-category'),
  ))
}

// Filter function to show articles based on the checkboxes
// [Promotion, Cold, Frozen and Bio]
$filterCheckboxes.on('change', function() {
    let selectedFilters = {};

    $filterCheckboxes.filter(':checked').each(function() {
        if (!selectedFilters.hasOwnProperty(this.name)) {
            selectedFilters[this.name] = [];
        }
        selectedFilters[this.name].push(this.value);
    });

    let $filteredResults = $('.article');

    $.each(selectedFilters, function(name, filterValues) {
        $filteredResults = $filteredResults.filter(function() {
            let matched = false,
                currentFilterValues = $(this).data('filters').split(' ');
            $.each(currentFilterValues, function(_, currentFilterValue) {
                if ($.inArray(currentFilterValue, filterValues) != -1) {
                    matched = true;
                    return false;
                }
            });
        return matched;
        });
    });
    $articles.hide().filter($filteredResults).show();
});

// Filter function to show articles based on price
// [Ascending, Descending]
$filterPrice.on('change', e => {
  let value = e.target.value
  if (value === "ascending-price") {
    $articlesList.sort((a, b) => (a.price > b.price ? 1 : -1))
  } else if (value === "descending-price") {
    $articlesList.sort((a, b) => (a.price < b.price ? 1 : -1))
  } else {

  }
  $articlesList.forEach(article =>{
    document.getElementById(article.name).style.order = $articlesList.findIndex(i => i.name === article.name)
  })
})

// Show article based on the breadcrumb categories
$breadcrumbDisplay.on('click', function() {
    let $select = Array.from($('.breadcrumb-display')[0].children)
    // let $clickValue = this
    $select.splice(0,  1).join()
    $('.breadcrumb-display')[0].innerHTML = $select
    const value = document.getElementsByClassName('breadcrumb-display')[0].innerText.split('\n').join(' ')
    $articlesList.forEach(article => {
        const isVisible = article.categories.includes(value)
        document.getElementById(article.name).classList.toggle('hide', !isVisible)
    })
})

// Check if the localStorage clicked button is on true and click the promotion checkbox if true
$(document).ready(function() {
    let clicked = localStorage.getItem('click')
    let dropdownMenuHomepage = localStorage.getItem('fromHomepage')
    let anchor = localStorage.getItem('anchor')
    if (clicked === 'true'){
        $filterPromo.click()
        localStorage.setItem('click', 'false')
    }
    if (dropdownMenuHomepage === 'true'){
        let $select = $('<div class="breadcrumb-display"></div>')
        $(anchor).parents('li').each(function(n, li) {
            $select.prepend($(li).children('a').clone().removeClass())
        })
        $('.breadcrumb').html($select.prepend('<a>Catalogue</a>'))
        const value = document.getElementsByClassName('breadcrumb-display').innerText
        $articlesList.forEach(article => {
            const isVisible = article.categories.includes(value)
            document.getElementById(article.name).classList.toggle('hide', !isVisible)
        })
    }
})