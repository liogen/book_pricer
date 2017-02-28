jQuery(function($) {
    $(document).ready( function() {

        function scrollToAnchor(aid){
            var aTag = $("#"+ aid);
            $('html,body').animate({scrollTop: aTag.offset().top}, 1000);
        }

        function emptyBookInfo(json_book_info) {
            console.log(json_book_info);
            if ('crawler_started' in json_book_info &&
                json_book_info['crawler_started'] === false) {
                book_title = 'book_title' in json_book_info ? json_book_info['book_title'] : null;
                book_cover_image = 'cover_image' in json_book_info ? json_book_info['cover_image'] : null;
                book_editor = 'editor' in json_book_info ? json_book_info['editor'] : null;
                book_distribution_date = 'distribution_date' in json_book_info ? json_book_info['distribution_date'] : null;
                $('#book-info-tab .section-heading').text(book_title);
                $("#book-info-tab .img-responsive").attr("src", book_cover_image);
                $("#book-info-tab .sub-title").text(book_editor + ", " + book_distribution_date);
                google.charts.setOnLoadCallback(function () {
                    console.log(json_book_info['chart_offers']);
                    drawChart(json_book_info['chart_offers']);
                });
                $("#book-info-tab").removeClass("hidden");
                $("#book-info-error").addClass("hidden");
            }
            scrollToAnchor('isbn-list');
            window.location.href = "#isbn-list";
        }

        function goToISBNList() {
            scrollToAnchor('isbn-list');
            window.location.href = "#isbn-list";
            $("#book-info").addClass("hidden");
            $("#book-info-tab").addClass("hidden");
            $("#book-info-error").addClass("hidden");
            $("#book-loading").removeClass("hidden");
        }

        function getBookInfo() {
            $("#book-loading").addClass("hidden");
            $("#book-info").removeClass("hidden");
        }

        function displayBook(json_book_info) {
            if ('crawler_started' in json_book_info &&
                json_book_info['crawler_started'] === true) {
                setTimeout(function(){
                    getISBN(json_book_info['isbn'], displayBook);
                }, 2000);
            } else {
                emptyBookInfo(json_book_info);
                setTimeout(getBookInfo, 2000);
            }
        }

        function displayError() {
            $("#book-loading").addClass("hidden");
            $("#book-info").removeClass("hidden");
            $("#book-info-error").removeClass("hidden");
        }

        function getISBN(isbn, callback) {
            var request = $.ajax({
                url: "/isbn/" + isbn + "/",
                type: "get"
            });

            request.done(function (response, textStatus, jqXHR){
                console.log("Hooray, it worked!");
                callback(response);
            });

            // Callback handler that will be called on failure
            request.fail(function (jqXHR, textStatus, errorThrown){
                // Log the error to the console
                displayError();
                console.error(
                    "The following error occurred: "+
                    textStatus, errorThrown
                );
            });
        }

        function postISBN(isbn, callback) {

            var request = $.ajax({
                url: "/",
                type: "post",
                data: {
                    'isbn': isbn,
                    csrfmiddlewaretoken: $.cookie("csrftoken")
                }
            });

            request.done(function (response, textStatus, jqXHR){
                console.log("Hooray, it worked!");
                goToISBNList();
                callback(response);
            });

            // Callback handler that will be called on failure
            request.fail(function (jqXHR, textStatus, errorThrown){
                // Log the error to the console
                console.error(
                    "The following error occurred: "+
                    textStatus, errorThrown
                );
            });
        }

        $("#isbn-submit-top").click(function(event) {
            isbn = $("#isbn-value-top").val();
            if (isbn === "") {
                return;
            }
            event.preventDefault();
            $("#isbn-value-middle").val(isbn);
            postISBN(isbn, displayBook)
        });

        $("#isbn-submit-middle").click(function(event) {
            isbn = $("#isbn-value-middle").val();
            if (isbn === "") {
                return;
            }
            event.preventDefault();
            $("#isbn-value-top").val(isbn);
            postISBN(isbn, displayBook)
        });

        $("#book-info .book-info-navbar li").click(function(event) {
            event.preventDefault();
            $("#book-info .book-info-navbar li").removeClass("active");
            $(this).addClass("active");
            if ($(this).hasClass("book-info-tab-description")) {
                $("#book-info .book-info-description").removeClass("hidden");
                $("#book-info .book-info-prices").addClass("hidden");
                $("#book-info .book-info-offers").addClass("hidden");
            } else if ($(this).hasClass("book-info-tab-prices")) {
                $("#book-info .book-info-description").addClass("hidden");
                $("#book-info .book-info-prices").removeClass("hidden");
                $("#book-info .book-info-offers").addClass("hidden");
            } else {
                $("#book-info .book-info-description").addClass("hidden");
                $("#book-info .book-info-prices").addClass("hidden");
                $("#book-info .book-info-offers").removeClass("hidden");
            }
        });

        google.charts.load("current", {packages:['corechart']});

        function drawChart(json_data) {
            console.log(json_data);
            var data = google.visualization.arrayToDataTable(json_data);

            var view = new google.visualization.DataView(data);
            view.setColumns([0, 1,
                       { calc: "stringify",
                         sourceColumn: 1,
                         type: "string",
                         role: "annotation" },
                       2]);

            var options = {
                title: "Density of Precious Metals, in g/cm^3",
                bar: {groupWidth: "95%"},
                legend: { position: "top" },
            };
            var chart = new google.visualization.ColumnChart(document.getElementById("price-chart"));
            chart.draw(view, options);
        }
    });
});