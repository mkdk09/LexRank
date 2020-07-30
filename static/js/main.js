let text_count;

// ウィンドウ読み込み時にフォームにfocusする
window.onload = function () {
    document.formStr.str.focus();
    text_count = document.getElementById('textlength');
    setInterval("countLength(document.formStr.str.value)", 1000);
}

function countLength(text) {
    if (text.length !== 0) {
	text_count.innerHTML = text.length + "文字";
    }
    else {
	text_count.innerHTML = "";
    }
}
