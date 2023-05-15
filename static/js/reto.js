var editor = CodeMirror.fromTextArea(document.getElementById("code-editor-logs"), {
    mode: "python",
    theme: "darcula",
    readOnly: true
  });

var editor2 = CodeMirror.fromTextArea(document.getElementById("code-editor-solution"), {
  mode: "python",
  lineNumbers: true,
  theme: "darcula"
});

var editor3 = CodeMirror.fromTextArea(document.getElementById("code-editor-instructions"), {
  mode: "normal",
  lineNumbers: true,
  theme: "darcula"
});

