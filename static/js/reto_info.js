var editor = CodeMirror.fromTextArea(document.getElementById("code-editor-instructions"), {
    mode: "md",
    lineNumbers: true,
    theme: "darcula",
    readOnly: true
  });

var editor2 = CodeMirror.fromTextArea(document.getElementById("code-editor-tests"), {
  mode: "python",
  lineNumbers: true,
  theme: "darcula",
  readOnly: true
});

var editor3 = CodeMirror.fromTextArea(document.getElementById("code-editor-template"), {
    mode: "python",
    lineNumbers: true,
    theme: "darcula",
    readOnly: true
  });
