$(document).ready(function () {
    let sortBy = null;
    let sortDescending = false;

    $(".sort-btn").on("click", function () {
        const newSortBy = $(this).data("sort");

        if (sortBy === newSortBy) {
            sortDescending = !sortDescending;
        } else {
            sortDescending = false;
            sortBy = newSortBy;
        }

        sortStories(sortBy, sortDescending);
    });

    function sortStories(sortBy, descending) {
        const storyList = $("#story-list");
        const storyItems = storyList.find(".story-item");

        storyItems.sort(function (a, b) {
            const aValue = $(a).find("." + sortBy).text();
            const bValue = $(b).find("." + sortBy).text();

            // Convert to numbers for numeric sorting
            const aNumber = parseFloat(aValue.replace(/[^\d.-]/g, ""));
            const bNumber = parseFloat(bValue.replace(/[^\d.-]/g, ""));

            if (!isNaN(aNumber) && !isNaN(bNumber)) {
                if (descending) {
                    return bNumber - aNumber;
                }
                return aNumber - bNumber;
            }

            if (descending) {
                return bValue.localeCompare(aValue);
            }
            return aValue.localeCompare(bValue);
        });

        storyList.empty().append(storyItems);
    }
});
