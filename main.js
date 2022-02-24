// ==UserScript==
// @name         BIT-延河课堂-Killer
// @namespace    http://tampermonkey.net/
// @version      1.1.0
// @description  open to everyone!
// @author       Seroz, Y.D.X.
// @match        https://www.yanhekt.cn/*
// @grant        none
// @run-at       document-start
// @require      https://cdn.jsdelivr.net/npm/xhook@1.4.9/dist/xhook.min.js
// ==/UserScript==

(function () {
    'use strict'

    xhook.after((req, res) => {
        if (req.url.includes('/v1/auth/permission')) {
            res.text = res.data = JSON.stringify({
                code: 0,
                message: "",
                data: { allowed: true }
            })
        }
    })

})()
