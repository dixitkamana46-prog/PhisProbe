async function scanURL() {
    const url = document.getElementById("urlInput").value;
    const loader = document.getElementById("loader");
    const resultDiv = document.getElementById("result");

    if (!url) {
        alert("Please enter a URL!");
        return;
    }

    loader.classList.remove("hidden");
    resultDiv.classList.add("hidden");

    const res = await fetch("/scan", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
    });

    const data = await res.json();

    loader.classList.add("hidden");
    resultDiv.classList.remove("hidden");

    let riskColor = data.risk > 60 ? "red" : data.risk > 30 ? "orange" : "lightgreen";
    let status = data.risk > 40 ? "Dangerous 🚨" :
                 data.risk > 20 ? "Suspicious ⚠️" :
                 "Safe ✅";

    let reasonsList = data.reasons.map(r => `<li>${r}</li>`).join("");

    resultDiv.innerHTML = `
        <p><strong>Domain:</strong> ${data.domain}</p>
        <p><strong>IP Address:</strong> ${data.ip}</p>
        <p><strong>Status:</strong> ${status}</p>
        <p><strong>Risk Score:</strong> <span style="color:${riskColor}">${data.risk}%</span></p>
        <p><strong>Analysis:</strong></p>
        <ul>${reasonsList}</ul>
    `;
}