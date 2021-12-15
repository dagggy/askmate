// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
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

    if (filterValue[0] === '!'){
        let input=filterValue.toLowerCase().slice(1);
        if (filterValue.indexOf(':') > -1){
            const fieldName = filterValue.slice(1).split(':',1)[0];
            input = input.split(':',2).slice(1)[0];
            console.log(fieldName);
            console.log(input);
            return getItemsFromFieldWithoutFilter(items, input, fieldName);
        }
        return getItemsWithoutFilter(items, input);
    } else {
        let input=filterValue.toLowerCase().slice(1);
        if (filterValue.indexOf(':') > -1){
            const fieldName = filterValue.split(':',1)[0];
            input = input.split(':',2).slice(1)[0];
            console.log(fieldName);
            console.log(input);
            return getItemsFromFieldWithFilter(items, input, fieldName);
        }
        return getItemsWithFilter(items, input);
    }
}


function getItemsWithoutFilter(items, input){
    let validItems = [];
    for (i = 0; i < items.length; i++) {
        let isValidItem = true;
        const item = items[i];
        if (item.Title.toLowerCase().indexOf(input) > -1){
            isValidItem = false;
        }
        if (item.Description.toLowerCase().indexOf(input) > -1){
            isValidItem = false;
        }
        if (item.ViewNumber.toLowerCase().indexOf(input) > -1){
            isValidItem = false;
        }
        if (item.VoteCount.toLowerCase().indexOf(input) > -1){
            isValidItem = false;
        }
        if (isValidItem) {
            validItems.push(item);
        }
    }

    return validItems;
}


function getItemsWithFilter(items, input){
    let validItems = [];
    for (i = 0; i < items.length; i++) {
        let isValidItem = false;
        const item = items[i];
        if (item.Title.toLowerCase().indexOf(input) > -1){
            isValidItem = true;
        }
        if (item.Description.toLowerCase().indexOf(input) > -1){
            isValidItem = true;
        }
        if (item.ViewNumber.toLowerCase().indexOf(input) > -1){
            isValidItem = true;
        }
        if (item.VoteCount.toLowerCase().indexOf(input) > -1){
            isValidItem = true;
        }
        if (isValidItem) {
            validItems.push(item);
        }
    }

    return validItems;
}


function getItemsFromFieldWithFilter(items, input, fieldName){
    let validItems = [];
    for (i = 0; i < items.length; i++) {
        let isValidItem = true;
        const item = items[i];
        if (item[fieldName].toLowerCase().indexOf(input) > -1){
            isValidItem = false;
        }
        if (isValidItem) {
            validItems.push(item);
        }
    }

    return validItems;
}


function getItemsFromFieldWithoutFilter(items, input, fieldName){
    let validItems = [];
    for (i = 0; i < items.length; i++) {
        let isValidItem = true;
        const item = items[i];
        if (item[fieldName].toLowerCase().indexOf(input) > -1){
            isValidItem = false;
        }
        if (isValidItem) {
            validItems.push(item);
        }
    }

    return validItems;
}


function toggleTheme() {
    console.log("toggle theme")
}

function increaseFont() {
    console.log("increaseFont")
}

function decreaseFont() {
    console.log("decreaseFont")
}
