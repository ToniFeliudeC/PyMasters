var editor = CodeMirror.fromTextArea(document.getElementById("code-editor-logs"), {
    mode: "python",
    lineNumbers: true,
    theme: "darcula",
    readOnly: true
  });

var editor = CodeMirror.fromTextArea(document.getElementById("code-editor-template"), {
  mode: "python",
  lineNumbers: true,
  theme: "darcula"
});