lizMap.events.on({
    'uicreated': function(e) {
        let selection = $('#print-scale')
        $("#print-scale option[value='55000']").remove();
        $("#print-scale option[value='100000']").remove();
        $("#print-scale option[value='150000']").remove();
        //selection.append(`<option value="100000">100000</option>`);
        //selection.append(`<option value="150000">150000</option>`);


    }
});