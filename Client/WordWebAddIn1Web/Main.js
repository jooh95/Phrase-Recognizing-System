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

            $('#recommend_button').click(recommend);
        });
    };

    function sendToServer(dragged, whole_text) {
        var myUrl = 'http://52.79.106.90:5000/dev/data';
        //  But if you make it from a browser, then it will work without problem ...

        // However to make it work, we are going to use the cors-anywhere free service to bypass this
        var proxy = 'https://cors-anywhere.herokuapp.com/';

        // Execute request
        var xmlhttp = new XMLHttpRequest();

        // Or post, etc
        xmlhttp.open("POST", proxy + myUrl, true);
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        console.log(JSON.stringify({ full_sentence: whole_text, target: dragged + "<31fe0826-7bb3-444d-8f2e-6ca06ae24e11>"}));
        xmlhttp.send(JSON.stringify({ full_sentence: whole_text, target: dragged + "<31fe0826-7bb3-444d-8f2e-6ca06ae24e11>" }));
        //xmlhttp.send(sentnece);
        xmlhttp.onload = function () {
            // do something to response
            console.log(this.responseText);


            //이동
            //recommend();
        };
    }

    function recommendSentence() {

        Word.run(function (context) {
            // 현재 선택한 항목을 가져오는 명령을 큐에 넣은 다음
            // 해당 결과로 프록시 범위 개체를 만듭니다.

            //마우스 파트
            //function mousePosition(evt) {
            //    evt = evt || window.event;
            //    var xPos = evt.pageX || evt.clientX || evt.offsetX || evt.x;
            //    var yPos = evt.pageY || evt.clientY || evt.offsetY || evt.y;
            //    return [xPos, yPos];
            //}
            //function moveWindow(e) {
            //    document.onmousemove = function (e) {
            //        console.log(mousePosition(e));
            //    };
            //}
            //onmousemove = moveWindow;
            var para = context.document.getSelection().paragraphs;
            para.load();
            context.document.getSelection().insertText("<31fe0826-7bb3-444d-8f2e-6ca06ae24e11>", 'Start');
            context.document.getSelection().insertText('<31fe0826-7bb3-444d-8f2e-6ca06ae24e11>', 'End');
            
            var dragged = context.document.getSelection();
            context.load(dragged, 'text');

            var documentBody = context.document.body;
            context.load(documentBody, 'text');
            
            //서버로 전송
            //sendToServer(dragged.text, documentBody.text);

            // 범위 선택 결과를 로드하는 명령을 큐에 넣습니다.

            return context.sync()
                .then(function () {
                    //sendToServer(dragged.text, documentBody.text);
                    console.log(para.items[0]);
                    //console.log(documentBody.text);
                    //console.log(tmp.text);
                    
                    //context.document.body.clear();
                    //context.document.body.insertText(documentBody.text, 'Start');
                    

                    //console.log(dragged.text);

                    //팝업 파트
                    //Office.context.ui.displayDialogAsync(window.location.origin + '/Result.html', { height: 30, width: 40 });

                    //이동
                    

                    //return context.sync().then(function () {
                        
                    //});


                    
                });

        })  
        .catch(errorHandler);
    }

    function recommend() {
        document.location.href = "Result.html";
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
