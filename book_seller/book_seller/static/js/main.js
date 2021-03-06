jQuery(function($) {
    $(document).ready( function() {

        function scrollToAnchor(aid){
            var aTag = $("#"+ aid);
            $('html,body').animate({scrollTop: aTag.offset().top}, 1000);
        }

        function emptyBookInfo(json_book_info) {
            if ('crawler_started' in json_book_info &&
                json_book_info['crawler_started'] === false) {
                book_title = 'book_title' in json_book_info ? json_book_info['book_title'] : null;
                book_cover_image = 'cover_image' in json_book_info ? json_book_info['cover_image'] : null;
                book_editor = 'editor' in json_book_info ? json_book_info['editor'] : null;
                book_distribution_date = 'distribution_date' in json_book_info ? json_book_info['distribution_date'] : null;
                book_median_prices = 'median_offers' in json_book_info ? json_book_info['median_offers'] : null;
                offers_number = 'total_offer_nb' in json_book_info ? json_book_info['total_offer_nb'] : null;
                lowest_new_price = 'lowest_new_price' in json_book_info ? json_book_info['lowest_new_price'] : null;
                lowest_used_price = 'lowest_used_price' in json_book_info ? json_book_info['lowest_used_price'] : null;
                $('#book-info-tab .book_title').text(book_title);
                $("#book-info-tab .img-responsive").attr("src", book_cover_image);
                $("#book-info-tab .book_editor").text(book_editor + ", " + book_distribution_date);
                $("#book-info-tab .median_price span").text(book_median_prices);
                $("#book-info-tab .offers_number span").text(offers_number);
                $("#book-info-tab .lowest_new_price span").text(lowest_new_price);
                $("#book-info-tab .lowest_used_price span").text(lowest_used_price);
                $("#book-info-tab").removeClass("hidden");
                $("#book-offers-tab").removeClass("hidden");
                $("#book-info-error").addClass("hidden");
                google.charts.load('current', {'packages':['bar'], callback: function () {
                    drawChart(json_book_info['chart_offers']);
                }});
            }
        }

        function goToISBNList() {
            scrollToAnchor('isbn-list');
            window.location.href = "#isbn-list";
            $("#price_chart div").empty();;
            $("#book-info").addClass("hidden");
            $("#book-info-tab").addClass("hidden");
            $("#book-offers-tab").addClass("hidden");
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

        function isbnSubmitBehavior(origin, target) {
            isbn = $(origin).val();
            if (isbn === "") {
                return;
            }
            $(target).val(isbn);
            postISBN(isbn, displayBook)
        }

        $("#isbn-submit-top").click(function(event) {
            event.preventDefault();
            isbnSubmitBehavior("#isbn-value-top", "#isbn-value-middle")
        });

        $("#isbn-submit-middle").click(function(event) {
            event.preventDefault();
            isbnSubmitBehavior("#isbn-value-middle", "#isbn-value-top")
        });

        function drawChart(json_data) {
            var data = google.visualization.arrayToDataTable(json_data);

            var options = {
                chart: {
                    title: 'Distribution of new and used offers',
                }
            };

            var chart = new google.charts.Bar(document.getElementById("price_chart"));

            chart.draw(data, options);
        }
    });
});