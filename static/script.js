// ページ読み込み時に履歴を表示
document.addEventListener('DOMContentLoaded', loadHistory);

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

    resultSection.classList.remove('hidden');
    loading.classList.remove('hidden');
    adviceContent.innerHTML = "";

    fetch('/consult', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ businessName: bizName, goal: goal })
    })
    .then(response => response.json())
    .then(data => {
        loading.classList.add('hidden');
        if (data.advice) {
            adviceContent.innerHTML = marked.parse(data.advice);
            loadHistory(); // 履歴を再読み込み
        }
    });
}

// 履歴をデータベースから取得して表示
function loadHistory() {
    fetch('/history')
    .then(response => response.json())
    .then(data => {
        const historyList = document.getElementById('historyList');
        historyList.innerHTML = ""; // 一旦クリア

        data.forEach(item => {
            const card = document.createElement('div');
            card.className = 'history-item';
            card.innerHTML = `
                <strong>${item.biz_name}</strong>
                <span>${item.date}</span>
                <button onclick="showPastReport(\`${encodeURIComponent(item.advice)}\`)">詳細を見る</button>
            `;
            historyList.appendChild(card);
        });
    });
}

// 過去のレポートをメイン画面に表示
function showPastReport(encodedAdvice) {
    const adviceContent = document.getElementById('adviceContent');
    const resultSection = document.getElementById('resultSection');
    adviceContent.innerHTML = marked.parse(decodeURIComponent(encodedAdvice));
    resultSection.classList.remove('hidden');
    window.scrollTo({ top: resultSection.offsetTop, behavior: 'smooth' });
}

function saveAsPDF() {
    const element = document.getElementById('adviceContent');
    const bizName = document.getElementById('bizName').value || "report";
    html2pdf().set({ margin: 10, filename: `${bizName}_report.pdf` }).from(element).save();
}