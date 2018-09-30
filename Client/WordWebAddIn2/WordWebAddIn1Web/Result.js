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

            $('#rec_button').click(recommendSentence);

            $('#hist_button').click(showHistory);
        });
    };

    function sendToGoogle(dragged) {
        $('#r_google').html('<h3>Google</h3><ul></ul>');
        var myUrl = 'https://translation.googleapis.com/language/translate/v2';
        //  But if you make it from a browser, then it will work without problem ...

        //// However to make it work, we are going to use the cors-anywhere free service to bypass this
        var proxy = 'https://cors-anywhere.herokuapp.com/';

        // Execute request
        var xmlhttp = new XMLHttpRequest();

        // Or post, etc
        xmlhttp.open("GET", proxy + myUrl + '?key=k&q=' + dragged + '&source=en&target=ko&format=text', true);

        xmlhttp.send();

        xmlhttp.onload = function () {
            // do something to response
            //console.log(this.responseText);

            var jsonData = JSON.parse(this.responseText);
            console.log(jsonData["data"]["translations"]);
            for (var i = 0; i < jsonData["data"]["translations"].length; i++) {
                var word = jsonData["data"]["translations"][i]["translatedText"];
                console.log("##########");
                console.log(word);
                console.log("##########");
                $('#r_google ul').append("<li><label id = label" + i + ">" + word + '</label></li>');
            }

        };
    }

    function sendToNaver(dragged) {
        $('#r_naver').html('<h3>Naver</h3><ul></ul>');

        var client_id = 'k';
        var client_secret = 'k';

        var query = dragged;

        var myUrl = 'https://openapi.naver.com/v1/papago/n2mt';
        //  But if you make it from a browser, then it will work without problem ...

        //// However to make it work, we are going to use the cors-anywhere free service to bypass this
        var proxy = 'https://cors-anywhere.herokuapp.com/';

        // Execute request
        var xmlhttp = new XMLHttpRequest();

        // Or post, etc
        xmlhttp.open("POST", proxy + myUrl);
        xmlhttp.setRequestHeader('Access-Control-Allow-Origin', '*');
        xmlhttp.setRequestHeader('X-Requested-With', 'xmlhttprequest');
        xmlhttp.setRequestHeader('Content-Type', 'application/json');
        xmlhttp.setRequestHeader('X-Naver-Client-Id', client_id);
        xmlhttp.setRequestHeader('X-Naver-Client-Secret', client_secret);

        var jsonRequest = { source: 'en', target: 'ko', text: query };

        xmlhttp.send(JSON.stringify(jsonRequest));

        xmlhttp.onload = function () {
            // do something to response
            //console.log(this.responseText);
            
            var jsonData = JSON.parse(this.responseText);
            console.log(jsonData["message"]["result"]["translatedText"]);
            //for (var i = 0; i < jsonData["message"]["result"].length; i++) {
            //    var word = jsonData["data"]["translations"][i]["translatedText"];
            //    console.log("##########");
            //    console.log(word);
            //    console.log("##########");
            //    $('#r_naver ul').append("<li><label id = label" + i + ">" + word + '</label></li>');
            //}
            var word = jsonData["message"]["result"]["translatedText"];
            $('#r_naver ul').append("<li><label>" + word + '</label></li>');

        };
    }

    function sendToServer(dragged, whole_text) {
        $('#r_result').html('<h3>Naver</h3><ul></ul>');
        var myUrl = 'http://52.79.106.90:5000/dev/data';
        //  But if you make it from a browser, then it will work without problem ...

        // However to make it work, we are going to use the cors-anywhere free service to bypass this
        var proxy = 'https://cors-anywhere.herokuapp.com/';

        // Execute request
        var xmlhttp = new XMLHttpRequest();

        // Or post, etc
        xmlhttp.open("POST", proxy + myUrl, true);
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        console.log(JSON.stringify({ full_sentence: whole_text, target: "<31fe0826-7bb3-444d-8f2e-6ca06ae24e11>" + dragged }));
        xmlhttp.send(JSON.stringify({ full_sentence: whole_text, target: "<31fe0826-7bb3-444d-8f2e-6ca06ae24e11>" + dragged}));
        //xmlhttp.send(sentnece);
        xmlhttp.onload = function () {
            // do something to response
            //console.log(JSON.parse(this.responseText)["result"][0]["target"]["word"]);

            var jsonData = JSON.parse(this.responseText);

            var count = 0;

            for (var i = 0; i < jsonData["result"].length; i++) {
                var word = jsonData["result"][i]["target"]["word"];
                console.log(word);
                $('#r_result ul').append("<li><button type='button' class='btn btn-primary' id = button" + i + ">" + word + '</button></li>');

                $("#button" + i).on("click", { word: word }, changeWord);
                count++;
            }

            for (var i = 0; i < jsonData["word2vec"].length; i++) {
                var word = jsonData["word2vec"][i]["word"];
                console.log(word);
                $('#r_result ul').append("<li><button type='button' class='btn btn-primary' id = button" + (i + count) + ">" + word + '</button></li>');

                $("#button" + (i + count)).on("click", { word: word }, changeWord);
            }
            
        };
    }

    function changeWord(event) {
        Word.run(function (context) {
            
            context.document.getSelection().clear();
            context.document.getSelection().insertText(event.data.word, 'Start');
            // 범위 선택 결과를 로드하는 명령을 큐에 넣습니다.

            return context.sync()
                .then(function () {

                });

        })
        .catch(errorHandler);
    }

    function back() {
        document.location.href = "Main.html";
    }

    function tmp() {
        Word.run(function (context) {

            //var para = context.document.getSelection().paragraphs;
            //para.load();

            var documentBody = context.document.body;

            context.load(documentBody, 'text');

            //documentBody.clear();
            return context.sync()
                .then(function () {
                    console.log("11111111111111");
                    console.log(documentBody.text);
                    return documentBody.text;

                });

        })
        .catch(errorHandler);
    }

    function vocabHistory(text) {
        $('#history_main').append("<div><ul><li>" + text + " : " + "</div></li></ul>");
    }

    function showHistory() {
        Word.run(function (context) {


            return context.sync()
                .then(function () {
                    $('.vocab_history').css("display", "block");

                });

        })
        .catch(errorHandler);
        
    }

    function noHistory() {
        $('.vocab_history').css("display", "none");
    }

    function recommendSentence() {

        Word.run(function (context) {

            noHistory();
            
            var documentBody = context.document.body;

            var dragged = context.document.getSelection();
            
            context.load(dragged, 'text');
            
            context.document.getSelection().insertText("<31fe0826-7bb3-444d-8f2e-6ca06ae24e11>", 'Start');

            context.load(documentBody, 'text');

            context.document.getSelection().clear();
            //documentBody.insertText(original, 'Start');
            
            //documentBody.clear();

            return context.sync()
                .then(function () {
                    //sendToServer(dragged.text, documentBody.text);
                    //sendToGoogle(dragged.text);
                    sendToNaver(dragged.text);
                    vocabHistory(dragged.text);
                    
                    //writeFile("text.txt", dragged.text);
                    //console.log(para.items[0].clear());
                    context.document.getSelection().insertText(dragged.text, 'Start');
                    
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
