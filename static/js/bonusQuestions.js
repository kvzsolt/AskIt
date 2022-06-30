// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    for (let i=0; i<filterValue.length; i++) {
        items.pop()
    }

    return items
}

function toggleTheme() {
    console.log("toggle theme")
}

function increaseFontSizeBy1px() {
   let txt = document.getElementsByTagName('table')[0];
   let txt2 = document.getElementsByTagName('body')[0];

   let style = window.getComputedStyle(txt, null).getPropertyValue('font-size');
   let currentSize = parseFloat(style);
   if (currentSize <= 20){
         txt.style.fontSize = (currentSize + 1) + 'px';
         txt2.style.fontSize = (currentSize + 1) + 'px';
}

   }


function decreaseFontSizeBy1px() {
   let txt = document.getElementsByTagName('table')[0];
   let txt2 = document.getElementsByTagName('body')[0];

   let style = window.getComputedStyle(txt, null).getPropertyValue('font-size');
   let currentSize = parseFloat(style);
   if (currentSize >= 10){
       txt.style.fontSize = (currentSize - 1) + 'px';
       txt2.style.fontSize = (currentSize - 1) + 'px';}

}