/// <reference path="/Scripts/FabricUI/MessageBanner.js" />


(function () {
    "use strict";

    var messageBanner;

    // 새 페이지가 로드될 때마다 초기화 함수가 실행되어야 합니다.
    Office.initialize = function (reason) {
        $(document).ready(function () {
            // FabricUI 알림 메커니즘을 초기화하고 숨깁니다.W
            var element = document.querySelector('.ms-MessageBanner');
            messageBanner = new fabric.MessageBanner(element);
            messageBanner.hideBanner();

            $('#login_button').click(login);
        });
    };

    function login() {
        document.location.href = "Main.html";
    }

    function loadSampleData() {

        //// Word 개체 모델에 대한 배치 작업을 실행합니다.
        //Word.run(function (context) {

        //    // 문서 본문에 대한 프록시 개체를 만듭니다.
        //    var body = context.document.body;

        //    // 본문 내용을 지울 명령을 큐에 넣습니다.
        //    body.clear();
        //    // Word 문서 본문의 마지막에 텍스트를 삽입하는 명령을 큐에 넣습니다.
        //    body.insertText("This is a sample text inserted in the document",
        //                    Word.InsertLocation.end);

        //    // 큐에 대기 중인 명령을 실행하여 문서 상태를 동기화한 후 프라미스를 반환하여 작업 완료를 표시합니다.
        //    return context.sync();
        //})
        //.catch(errorHandler);
    }

    function hightlightLongestWord() {

        Word.run(function (context) {

            // 현재 선택한 항목을 가져오는 명령을 큐에 넣은 다음
            // 해당 결과로 프록시 범위 개체를 만듭니다.
            var documentBody = context.document.body;
            context.load(documentBody);
            
            // 가장 긴 단어에 대한 검색 결과를 유지하기 위한 변수입니다.
            var searchResults;
            
            // 범위 선택 결과를 로드하는 명령을 큐에 넣습니다.
            

            return context.sync()
                .then(function () {
                    console.log(documentBody.text);
                });

            // 큐에 대기 중인 명령을 실행하여 문서 상태를 동기화한 후
            // 프라미스를 반환하여 작업 완료를 표시합니다.
           
        })
        .catch(errorHandler);
    } 


    function displaySelectedText() {
        Office.context.document.getSelectedDataAsync(Office.CoercionType.Text,
            function (result) {
                if (result.status === Office.AsyncResultStatus.Succeeded) {
                    showNotification('선택한 텍스트:', '"' + result.value + '"');
                } else {
                    showNotification('오류:', result.error.message);
                }
            });
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
