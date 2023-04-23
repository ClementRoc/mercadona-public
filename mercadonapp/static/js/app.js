
const $filterCheckboxes = $(".checkbox-filter")
const $article = $(".article")

$filterCheckboxes.on("change", function () {
    let selectedFilters = {};

    $filterCheckboxes.filter(":checked").each(function () {
        if (!selectedFilters.hasOwnProperty(this.name)) {
            selectedFilters[this.name] = [];
        }
        selectedFilters[this.name].push(this.value);
    });

    let $filteredResults = $article;

    $.each(selectedFilters, function (name, filterValues) {
        $filteredResults = $filteredResults.filter(function () {
            let matched = false,
                currentFilterValues = $(this).data("category").split(" ");

            $.each(currentFilterValues, function (_, currentFilterValue) {
                if ($.inArray(currentFilterValue, filterValues) != -1) {
                    matched = true;
                    return false;
                }
            });

            return matched;
        });
    });

    $article
        .addClass("hidden")
        .filter($filteredResults)
        .removeClass("hidden");
});