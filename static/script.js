// 戦略レポート生成の開始
function startConsult() {
    const bizName = document.getElementById('bizName').value;
    const goal = document.getElementById('goal').value;
    const resultSection = document.getElementById('resultSection');
    const loading = document.getElementById('loading');
    const adviceContent = document.getElementById('adviceContent');

    if (!bizName || !goal) {
        alert("企業名と悩みを入力してください。");
        return;
    }

    // 画面表示のリセット
    resultSection.classList.remove('hidden');
    loading.classList.remove('hidden');
    adviceContent.classList.add('hidden');
    adviceContent.innerHTML = "";

    // Flaskサーバーへリクエスト
    fetch('/consult', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ businessName: bizName, goal: goal })
    })
    .then(response => response.json())
    .then(data => {
        // ローディングを隠し、結果を表示
        loading.classList.add('hidden');
        adviceContent.classList.remove('hidden');

        if (data.advice) {
            // MarkdownをHTMLに変換して表示
            adviceContent.innerHTML = marked.parse(data.advice);
        } else {
            adviceContent.innerHTML = `<p style="color:red;">エラー: ${data.error}</p>`;
        }
    })
    .catch(error => {
        loading.classList.add('hidden');
        adviceContent.classList.remove('hidden');
        adviceContent.innerHTML = `<p style="color:red;">通信エラーが発生しました。</p>`;
    });
}

// ★追加：PDF保存機能
function saveAsPDF() {
    const element = document.getElementById('adviceContent');
    const bizName = document.getElementById('bizName').value || "strategy_report";

    const opt = {
        margin:       10,
        filename:     `${bizName}_戦略レポート.pdf`,
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2 }, 
        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };

    // PDF生成の実行
    html2pdf().set(opt).from(element).save();
}