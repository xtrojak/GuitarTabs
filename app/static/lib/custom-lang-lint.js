// CodeMirror, copyright (c) by Marijn Haverbeke and others
// Distributed under an MIT license: https://codemirror.net/LICENSE


(function(mod) {
  if (typeof exports == "object" && typeof module == "object") // CommonJS
    mod(require("../../lib/codemirror"));
  else if (typeof define == "function" && define.amd) // AMD
    define(["../../lib/codemirror"], mod);
  else // Plain browser env
    mod(CodeMirror);
})(function(CodeMirror) {
  "use strict";

  function validator(text, options) {
    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/parse";
    var data = {"expression": text};
    var output = [];
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onload = function () {
        if (xhr.status == 200){
            var response = JSON.parse(xhr.responseText);
            if (!response.success){
                var expected = '';
                if (response.expected.length == 1){
                    expected = '"' + response.expected[0] + '"';
                } else {
                    expected = 'one of "' + response.expected.join(', ') + '"';
                }

                var start = response.column - 1;
                var end = start + response.unexpected.length;

                var hint = {
                  message: 'Unexpected "' + response.unexpected + '", expected ' + expected + ' at position [row: ' + response.line + ', column: ' + response.column + ']',
                  severity: "error",
                  from: CodeMirror.Pos(response.line - 1, start),
                  to: CodeMirror.Pos(response.line - 1, end)
                };
                output.push(hint);
            };
        };
    };
    xhr.send(JSON.stringify(data));
    return output;
  }

  CodeMirror.registerHelper("lint", "custom-lang", validator);
});