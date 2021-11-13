// ==UserScript==
// @name         yanhekt_killer
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  open to everyone!
// @author       Seroz
// @match        https://www.yanhekt.cn/course/*
// @grant        none
// @run-at       document-start
// ==/UserScript==


function modifyResponse(response) {

    if (this.readyState === 4) {
        if (this.requestURL.indexOf("permission") != -1 && this.requestMethod.indexOf("GET") != -1) {
            Object.defineProperty(this, "responseText", { writable: true });
            this.responseText = '{"code":0,"message":"","data":{"allowed": true}}';
            Object.defineProperty(this, "response", { writable: true });
            this.response = '{"code":0,"message":"","data":{"allowed": true}}';
        }
    }
}

function openBypass(original_function) {

    return function (method, url, async) {
        this.requestMethod = method;
        this.requestURL = url;

        this.addEventListener("readystatechange", modifyResponse);
        return original_function.apply(this, arguments);
    };

}

// function sendBypass(original_function) {
//     return function (data) {
//         this.requestData = data;
//         return original_function.apply(this, arguments);
//     };
// }

XMLHttpRequest.prototype.open = openBypass(XMLHttpRequest.prototype.open);
// XMLHttpRequest.prototype.send = sendBypass(XMLHttpRequest.prototype.send);
