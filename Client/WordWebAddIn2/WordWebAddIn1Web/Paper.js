(function () {

    "use strict";
    var messageBanner;

    // 새 페이지가 로드될 때마다 초기화 함수가 실행되어야 합니다.
    Office.initialize = function (reason) {
        $(document).ready(function () {

            // Word 2016을 사용하지 않는 경우 대체 논리를 사용합니다.
            if (!Office.context.requirements.isSetSupported('WordApi', '1.1')) {
                //채워야함.
                return;
            }


            receivePapers();
        });
    };

    function receivePapers() {
        Word.run(function (context) {
            
            var whole_text = context.document.body;

            context.load(whole_text, 'text');

            $('#r_result').html("");

            return context.sync()
                .then(function () {

                    console.log("1111");
                    var myUrl = 'http://mpbear11.duckdns.org:5000/papers';
                    //  But if you make it from a browser, then it will work without problem ...

                    // However to make it work, we are going to use the cors-anywhere free service to bypass this
                    var proxy = 'https://cors-anywhere.herokuapp.com/';

                    // Execute request
                    var xmlhttp = new XMLHttpRequest();

                    // Or post, etc
                    xmlhttp.open("POST", proxy + myUrl);
                    xmlhttp.setRequestHeader("Content-Type", "application/json");
                    xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");

                    console.log(JSON.stringify({ doc: whole_text.text }));
                    xmlhttp.send(JSON.stringify({ doc: whole_text.text }));

                    xmlhttp.onload = function () {
                        // do something to response
                        //console.log(JSON.parse(this.responseText)["result"][0]["target"]["word"]);

                        console.log("222");
                        console.log(this.responseText);
                        var jsonData = JSON.parse(this.responseText);
                        console.log(jsonData["result"]);
                        for (var i = 0; i < jsonData["result"].length; i++) {
                            
                            var title = jsonData["result"][i]["title"];
                            var link = jsonData["result"][i]["file_link"];
                            var author = jsonData["result"][i]["author_list"][0]["name"];
                            var quotation = jsonData["result"][i]["quotation"];;
                            $('#r_result').append("<div><ul><li> 논문 제목 : " + title + '</br>저자 : ' + author + '</br>링크 : <a href="' + link + '">' + link +'</a></br>인용횟수 : ' + quotation +'</div></li></ul>');
                        }

                    };
                });
        })
       .catch(errorHandler);
    }


    //$$(Helper function for treating errors, $loc_script_taskpane_home_js_comment34$)$$
    function errorHandler(error) {
        // $$(Always be sure to catch any accumulated errors that bubble up from the Word.run execution., $loc_script_taskpane_home_js_comment35$)$$
        showNotification("오류:", error);
        console.log("Error: " + error);
        if (error instanceof OfficeExtension.Error) {
            console.log("Debug info: " + JSON.stringify(error.debugInfo));
        }
    }

    // 알림 표시를 위한 도우미 함수입니다.
    function showNotification(header, content) {
        $("#notificationHeader").text(header);
        $("#notificationBody").text(content);
        messageBanner.showBanner();
        messageBanner.toggleExpansion();
    }
})();