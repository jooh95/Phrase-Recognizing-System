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
            $('#paper_button').click(recommendPaper);
            $('#hist_button').click(showHistory);
        });
    };

    function recommendPaper() {
        document.location.href = "Paper.html";
    }

    function sendToGoogle(dragged) {
        $('#r_google').html('<h3>Google</h3><ul></ul>');
        var myUrl = 'https://translation.googleapis.com/language/translate/v2';
        //  But if you make it from a browser, then it will work without problem ...

        //// However to make it work, we are going to use the cors-anywhere free service to bypass this
        var proxy = 'https://cors-anywhere.herokuapp.com/';

        // Execute request
        var xmlhttp = new XMLHttpRequest();

        // Or post, etc
        xmlhttp.open("GET", proxy + myUrl + '?key=apikey&q=' + dragged + '&source=en&target=ko&format=text', true);
        xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
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
        $('#r_naver').html('<h3>Kakao</h3><ul></ul>');

        var client_id = 'apikey';
        //var client_secret = '1IjcbfdwKl';

        var myUrl = "https://kapi.kakao.com/v1/translation/translate";
        //  But if you make it from a browser, then it will work without problem ...

        //// However to make it work, we are going to use the cors-anywhere free service to bypass this
        var proxy = "https://cors-anywhere.herokuapp.com/";

        // Execute request
        var xmlhttp = new XMLHttpRequest();

        // Or post, etc
        xmlhttp.open("GET", proxy + myUrl + '?src_lang=en&target_lang=kr&query=' + dragged);
        xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xmlhttp.setRequestHeader('Authorization', client_id);
        xmlhttp.send();
        //var jsonRequest = { source: 'en', target: 'ko', text: query };

        //xmlhttp.send(JSON.stringify(jsonRequest));

        xmlhttp.onload = function () {

            console.log(this.responseText);

            var jsonData = JSON.parse(this.responseText);
            //console.log(jsonData["message"]["result"]["translatedText"]);
            //for (var i = 0; i < jsonData["message"]["result"].length; i++) {
            //    var word = jsonData["data"]["translations"][i]["translatedText"];
            //    console.log("##########");
            //    console.log(word);
            //    console.log("##########");
            //    $('#r_naver ul').append("<li><label id = label" + i + ">" + word + '</label></li>');
            //}
            var word = jsonData["translated_text"];
            $('#r_naver ul').append("<li><label>" + word + '</label></li>');
        };
    }


    function translateVocab(word, pos) {
        var myUrl = 'https://translation.googleapis.com/language/translate/v2';
        //  But if you make it from a browser, then it will work without problem ...

        //// However to make it work, we are going to use the cors-anywhere free service to bypass this
        var proxy = 'https://cors-anywhere.herokuapp.com/';

        // Execute request
        var xmlhttp = new XMLHttpRequest();

        // Or post, etc
        xmlhttp.open("GET", proxy + myUrl + '?key=AIzaSyBCXxskVOciO7tlqD7-RR56MrFQGitL-30&q=' + word + '&source=en&target=ko&format=text', true);
        xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xmlhttp.send();

        xmlhttp.onload = function () {

            var jsonData = JSON.parse(this.responseText);

            var word = jsonData["data"]["translations"][0]["translatedText"];

            console.log(pos);
            $('#r_result #button' + pos).append(" : " + word);
        };

    }

    function getRecommendSentence(dragged, count) {
        var myUrl = 'http://mpbear11.duckdns.org:5000/sentences';
        //  But if you make it from a browser, then it will work without problem ...

        //// However to make it work, we are going to use the cors-anywhere free service to bypass this
        var proxy = 'https://cors-anywhere.herokuapp.com/';

        // Execute request
        var xmlhttp = new XMLHttpRequest();

        // Or post, etc
        xmlhttp.open("POST", proxy + myUrl, true);
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        console.log(JSON.stringify({ sentence: dragged}));
        xmlhttp.send(JSON.stringify({ sentence: dragged }));

        xmlhttp.onload = function () {
            $('#s_result ol').html("<p>문장 추천 결과</p>");
            console.log(this.responseText);

            var jsonData = JSON.parse(this.responseText);

            var sentences = jsonData["result"];

            for(var i = 0; i < sentences.length; i++){
                var sentence = sentences[i];

                $('#s_result ol').append("<li><p>'" + sentence + "</p></li>");

                //$("#button" + i).on("click", { word: sentence, dragged: dragged }, changeWord);

                //translateVocab(sentence, i);
            }

        };


    }

    function getRecommendList(dragged) {
        Word.run(function (context) {
            return context.sync()
                .then(function () {


                    var whole_text = $("#tmp_content").text();

                    var myUrl = 'http://mpbear11.duckdns.org:5000/dev/v3/data';
                    //  But if you make it from a browser, then it will work without problem ...

                    // However to make it work, we are going to use the cors-anywhere free service to bypass this
                    var proxy = 'https://cors-anywhere.herokuapp.com/';

                    // Execute request
                    var xmlhttp = new XMLHttpRequest();

                    // Or post, etc
                    xmlhttp.open("POST", proxy + myUrl, true);
                    xmlhttp.setRequestHeader("Content-Type", "application/json");
                    xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
                    console.log(JSON.stringify({ full_sentence: whole_text, target: dragged }));
                    //xmlhttp.send(JSON.stringify({ full_sentence: whole_text, target: "<31fe0826-7bb3-444d-8f2e-6ca06ae24e11>" + dragged }));
                    xmlhttp.send(JSON.stringify({ full_sentence: whole_text, target: "<31fe0826-7bb3-444d-8f2e-6ca06ae24e11>" + dragged }));
                    //xmlhttp.send(sentnece);
                    xmlhttp.onload = function () {
                        // do something to response
                        console.log("response");
                        console.log(JSON.parse(this.responseText));

                        var jsonData = JSON.parse(this.responseText);

                        if (jsonData["result"] == null) {
                            return;
                        }


                        var count = 0;

                        var drag = dragged;
                        $('#r_result ul').html("<p>단어 추천 결과</p>");
                        for (var i = 0; i < jsonData["result"].length; i++) {
                            var word = jsonData["result"][i]["target"];
                            console.log(word);

                            $('#r_result ul').append("<li><button type='button' class='btn btn-primary' id = button" + i + ">" + word + "</button></li>");

                            $("#button" + i).on("click", { word: word, dragged: dragged }, changeWord);

                            translateVocab(word, i);

                            count++;

                        }

                        for (var i = 0; i < jsonData["word2vec"].length; i++) {
                            var word = jsonData["word2vec"][i]["word"];
                            console.log(word);
                            $('#r_result ul').append("<li><button type='button' class='btn btn-primary' id = button" + (i + count) + ">" + word + '</button></li>');

                            $("#button" + (i + count)).on("click", { word: word, dragged: dragged }, changeWord);

                            translateVocab(word, i + count);

                            count++;

                        }
                    };
                });
        })
        .catch(errorHandler);


    }

    function sendHistory(dragged, changed) {

        Word.run(function (context) {

            return context.sync()
                .then(function () {
                    //$('#r_result').html('<h3>Naver</h3><ul></ul>');
                    var myUrl = 'http://mpbear11.duckdns.org:5000/history/push';
                    //  But if you make it from a browser, then it will work without problem ...

                    // However to make it work, we are going to use the cors-anywhere free service to bypass this
                    var proxy = 'https://cors-anywhere.herokuapp.com/';

                    // Execute request
                    var xmlhttp = new XMLHttpRequest();

                    // Or post, etc

                    xmlhttp.open("POST", proxy + myUrl, true);
                    xmlhttp.setRequestHeader("Content-Type", "application/json");
                    xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
                    xmlhttp.send(JSON.stringify({ user_name: "test1234", before: dragged, after: changed }));
                    //xmlhttp.send(sentnece);
                });
        })
        .catch(errorHandler);
    }

    function receiveHistory(dragged, changed) {
        var myUrl = 'http://mpbear11.duckdns.org:5000/history/get';
        //  But if you make it from a browser, then it will work without problem ...

        // However to make it work, we are going to use the cors-anywhere free service to bypass this
        var proxy = 'https://cors-anywhere.herokuapp.com/';

        // Execute request
        var xmlhttp = new XMLHttpRequest();

        // Or post, etc
        xmlhttp.open("POST", proxy + myUrl, true);
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xmlhttp.send(JSON.stringify({ user_name: "test1234" }));
        //xmlhttp.send(sentnece);

        $('#history_main').html("");

        xmlhttp.onload = function () {
            // do something to response
            //console.log(JSON.parse(this.responseText)["result"][0]["target"]["word"]);

            console.log("222222");
            console.log(this.responseText);
            var jsonData = JSON.parse(this.responseText);

            for (var i = jsonData["result"].length - 1; i >= jsonData["result"].length - 5; i--) {
                var before = jsonData["result"][i]["before"];
                var after = jsonData["result"][i]["after"];
                $('#history_main').append("<div><ul><li> 원래 단어 : " + before + " -> 수정한 단어 : " + after + "</div></li></ul>");
            }

        };

    }

    function changeWord(event) {
        Word.run(function (context) {

            var whole_text = $("#tmp_content").text();
            var dragged = context.document.getSelection();
            var dragged_history = $("#tmp_dragged").text().replace("<31fe0826-7bb3-444d-8f2e-6ca06ae24e11>", "");
            //context.load(dragged, 'text');
            context.document.body.clear();
            whole_text = whole_text.replace($("#tmp_dragged").text(), event.data.word);
            console.log("tmp_dragged : " + $("#tmp_dragged").text());
            console.log("btn_word : " + event.data.word);
            console.log("dragged_history : " + dragged_history);
            console.log("whole_text : " + whole_text);
            context.document.body.insertText(whole_text, 'Start');

            
            //console.log("clear");

            //$("#tmp_content").text(context.document.body.text);


            // 범위 선택 결과를 로드하는 명령을 큐에 넣습니다.

            return context.sync()
                .then(function () {

                    sendHistory(dragged_history, event.data.word);
                });
        })
        .catch(errorHandler);
    }

    function back() {
        document.location.href = "Main.html";
    }


    function vocabHistory(text) {
        $('#history_main').append("<div><ul><li>" + text + " : " + "</div></li></ul>");
    }

    function showHistory() {
        Word.run(function (context) {
            return context.sync()
                .then(function () {

                    receiveHistory();
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

                    $("#tmp_content").text(documentBody.text);
                    $("#tmp_dragged").text("<31fe0826-7bb3-444d-8f2e-6ca06ae24e11>" + dragged.text);
                    console.log("content");
                    console.log($("#tmp_content").text());
                    console.log($("#tmp_dragged").text());

                    

                    getRecommendList(dragged.text);
                    getRecommendSentence(dragged.text);
                    //vocabHistory(dragged.text);

                    //writeFile("text.txt", dragged.text);
                    //console.log(para.items[0].clear());
                    context.document.getSelection().insertText(dragged.text, 'Start');

                    sendToGoogle(dragged.text);

                    sendToNaver(dragged.text);

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
