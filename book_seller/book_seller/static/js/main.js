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
                $("#book-info-tab").removeClass("hidden");
                $("#book-info-error").addClass("hidden");
            }
            $("#book-info").addClass("hidden");
            $("#book-loading").removeClass("hidden");
            scrollToAnchor('isbn-list');
            window.location.href = "#isbn-list";
        }

        function goToISBNList() {
            scrollToAnchor('isbn-list');
            window.location.href = "#isbn-list";
        }

        function getBookInfo() {
            $("#book-loading").addClass("hidden");
            $("#book-info").removeClass("hidden");
        }

        function displayBook(json_book_info) {
            emptyBookInfo(json_book_info);
            goToISBNList();
            setTimeout(getBookInfo, 2000);
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

            // Callback handler that will be called regardless
            // if the request failed or succeeded
            request.always(function () {
                // Reenable the inputs
            });
        }

        console.log('Here')

        $(".isbn-submit").click(function(event) {
            console.log('Here2')
            isbn = $("#isbn-value").val();
            if (isbn === "") {
                return;
            }
            event.preventDefault();
            console.log(isbn);
            postISBN(isbn, displayBook)
        });
    });
});