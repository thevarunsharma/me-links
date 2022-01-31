$(document).ready(function() {
    $('#add_form').hide()

    $("#show_add").click(function() {
        if ($('#show_add').html() == '+') {
            $('#show_add').html('-')
            $('#add_form').fadeIn()
        } else {
            $('#show_add').html('+')
            $('#add_form').fadeOut()
        }
    })

    $('#search_box').keypress(function(e) {
        if (e.which == 13) { //Enter key pressed
            search()
        }
    });

})

function save() {
    key = $("#key").val()
    link = $("#link").val()
    has_query = $("#has_query").is(":checked")

    data = {
        'key': key,
        'link': link,
        'has_query': has_query
    }

    if (key.indexOf(' ') >= 0) {
        alert("Key shouldn't have any whitespaces")
        return;
    }

    $.ajaxSetup({ async: false })
    var ok = true
    $.get('/check', { 'key': key }, function(data) {
        if (data.isKey) {
            ok = confirm(`${key} is already present in database, do you want to edit?`)
            console.log(ok)
        }
    })
    console.log(ok)
    if (!ok)
        return

    $.post('/save', data, function() {
        key = $("#key").val()
        $("#key").val("")
        $("#link").val("")
        $("#has_query").prop('checked', false)
        alert(`${key} added to database`)
    }).fail(
        function(event) {
            alert('Some error occured, check the inputs and try again')
        }
    )
}

function search() {
    const keyword = $("#search_box").val()

    $.get("/search", { "query": keyword }, function(data) {
        result_box = $('#search_results')
        if (data.status == 'INVALID')
            alert("Invalid search keyword")
        else if (data.status == 'NOT FOUND')
            result_box.html(`<em>No result found for ${keyword}</em>`)
        else {
            rows = `<tr>
            <th></th>
            <th>KEY</th>
            <th>URL</th>
            <th></th>
            </tr>`
            results = data.data
            for (i = 0; i < results.length; i++) {
                row = `<tr>
                    <td style="width: 5px;">me/</td>
                    <td>${results[i][0]}</td>
                    <td><a href='${results[i][1][0]}'>${results[i][1][0]}</a></td>
                    <td><button class="deletebutton" onclick="deleteKey('${results[i][0]}')">Delete</button></td>
                </tr>`
                rows += row
            }
            result_box.html(
                `<table>
                ${rows}
                </table>`
            )
        }
    })
}

function deleteKey(key) {
    if (!confirm(`Are you sure you want to delete ${key}?`))
        return;
    $.post('/delete', { 'key': key }, function() {
        alert(`${key} popped from database`)
        search()
    }).fail(
        function(event) {
            alert("Couldn't delete invalid or non-existent key")
        }
    )
}

function closeBanner() {
    $("#banner").hide();
}
